import csv
import re
from datetime import date
from pathlib import Path
from time import strptime

import boto3
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

    def extract_number(self, filename):
        match = re.search(r'^(\d+)', filename)
        return int(match.group(1)) if match else None

    def upload_to_s3(self, file_path):
        try:
            self.s3.upload_file(str(file_path), self.bucket, file_path.name)
            return f"s3://{self.bucket}/{file_path.name}"
        except Exception as e:
            print(f"Error subiendo {file_path}: {str(e)}")
            return None

    def process_row(self, row):
        try:
            book_number = self.extract_number(row['titulo'])

            if not book_number:
                print(f"⚠️ Título sin número: {row['titulo']}")
                return

            pdf_file = next(self.libros_dir.glob(f"{book_number}.*.pdf"), None)
            cover_file = next(self.portadas_dir.glob(f"{book_number}.jpg"), None)

            if not pdf_file or not cover_file:
                print(f"Archivos faltantes para libro #{book_number}")
                return

            pdf_url = self.upload_to_s3(pdf_file)
            cover_url = self.upload_to_s3(cover_file)

            self.db.begin()

            libro_id = LibroController.crear_libro_base(
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                fecha_publicacion=row['fecha_publicacion'],
                imagen_url=cover_url,
            )

            for edicion in row['ediciones'].split('|'):
                isbn, fecha = edicion.split(';')
                EdicionController.crear_edicion(
                    libro_id=libro_id["id_libro"],
                    isbn=isbn.split('=')[1],
                    fecha_edicion=fecha.split('=')[1],
                    enlace=pdf_url,
                    db=self.db
                )

            for autor in row['autores'].split(','):
                nombre, apellido = autor.strip().split(' ', 1) if ' ' in autor else (autor, '')
                AutorController.create_autor(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=strptime("1900-01-01", "%Y-%m-%d"),
                )

            for categoria in row['categorias'].split(','):
                CategoriaController.create_categoria(
                    nombre=categoria.strip(),
                )

            self.db.commit()
            print(f"Libro #{book_number} importado")

        except Exception as e:
            self.db.rollback()
            print(f"Error procesando libro #{book_number}: {str(e)}")

    def run(self):
        with open(self.csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.process_row(row)