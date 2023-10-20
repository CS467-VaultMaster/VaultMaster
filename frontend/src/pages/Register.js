import React, { useState } from "react";
import { useNavigate } from "react-router-dom"
import GeneratePassword from "../components/GeneratePassword";
import axios from 'axios'

export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const checkPasswordComplexity = (pwd) => {
    // TODO enhance this function with special char requirements, etc.
    if (pwd.length < 8) {
      return "Password must be at least 8 characters long.";
    }
    // May want to check against a list of poor passwords as well
    return "";
  };

  const handleRegistration = async (e) => {
    e.preventDefault();

    const pwdError = checkPasswordComplexity(password);
    if (pwdError) {
      setPasswordError(pwdError);
      return;
    }

    setPasswordError('')  // Reset password error and proceed with registration

    try {
      const response = await axios.post("ENDPOINT",{
        username: username,
        password: password,
        email: email,
        phone_number: phoneNumber
      });

      if (response.data.success){
        console.log(response.data)
        navigate('/login')
      }

    } catch (error) {
      console.error("Error registering user:", error.response)
      // Also display error message to the user
    }
  };

  return (
    <div className="register page">
      <h2>Register</h2>
      <form onSubmit={handleRegistration}>
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
          <GeneratePassword />
          {passwordError && <p className="error">{passwordError}</p>}
        </div>

        <div className="input-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="phoneNumber">Phone Number</label>
          <input
            type="tel"
            id="phoneNumber"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
        </div>

        <button type="submit">Register</button>
      </form>
    </div>
  );
}
