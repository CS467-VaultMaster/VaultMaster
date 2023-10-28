import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import GeneratePassword from "../components/GeneratePassword";
import axios from "axios";

export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("HomerJSimpson");
  const [password1, setPassword1] = useState("password123");
  const [password2, setPassword2] = useState("password123");
  const [email, setEmail] = useState("homer@email.com");
  const [firstName, setFirstName] = useState("Homer");
  const [lastName, setLastName] = useState("Simpson");
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
      const response = await axios.post(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/user/register`,
        {
          username: username,
          password1: password1,
          password2: password2,
          first_name: firstName,
          last_name: lastName,
          email: email,
        }
      );

      if (response.status === 200) {
        console.log(response.data);
        setSuccessMessage("Registration successful! Redirecting to login...");
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setGeneralError(
          response.data.message || "An error occurred during registration."
        );
      }
    } catch (error) {
      let errorMessage = "Error registering user. Please try again.";

      if (error.response) {
        if (error.response.status === 409) {
          errorMessage = "This user already exists.";
        } else if (error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        }
      }
      setGeneralError(errorMessage);
      console.error("Error registering user:", error.response);
    }
  };

  return (
    <div className="register page">
      <h2>Register</h2>
      {successMessage && <p className="success">{successMessage}</p>}
      {generalError && <p className="error">{generalError}</p>}
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

        <div className="register-link">
          <Link to="/login">Login</Link>
        </div>
      </form>
    </div>
  );
}
