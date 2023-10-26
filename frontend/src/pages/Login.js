import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL}/vaultmaster/user/login`,
        {
          username: username,
          password: password,
        }
      );

      console.log(response.data)

      if (response.data && response.data.token) {
        localStorage.setItem("authToken", response.data.token);
        navigate("/dashboard");
      } else {
        setLoginError("Authentication failed. Please check your credentials.");
      }
    } catch (error) {
      const errorMessage =
        error.response && error.response.data && error.response.data.detail
          ? error.response.data.detail
          : "Error logging in. Please try again.";
      setLoginError(errorMessage);
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

      <div className="login-links">
        <Link to="/register">Register</Link>
      </div>
    </div>
  );
}
