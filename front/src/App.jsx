import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login.jsx';
import MainView from './MainView.jsx';
import UserLibrary from './MyBooks.jsx';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/main" element={<MainView />} />
        <Route path="/mi-libreria" element={<UserLibrary />} />
      </Routes>
    </Router>
  );
}

export default App;
