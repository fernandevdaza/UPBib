import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Register.css';
import api from "./utils/api.js";

const Register = () => {
   const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    birthDay: '',
    birthMonth: '',
    birthYear: '',
    upbCode: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('')
  const navigate = useNavigate();
  const isValidDate = (day, month, year) => {
    if (month < 1 || month > 12) return false;
    if (day < 1 || day > 31) return false;

    const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if ((year % 4 === 0 && month === 2) && day <= 29) return true;

    return day <= daysInMonth[month - 1];
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.firstName.trim() || !formData.lastName.trim()) {
      setError('Ingresa nombres y apellidos válidos');
      return;
    }

    const day = parseInt(formData.birthDay);
    const month = parseInt(formData.birthMonth);
    const year = parseInt(formData.birthYear);

    if (!isValidDate(day, month, year)) {
      setError('Fecha inválida');
      return;
    }

    if (!/^\d{5,10}$/.test(formData.upbCode)) {
      setError('Código UPB inválido (5-10 dígitos)');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    // Formatear fecha para el backend
    const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    try {
        const response = await api.post('/auth/register', {
            nombre: formData.firstName,
            apellido: formData.lastName,
            fecha_nacimiento: formattedDate,
            email: formData.email,
            password: formData.password,
            codigo_upb: formData.upbCode
        });

        sessionStorage.setItem('access_token', response.data.access_token);
        navigate('/main');
      } catch (error) {
        setError(error.message || 'Error al registrar el usuario');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  return (
    <div className="registro-container">
      <img className="imageRegister" src="public/LogoUPBibGOD2.png" alt="Logo Login" />
      <div className="allRegister">
        <form onSubmit={handleSubmit}>

          <div className="form-group row">
            <div className="col">
              <input className="inputRegister"
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
              <input className="inputRegister"
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
            <input className="inputRegister"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Correo electrónico"
              required
            />
          </div>
          <div className="form-group date-inputs">
          <input
            type="number"
            name="birthDay"
            placeholder="DD"
            min="1"
            max="31"
            value={formData.birthDay}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="birthMonth"
            placeholder="MM"
            min="1"
            max="12"
            value={formData.birthMonth}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="birthYear"
            placeholder="AAAA"
            min="1900"
            max={new Date().getFullYear()}
            value={formData.birthYear}
            onChange={handleChange}
            required
          />
        </div>

          <div className="form-group">
            <input className="inputRegister"
              type="number"
              name="upbCode"
              placeholder="Código UPB"
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
            <input className="inputRegister"
              type="password"
              name="password"
              placeholder="Contraseña"
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <input className="inputRegister"
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