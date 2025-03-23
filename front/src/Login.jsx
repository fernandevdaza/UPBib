import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";
import { Link } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (username === "Usuario123" && password === "Contraseña123") {
      navigate("/main");
    } else {
      alert("Usuario o contraseña incorrectos.");
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
                value={username}
                onChange={(e) => setUsername(e.target.value)}
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
