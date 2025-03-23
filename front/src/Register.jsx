import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.firstName.trim() || !formData.lastName.trim()) {
      setError('Debe ingresar nombres y apellidos válidos');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    const dateRegex = /^\d{4}\/\d{2}\/\d{2}$/;
    if (!dateRegex.test(formData.birthDate)) {
      setError('Formato de fecha inválido. Use AAAA/MM/DD');
      return;
    }

    const codeRegex = /^\d{5,10}$/;
      if (!codeRegex.test(formData.upbCode)) {
      setError('Código UPB inválido (5-10 dígitos)');
  return;
}


    alert('¡Registro exitoso! Ahora puedes iniciar sesión');
    navigate('/');
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  return (
    <div className="login-container">
      <img className="imageLogin" src="public/LogoUPBibGOD2.png" alt="Logo Login" />
      <div className="all">
        <form onSubmit={handleSubmit}>
          <h2>Crear nueva cuenta</h2>

          <div className="form-group row">
            <div className="col">
              <input
                type="text"
                name="firstName"
                placeholder="Nombres"
                value={formData.firstName}
                onChange={handleChange}
                required
                pattern="[A-Za-zÁ-Úá-ú\s]{2,}"
              />
            </div>
            <div className="col">
              <input
                type="text"
                name="lastName"
                placeholder="Apellidos"
                value={formData.lastName}
                onChange={handleChange}
                required
                pattern="[A-Za-zÁ-Úá-ú\s]{2,}"
              />
            </div>
          </div>

          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Correo electrónico"
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="text"
              name="birthDate"
              placeholder="Fecha de nacimiento (AAAA/MM/DD)"
              value={formData.birthDate}
              onChange={handleChange}
              pattern="\d{4}/\d{2}/\d{2}"
              required
            />
          </div>

          <div className="form-group">
            <input
              type="number"
              name="upbCode"
              placeholder="Código UPB (5-10 dígitos)"
              value={formData.upbCode}
              onChange={handleChange}
              min="10000"
              max="9999999999"
              onKeyPress={(e) => {
              if (!/[0-9]/.test(e.key)) {
                e.preventDefault();
              }
              }}
              required
              />
            </div>

          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Contraseña"
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirmar contraseña"
              onChange={handleChange}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button className="validar" type="submit">Registrarse</button>

          <div className="login-link">
            <span>¿Ya tienes cuenta? </span>
            <Link to="/" className="link">Iniciar sesión</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;