import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await axios.post(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/user/login`,
        formData.toString(),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      if (response.status === 200) {
        sessionStorage.setItem("authToken", response.data.access_token);
        setIsAuthenticated(true);
        navigate("/vault");
      }
    } catch (error) {
      console.log(error.response.data.detail);
      setPassword("");
      setUsername("");
      setLoginError(error.response.data.detail);
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      {loginError && <p className="error">{loginError}</p>}
      <form onSubmit={handleLogin}>
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Login</button>
      </form>

      <div className="login-link">
        <Link to="/register">Register</Link>
      </div>
    </div>
  );
}
