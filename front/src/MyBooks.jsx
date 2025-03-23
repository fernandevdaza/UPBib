import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './MyBooks.css';

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
            {books
              .filter(book => book.status === 'Prestado')
              .map(book => (
                <div key={book.id} className="book-card-book">
                  <div
                    className="book-cover-book"
                    style={{ backgroundImage: `url(${book.imagen})` }}
                  >
                    {!book.imagen && <div className="cover-placeholder-book">Sin portada</div>}
                  </div>
                  <div className="book-info-book">
                    <h3 className="book-title-book">{book.title}</h3>
                    <p className="book-author-book">{book.author}</p>
                  </div>
                  <div className="book-actions-book">
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