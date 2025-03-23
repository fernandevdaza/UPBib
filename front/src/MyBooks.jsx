import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './MainView.css';

const UserLibrary = ({ books, onReturnBook }) => {
  const [showDropdown, setShowDropdown] = React.useState(false);
  const navigate = useNavigate();

  const handleLogout = () => navigate('/');

  const handleLeerLibro = (bookId) => {
    window.open(`/lector/${bookId}`, '_blank');
  };

  const handleDevolverLibro = (bookId) => {
    onReturnBook(bookId);
  };

  return (
    <div className="main-container">
      <nav className="top-bar">
        <img className="imageOtherViews" src="public/LogoUPBib2.png" alt="Logo Main" />
        <Link to="/main">
          <button className="biblioteca-btn">Biblioteca</button>
        </Link>
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
        <div className="category-section">
          <h2>Mi Librero</h2>
          <div className="books-scroll">
            {books
              .filter(book => book.status === 'Prestado')
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
                  <div className="book-actions">
                    <button
                      className="leer-btn"
                      onClick={() => handleLeerLibro(book.id)}
                    >
                      Leer
                    </button>
                    <button
                      className="devolver-btn"
                      onClick={() => handleDevolverLibro(book.id)}
                    >
                      Devolver
                    </button>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserLibrary;