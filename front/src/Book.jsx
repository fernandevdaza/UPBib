import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './Book.css';

const Book = ({ books }) => {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const book = books.find(b => b.id === parseInt(bookId));

  if (!book) {
    return <div className="error-container">Libro no encontrado</div>;
  }

  return (
    <div className="book-container">
      <button onClick={() => navigate(-1)} className="back-button">
        ← Volver
      </button>

      <div className="book-details">
        <div className="book-cover-large">
          <img
            src={book.imagen}
            alt={book.title}
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'ruta/a/imagen-default.jpg';
            }}
          />
        </div>

        <div className="book-info">
          <h1>{book.title}</h1>
          <h2>Por {book.author}</h2>
          <p className="description">
            {book.description || 'Descripción no disponible'}
          </p>
          <div className="meta-data">
            <p><strong>Categorías:</strong> {book.categorias?.join(', ') || 'Sin categorías'}</p>
            <p><strong>Estado:</strong> {book.status}</p>
            <p><strong>ISBN:</strong> {book.isbn || 'No disponible'}</p>
            <p><strong>Año de publicación:</strong> {book.publicationYear || 'Desconocido'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Book;