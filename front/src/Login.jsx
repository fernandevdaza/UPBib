import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

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
            <label>
              Usuario:
              <input
                type="text"
                name="name"
                placeholder="Usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>
          </div>
          <div className="pass">
            <label>
              Contraseña:
              <input
                type="password"
                name="contrasenia"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
          </div>
          <button className="validar" type="submit">Acceder</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
