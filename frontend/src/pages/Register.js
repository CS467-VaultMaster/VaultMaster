import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import GeneratePassword from "../components/GeneratePassword";
import { passwordComplexity, hasPasswordBeenPwned } from "../utilities/passwordUtils";
import { QRCodeSVG } from "qrcode.react";
import axios from "axios";

export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("HomerSimpson");
  const [password1, setPassword1] = useState("goodpassword321");
  const [password2, setPassword2] = useState("goodpassword321");
  const [email, setEmail] = useState("homer@email.com");
  const [firstName, setFirstName] = useState("Homer");
  const [lastName, setLastName] = useState("Simpson");
  const [passwordError, setPasswordError] = useState("");
  const [generalError, setGeneralError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [otpUri, setOtpUri] = useState("");

  const isValidEmail = (email) => {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(email);
  };

  const handleLogin = () => {
    navigate("/login")
  }

  const handleRegistration = async (e) => {
    setGeneralError("");
    setPasswordError("");
    e.preventDefault();

    if (password1 !== password2) {
      setPasswordError("Passwords do not match!");
      setPassword2(""); // Clear password2 field
      return;
    }

    if (!passwordComplexity(password1)) {
      setPasswordError("Password must be at least 8 characters long.");
      return;
    } else {
      const isPwnd = await hasPasswordBeenPwned(password1);
      if (isPwnd) {
        setPasswordError(
          "This password has appeared in a breach. Please pick a stronger one."
        );
        setPassword1("");
        setPassword2("");
        return;
      }
    }

    if (!isValidEmail(email)) {
      setGeneralError("Please enter a valid email address.");
      return;
    }

    setPasswordError(""); // Reset password error and proceed with registration
    setGeneralError("");

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
        setOtpUri(response.data.otp_uri);
        setGeneralError("");
        setPasswordError("");
        setSuccessMessage(
          "Registration successful! Please scan the QR code with your MFA app. This will be the only time this QR code is shown."
        );
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

  const handleQRConfirmation = () => {
    window.alert(
      "Please ensure you have scanned the QR code before proceeding. It will not be shown again."
    );
    navigate("/login");
  };

  return (
    <div className="register page">
      <h2>Register</h2>
      {successMessage && <p className="success">{successMessage}</p>}
      {generalError && <p className="error">{generalError}</p>}
      {successMessage && !otpUri && <p className="success">{successMessage}</p>}
      {!otpUri && (
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

          <div className="button-container">
            <button type="submit">Register</button>
            <button onClick={handleLogin}>Login</button>
          </div>
        </form>
      )}
      {otpUri && (
        <div>
          <QRCodeSVG value={otpUri} />
          <p>Scan this QR code with your MFA app and then click 'OK'</p>
          <button onClick={handleQRConfirmation}>OK</button>
        </div>
      )}
    </div>
  );
}
