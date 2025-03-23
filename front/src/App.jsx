import React, {useState} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login.jsx';
import MainView from './MainView.jsx';
import UserLibrary from './MyBooks.jsx';
import Register from './Register.jsx';
import ResetPassword from './ResetPassword.jsx';
import Book from './Book.jsx';
import './App.css';

function App() {

    const [sampleBooks, setSampleBooks] = useState([
    {
      id: 1,
      title: 'El Señor de los Anillos',
      author: 'J.R.R. Tolkien',
      status: 'Prestado',
      description: 'Una épica historia de fantasía que sigue el viaje de Frodo Bolsón...',
      imagen: '/ruta/a/imagen1.jpg',
      categorias: ['Ficción']
    },
    {
      id: 2,
      title: 'Breves respuestas',
      author: 'Stephen Hawking',
      status: 'Prestar',
      description: '',
      imagen: '/ruta/a/imagen2.jpg',
      categorias: ['Ciencia']
    },
    {
      id: 3,
      title: 'Sapiens',
      author: 'Yuval Noah Harari',
      status: 'Prestado',
      description: '',
      imagen: '/ruta/a/imagen3.jpg',
      categorias: ['Historia']
    },
    {
      id: 4,
      title: 'El arte de la guerra',
      author: 'Sun Tzu',
      status: 'Prestar',
      description: '',
      imagen: '/ruta/a/imagen4.jpg',
      categorias: ['Arte', 'Historia']
    },

  ]);
    const handleReturnBook = (bookId) => {
    setSampleBooks(prevBooks =>
      prevBooks.map(book =>
        book.id === bookId ? { ...book, status: 'Prestar' } : book
      )
    );
  };
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/registro" element={<Register />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/mi-libreria" element={<UserLibrary books={sampleBooks} onReturnBook={handleReturnBook}/>} />
        <Route path="/main" element={<MainView books={sampleBooks} setBooks={setSampleBooks} />} />
        <Route path="/book/:bookId" element={<Book books={sampleBooks} />} />
      </Routes>
    </Router>
  );
}

export default App;
