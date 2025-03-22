import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${process.env.VITE_BACKEND_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Error de autenticación");
      }

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);

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
            <label>
              Usuario:
              <input
                type="text"
                name="name"
                placeholder="Usuario"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
