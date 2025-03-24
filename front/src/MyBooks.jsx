import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './MyBooks.css';
import api from './utils/api.js';

const UserLibrary = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await api.get('/libros/'); // Llamada a la API
        setBooks(response.data);
      } catch (error) {
        console.error('Error al obtener los libros:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  const handleLeerLibro = (bookId) => {
    window.open(`/book/${bookId}/read`, "_blank");
  };

  const handleDevolverLibro = async (bookId) => {
    try {
      const response = await api.post(`/librero/libros/${bookId}/devolver`);
      if (response.status === 200) {
        setBooks(prevBooks =>
          prevBooks.map(book =>
            book.id_libro === bookId ? { ...book, status: 'Disponible' } : book
          )
        );
      }
    } catch (error) {
      console.error('Error al devolver el libro:', error);
    }
  };

  const handlePrestarLibro = async (bookId) => {
    try {
      const response = await api.post(`/librero/libros/${bookId}/prestar`);
      if (response.status === 200) {
        setBooks(prevBooks =>
          prevBooks.map(book =>
            book.id_libro === bookId ? { ...book, status: 'Prestado' } : book
          )
        );
      }
    } catch (error) {
      console.error('Error al prestar el libro:', error);
    }
  };

  return (
    <div className="main-container-Books">
      <nav className="top-bar-Books">
        <img className="imageOtherViews-mybooks" src="public/logoUPBib2.png" alt="Logo Main" />
        <Link to="/main">
          <button className="biblioteca-btn">Biblioteca</button>
        </Link>
        <div className="user-profile-books" onClick={() => setShowDropdown(!showDropdown)}>
          <div className="user-image-books"></div>
          <span>Usuario</span>
          {showDropdown && (
            <div className="profile-dropdown-books">
              <button>Mi Perfil</button>
              <button>Ajustes</button>
              <button onClick={handleLogout}>Cerrar Sesión</button>
            </div>
          )}
        </div>
      </nav>

      <div className="categories-container-book">
        <div className="category-section-book">
          <h2>Mi Librero</h2>
          <div className="books-scroll-book">
            {loading ? (
              <p>Cargando libros...</p>
            ) : (
              books
                .filter(book => book.status === 'Prestado') // Filtrar solo los libros prestados
                .map(book => (
                  <div key={book.id_libro} className="book-card-book">
                    <div
                      className="book-cover-book"
                      style={{ backgroundImage: `url(${book.imagen_libro_url})` }}
                    >
                      {!book.imagen_libro_url && <div className="cover-placeholder-book">Sin portada</div>}
                    </div>
                    <div className="book-info-book">
                      <h3 className="book-title-book">{book.titulo_libro}</h3>
                      <p className="book-author-book">{book.autores}</p>
                    </div>
                    <div className="book-actions-book">
                      <button
                        className="leer-btn"
                        onClick={() => handleLeerLibro(book.id_libro)}
                      >
                        Leer
                      </button>
                      <button
                        className="devolver-btn"
                        onClick={() => handleDevolverLibro(book.id_libro)}
                      >
                        Devolver
                      </button>
                      {book.status === 'Disponible' && (
                        <button
                          className="prestar-btn"
                          onClick={() => handlePrestarLibro(book.id_libro)}
                        >
                          Prestar
                        </button>
                      )}
                    </div>
                  </div>
                ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserLibrary;
