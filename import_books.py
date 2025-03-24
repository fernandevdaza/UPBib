import csv
import re
from datetime import date
from pathlib import Path
from botocore.exceptions import ClientError
import boto3
from sqlalchemy import text

from app.models.database import get_db_connection
from app.controllers.libro_controller import LibroController
from app.controllers.autor_controller import AutorController
from app.controllers.categoria_controller import CategoriaController
from app.controllers.edicion_controller import EdicionController

class BookImporter:
    def __init__(self, csv_path, libros_dir, portadas_dir, s3_bucket):
        self.csv_path = csv_path
        self.libros_dir = Path(libros_dir)
        self.portadas_dir = Path(portadas_dir)
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.db = get_db_connection()
        self.region = self.get_bucket_region()

    def get_bucket_region(self):
        """Obtiene la región del bucket S3"""
        try:
            return self.s3.get_bucket_location(Bucket=self.bucket)['LocationConstraint'] or 'us-east-1'
        except ClientError as e:
            print(f"Error obteniendo región del bucket: {str(e)}")
            return 'us-east-1'
    @staticmethod
    def clean_title(title):
        """Elimina número y punto inicial del título"""
        return re.sub(r'^\d+\.\s*', '', title).strip()

    def upload_to_s3(self, file_path, folder='books'):
        """Sube archivo a S3 y retorna la clave (sin URL)"""
        try:
            key = f"{folder}/{file_path.name}"
            self.s3.upload_file(
                str(file_path),
                self.bucket,
                key
            )
            return key
        except Exception as e:
            print(f"Error subiendo {file_path}: {str(e)}")
            return None

    @staticmethod
    def extract_number(filename):
        match = re.search(r'^(\d+)', filename)
        return int(match.group(1)) if match else None

    def process_row(self, row):
        book_number = self.extract_number(row['titulo'])
        try:
            cleaned_title = self.clean_title(row['titulo'])
            if not book_number:
                print(f"⚠️ Título sin número: {row['titulo']}")
                return

            pdf_file = next(self.libros_dir.glob(f"{book_number}.*.pdf"), None)
            cover_file = next(self.portadas_dir.glob(f"{book_number}.jpg"), None)

            if not pdf_file or not cover_file:
                print(f"Archivos faltantes para libro #{book_number}")
                return

            pdf_key = self.upload_to_s3(pdf_file, "libros")
            cover_key = self.upload_to_s3(cover_file, "portadas")

            self.db.begin()
            libro_id = LibroController.crear_libro_base(
                titulo=cleaned_title,
                descripcion=row['descripcion'],
                fecha_publicacion=row['fecha_publicacion'],
                imagen_url=cover_key,
                db=self.db
            )["id_libro"]
            self.db.commit()

            for edicion in row['ediciones'].split('|'):
                edicion_data = edicion.split(';')
                isbn = edicion_data[0].split('=')[1]
                fecha = edicion_data[1].split('=')[1]

                EdicionController.crear_edicion(
                    libro_id=libro_id,
                    isbn=isbn,
                    fecha_edicion=fecha,
                    enlace=pdf_key,
                    db=self.db
                )

            self.db.commit()


            autores_ids = []
            for autor in row['autores'].split(','):
                autor = autor.strip()
                if ' ' in autor:
                    nombres = autor.split(' ', 1)
                    nombre = nombres[0]
                    apellido = nombres[1]
                else:
                    nombre = autor
                    apellido = ''

                autor_id = AutorController.create_autor(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=date(1900, 1, 1),
                    db=self.db
                )["id_autor"]
                autores_ids.append(autor_id)

            self.db.commit()


            if autores_ids:
                self.db.execute(
                    text("""
                                INSERT IGNORE INTO Libros_Autores 
                                (libros_id_libro, autores_id_autor) 
                                VALUES (:libro_id, :autor_id)
                            """),
                    [{"libro_id": libro_id, "autor_id": aid} for aid in autores_ids]
                )

            self.db.commit()


            categorias_ids = []
            for categoria in row['categorias'].split(','):
                categoria = categoria.strip()
                categoria_id = CategoriaController.create_categoria(
                    nombre=categoria,
                    db=self.db
                )["id_categoria"]
                categorias_ids.append(categoria_id)

            self.db.commit()


            if categorias_ids:
                self.db.execute(
                    text("""
                                INSERT IGNORE INTO Libros_Categorias 
                                (libros_id_libro, categorias_id_categoria) 
                                VALUES (:libro_id, :categoria_id)
                            """),
                    [{"libro_id": libro_id, "categoria_id": cid} for cid in categorias_ids]
                )

            self.db.commit()
            print(f"✅ Libro #{book_number} importado completamente")

        except Exception as e:
            self.db.rollback()
            print(f"Error procesando libro #{book_number}: {str(e)}")

    def run(self):
        with open(self.csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.process_row(row)