import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ResetPassword.css'

const ResetPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      if (response.ok) {
        setMessage('Se ha enviado un enlace de recuperación a tu correo');
        setTimeout(() => navigate('/login'), 3000);
      } else {
        setMessage('Error al enviar el enlace');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Error de conexión');
    }
  };

  return (
    <div className="principal">
      <div className="reset-container">
        <img className="imageReset" src="public/LogoUPBibGOD2.png" alt="Logo" />
        <form onSubmit={handleSubmit}>
            <h2>Recuperar Contraseña</h2>
            <input
            type="email"
            placeholder="Correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            />
         <button className ="enviar" type="submit">Enviar enlace</button>
         {message && <p className="message">{message}</p>}
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;