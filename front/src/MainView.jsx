import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './MainView.css';
import api from './utils/api.js';
import {getCookie} from "./utils/getCookie.js";

const MainView = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [groupedBooks, setGroupedBooks] = useState({});
  const navigate = useNavigate();


  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await api.get('/libros/');
        const booksData = response.data;

        const grouped = booksData.reduce((acc, book) => {
          const categories = book.categorias.split(',').map(category => category.trim());

          categories.forEach((category) => {
            if (!acc[category]) {
              acc[category] = [];
            }
            acc[category].push(book);
          });

          return acc;
        }, {});

        setGroupedBooks(grouped);
      } catch (error) {
        console.error('Error al obtener los libros:', error);
      }
    };

    fetchBooks();
  }, []);

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout', {
        'refresh_token': localStorage.getItem("refresh_token")});
      sessionStorage.removeItem('access_token');
      navigate('/');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };
  const toggleBookStatus = async (bookId, currentStatus) => {
    try {
      let newStatus;
      let apiEndpoint;

      if (currentStatus === 'Disponible') {
        apiEndpoint = `/librero/libros/${bookId}/prestar`;
        newStatus = 'Prestado';
      }
      else if (currentStatus === 'Prestado') {
        apiEndpoint = `/librero/libros/${bookId}/devolver`;
        newStatus = 'Disponible';
      }

      const response = await api.post(apiEndpoint);

      if (response.status === 200) {
        setGroupedBooks((prevGroupedBooks) => {
          return Object.keys(prevGroupedBooks).reduce((acc, category) => {
            acc[category] = prevGroupedBooks[category].map((book) => {
              if (book.id_libro === bookId) {
                return { ...book, status: newStatus };
              }
              return book;
            });
            return acc;
          }, {});
        });
      }
    } catch (error) {
      console.error('Error al cambiar el estado del libro:', error);
    }
  };

  return (
    <div className="main-container">
      <nav className="top-bar">
        <img className="imageOtherViews" src="public/logoUPBib2.png" alt="Logo Main" />
        <button
          type="button"
          className="mis-libros-btn"
          onClick={() => navigate('/mi-libreria')}
        >
          Mi librero
        </button>
        <div className="search-container">
          <input type="text" placeholder="Buscar..." />
        </div>
        <div className="user-profile" onClick={() => setShowDropdown(!showDropdown)}>
          <div className="user-image"></div>
          <span>Usuario</span>
          {showDropdown && (
            <div className="profile-dropdown">
              <button>Mi Perfil</button>
              <button>Ajustes</button>
              <button onClick={handleLogout}>Cerrar Sesión</button>
            </div>
          )}
        </div>
      </nav>

      <div className="categories-container">
        {Object.keys(groupedBooks).map((category) => (
          <div key={category} className="category-section">
            <h2>{category}</h2>
            <div className="books-scroll">
              {groupedBooks[category].map((book) => (
                  <div key={book.id_libro} className="book-card">
                    <div
                        className="book-cover"
                        style={{
                          backgroundImage: `url(${book.imagen_libro_url})`,  // Usar la URL completa de la imagen
                        }}
                    >
                      {!book.imagen_libro_url && <div className="cover-placeholder">Sin portada</div>}
                    </div>
                    <div className="book-info">
                      <h3 className="book-title">
                        <Link to={`/book/${book.id_libro}`}>{book.titulo_libro}</Link>
                      </h3>
                      <p className="book-author">{book.autores}</p>
                    </div>
                    <button
                        className={`status-btn ${book.status ? book.status.toLowerCase() : 'disponible'}`}
                        onClick={() => toggleBookStatus(book.id_libro, book.status)}
                        disabled={book.status === 'Prestado'}
                    >
                      {book.status || 'Disponible'}
                    </button>
                  </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MainView;
