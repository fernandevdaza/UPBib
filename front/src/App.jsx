import React, {useState} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login.jsx';
import MainView from './MainView.jsx';
import UserLibrary from './MyBooks.jsx';
import Register from './Register.jsx';
import ResetPassword from './ResetPassword.jsx';
import Book from './Book.jsx';
import './App.css';
import BookDetail from './BookDetail.jsx';

function App() {

    const [sampleBooks, setSampleBooks] = useState([
    {
      id: 1,
      title: 'El Señor de los Anillos',
      author: 'J.R.R. Tolkien',
      status: 'Prestado',
      description: '"El Señor de los Anillos" es una obra de fantasía épica que sigue las aventuras de un joven hobbit llamado Frodo Bolsón, quien recibe la misión de destruir un anillo mágico con un poder inmenso. Este anillo fue forjado por el oscuro señor Sauron, quien busca recuperarlo para dominar toda la Tierra Media. La historia narra su viaje junto con un grupo diverso de compañeros, incluyendo al mago Gandalf, el elfo Legolas, el enano Gimli, y el hombre Aragorn, descendiente de los antiguos reyes. A lo largo de la serie, Frodo y su grupo deben enfrentarse a diversos desafíos, como monstruos, traiciones y luchas contra las fuerzas oscuras, mientras intentan evitar que Sauron se apodere del anillo y destruya el mundo tal como lo conocen.',
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
        <Route path = "/book/:id/read" element={ <BookDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
