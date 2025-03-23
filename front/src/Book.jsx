import React from 'react';
import {useParams, useNavigate, Link} from 'react-router-dom';
import './Book.css';

const Book = ({ books }) => {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const book = books.find(b => b.id === parseInt(bookId));
  const [showDropdown, setShowDropdown] = React.useState(false);

  if (!book) {
    return <div className="error-container">Libro no encontrado</div>;
  }

  return (
    <div className="book-container">
      <nav className="book-top-bar">
        <img className="imageOtherViews-book" src="/logoUPBib2.png" alt="Logo Main" />
        <Link to="/main">
          <button className="back-button">← Volver</button>
        </Link>
        <div className="book-user-profile" onClick={() => setShowDropdown(!showDropdown)}>
          <div className="book-user-image"></div>
          <span>Usuario</span>
          {showDropdown && (
            <div className="book-profile-dropdown">
              <button>Mi Perfil</button>
              <button>Ajustes</button>
              <button onClick={handleLogout}>Cerrar Sesión</button>
            </div>
          )}
        </div>
      </nav>

      <div className="main-content">
        <div className="book-card-view">
          <div className="book-cover-container">
            <img
              src={book.imagen}
              alt={book.title}
              className="book-cover-large"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = 'ruta/a/imagen-default.jpg';
              }}
            />
          </div>

          <div className="book-info-container">
            <h1 className="book-title-view">{book.title}</h1>
            <h2 className="book-author-view">Por {book.author}</h2>

            <div className="book-meta">
              <div className="meta-item">
                <span className="meta-label">Categorías:</span>
                <span className="meta-value">{book.categorias?.join(', ') || 'Sin categorías'}</span>
              </div>

                <div className="meta-item">
                  <span className="meta-label">ISBN:</span>
                  <span className="meta-value">{book.isbn || 'No disponible'}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Año de publicación:</span>
                  <span className="meta-value">{book.publicationYear || 'Desconocido'}</span>
                </div>

              <div className="description-container">
                <p className="book-description">
                  {book.description || 'Descripción no disponible'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Book;