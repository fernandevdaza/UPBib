import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './MainView.css';

const UserLibrary = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  
  // Ejemplo de libros del usuario (puedes recibirlos por props o desde un estado global)
  const userBooks = [
    // Agrega aquí los libros del usuario
  ];

  return (
    <div className="main-container">
      <nav className="top-bar">
        <Link to="/">
          <img className="imageOtherViews" src="public/LogoUPBib2.png" alt="Logo Main" />
        </Link>
        
        <div className="user-profile" onClick={() => setShowDropdown(!showDropdown)}>
          <div className="user-image"></div>
          <span>Usuario</span>
          {showDropdown && (
            <div className="profile-dropdown">
              <button>Mi Perfil</button>
              <button>Ajustes</button>
              <button>Cerrar Sesión</button>
            </div>
          )}
        </div>
      </nav>

      <div className="categories-container">
        <div className="category-section">
          <h2>Mi Librero</h2>
          <div className="books-scroll">
            {userBooks
            .filter(book => book.status === 'Prestado') // Filtra por estado
            .map(book => (
          <div key={book.id} className="book-card">
            <div className="book-cover" style={{ backgroundImage: `url(${book.imagen})` }}>
              {!book.imagen && <div className="cover-placeholder">Sin portada</div>}
            </div>
              <div className="book-info">
                <h3 className="book-title">{book.title}</h3>
                <p className="book-author">{book.author}</p>
              </div>
                <button className={`status-btn devolver`}>
                Devolver
                </button>
            </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserLibrary;