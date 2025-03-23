import './MainView.css'
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const MainView = ({ books, setBooks }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const categories = ['Ficción', 'Ciencia', 'Historia', 'Tecnología', 'Arte'];
  const navigate = useNavigate();

  const handleLogout = () => navigate('/');

  const toggleBookStatus = (bookId) => {
    setBooks(prevBooks =>
      prevBooks.map(book =>
        book.id === bookId && book.status === 'Prestar'
          ? {...book, status: 'Prestado'}
          : book
      )
    );
  };

  return (
    <div className="main-container">
      <nav className="top-bar">
        <img className="imageOtherViews" src="public/LogoUPBib2.png" alt="Logo Main" />
        <Link to="/mi-libreria">
            <button className="mis-libros-btn">Mis Libros</button>
        </Link>
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
        {categories.map((category) => (
          <div key={category} className="category-section">
            <h2>{category}</h2>
            <div className="books-scroll">
              {books
                .filter(book => book.categorias.includes(category))
                .map(book => (
                  <div key={book.id} className="book-card">
                    <div
                      className="book-cover"
                      style={{ backgroundImage: `url(${book.imagen})` }}
                    >
                      {!book.imagen && <div className="cover-placeholder">Sin portada</div>}
                    </div>
                    <div className="book-info">
                      <h3 className="book-title">
                        <Link to={`/book/${book.id}`}>{book.title}</Link>
                      </h3>
                      <p className="book-author">{book.author}</p>
                    </div>
                    <button
                      className={`status-btn ${book.status.toLowerCase()}`}
                      onClick={() => toggleBookStatus(book.id)}
                      disabled={book.status === 'Prestado'}
                    >
                      {book.status}
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