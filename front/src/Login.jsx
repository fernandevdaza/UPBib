import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";
import { Link } from "react-router-dom";
import api from "./utils/api.js";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
    const response = await api.post('/auth/login', {
      email,
      password
    });

      sessionStorage.setItem('access_token', response.data.access_token);

      navigate("/main");
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="login-container">
      
      <img className="imageLogin" src="public/LogoUPBibGOD2.png" alt="Logo Login" />

      <div className="all">
        <form onSubmit={handleLogin}>
          <div className="user">
              <input className="inputLogin"
                type="text"
                name="name"
                placeholder="Usuario"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
          </div>
          <div className="pass">
              <input className="inputLogin"
                type="password"
                name="contrasenia"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
          </div>
          <button className="validar" type="submit">Acceder</button>
          <div className="reset-link">
              <a href="/reset-password">¿Olvidaste tu contraseña?</a>
          </div>
          <div className="divider">
            <span>o</span>
          </div>
          <button
              type="button"
              className="crear-cuenta"
              onClick={() => navigate('/registro')}
          >Crear cuenta
          </button>
        </form>

      </div>
    </div>
  );
};

export default Login;
