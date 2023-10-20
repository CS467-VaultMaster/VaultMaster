import React, { useState } from "react";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const checkPasswordComplexity = (pwd) => {
    if (pwd.length < 8) {
      return "Password must be at least 8 characters long.";
    }

    // Can add other complexity requirements here
    // May want to check against a list of poor passwords as well
    return "";
  };

  const handleRegistration = (e) => {
    e.preventDefault();

    const pwdError = checkPasswordComplexity(password);
    if (pwdError) {
      setPasswordError(pwdError);
      return;
    }

    setPasswordError('')  // Reset password error and proceed with registration

    console.log(`Registering user with:
      username: ${username},
      password: ${password},
      email: ${email},
      phone: ${phoneNumber}`);
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
