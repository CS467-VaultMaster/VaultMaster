import React, { useState } from "react";

export default function GeneratePassword() {
  const [generatedPassword, setGeneratedPassword] = useState("");

  const generatePassword = () => {
    const charset =
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&!@#$%^&*()";
    let password = "";
    for (let i = 0; i < 16; i++) {
      password += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    setGeneratedPassword(password);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedPassword);
  };

  return (
    <div className="password-generator-container">
      <div className="generate-button-container">
        <button type="button" onClick={generatePassword} className="generate-button">
          Generate Strong Password
        </button>
      </div>
      {generatedPassword && (
        <div className="password-display-card">
          <input
            type="text"
            value={generatedPassword}
            readOnly
            className="password-input"
          />
          <button type="button" onClick={copyToClipboard} className="clipboard-button">
            <i className="fas fa-clipboard" style={{ fontSize: "14px" }}></i>
          </button>
        </div>
      )}
    </div>
  );
}
