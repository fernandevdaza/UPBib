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
    const [sampleBooks, setSampleBooks] = useState([]);
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
        <Route path="/main" element={<MainView />} />
        <Route path="/book/:bookId" element={<Book books={sampleBooks} />} />
        <Route path = "/book/:id/read" element={ <BookDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
