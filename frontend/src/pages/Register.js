import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import GeneratePassword from "../components/GeneratePassword";
import axios from "axios";

export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [generalError, setGeneralError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const isValidEmail = (email) => {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(email);
  };

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

    if (password1 !== password2) {
      setPasswordError("Passwords do not match!");
      setPassword2(""); // Clear password2 field
      return;
    }

    if (!isValidEmail(email)) {
      setGeneralError("Please enter a valid email address.");
      return;
    }

    const pwdError = checkPasswordComplexity(password1);
    if (pwdError) {
      setPasswordError(pwdError);
      return;
    }

    setPasswordError(""); // Reset password error and proceed with registration

    try {
      const response = await axios.post("http://localhost:3000/", {
        username: username,
        password1: password1,
        password2: password2,
        email: email,
        first_name: firstName,
        last_name: lastName,
      });

      if (response.data.success) {
        setSuccessMessage("Registration successful! Redirecting to login...");
        setTimeout(() => {
          navigate("/login");
        }, 2000);
        console.log(response.data);
      } else {
        setGeneralError(
          response.data.message || "An error occurred during registration."
        );
      }
    } catch (error) {
      const errorMessage =
        error.response && error.response.data && error.response.data.message
          ? error.response.data.message
          : "Error registering user. Please try again.";
      setGeneralError(errorMessage);
      console.error("Error registering user:", error.response);
    }
  };

  return (
    <div className="register page">
      <h2>Register</h2>
      {successMessage && <p className="success">{successMessage}</p>}{" "}
      {/* Display success message to user */}
      <form onSubmit={handleRegistration}>
        <div className="input-group">
          <label htmlFor="firstName">First Name</label>
          <input
            type="text"
            id="firstName"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="lastName">Last Name</label>
          <input
            type="text"
            id="lastName"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
        </div>

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
          <label htmlFor="password1">Password</label>
          <input
            type="password"
            id="password1"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            required
          />
          <GeneratePassword />
          {passwordError && <p className="error">{passwordError}</p>}
        </div>

        <div className="input-group">
          <label htmlFor="password2">Confirm Password</label>
          <input
            type="password"
            id="password2"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            required
          />
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

        <button type="submit">Register</button>
      </form>
    </div>
  );
}
