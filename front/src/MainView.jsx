import './MainView.css'
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserLibrary from './MyBooks';
import { Link } from 'react-router-dom';

const MainView = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const categories = ['Ficción', 'Ciencia', 'Historia', 'Tecnología', 'Arte'];
  
  // Libros con categorías asignadas
  const sampleBooks = [
    { 
      id: 1, 
      title: 'El Señor de los Anillos', 
      author: 'J.R.R. Tolkien', 
      status: 'Prestado',
      imagen: '/ruta/a/imagen1.jpg',
      categorias: ['Ficción']
    },
    { 
      id: 2, 
      title: 'Breves respuestas', 
      author: 'Stephen Hawking', 
      status: 'Prestar',
      imagen: '/ruta/a/imagen2.jpg',
      categorias: ['Ciencia']
    },
    { 
      id: 3, 
      title: 'Sapiens', 
      author: 'Yuval Noah Harari', 
      status: 'Prestado',
      imagen: '/ruta/a/imagen3.jpg',
      categorias: ['Historia']
    },
    { 
      id: 4, 
      title: 'El arte de la guerra', 
      author: 'Sun Tzu', 
      status: 'Prestar',
      imagen: '/ruta/a/imagen4.jpg',
      categorias: ['Arte', 'Historia']
    },
    // ... más libros
  ];

  return (
    <div className="main-container">
      
      {/* Barra superior */}
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
              <button>Cerrar Sesión</button>
            </div>
          )}
        </div>
      </nav>

      {/* Secciones de categorías */}
      <div className="categories-container">
        {categories.map((category) => (
          <div key={category} className="category-section">
            <h2>{category}</h2>
            <div className="books-scroll">
              {sampleBooks
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
                      <h3 className="book-title">{book.title}</h3>
                      <p className="book-author">{book.author}</p>
                    </div>
                    <button className={`status-btn ${book.status.toLowerCase()}`}>
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