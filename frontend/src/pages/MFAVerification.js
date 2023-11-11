import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyToken } from "../utilities/passwordUtils";
import axios from "axios";

export default function MFAVerification({ setIsAuthenticated }) {
  const [mfaToken, setMfaToken] = useState("");
  const [mfaError, setMfaError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMfaError("");

    try {
      const token = verifyToken();
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      const response = await axios.get(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/user/otp_verify/${mfaToken}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        setIsAuthenticated(true);
        setMfaError("");
        navigate("/vault");
      } else {
        setMfaToken("");
        setMfaError("Invalid MFA token.");
      }
    } catch (error) {
      console.error(error);
      setMfaToken("")
      setMfaError("Invalid MFA token.");
    }
  };

  return (
    <div className="mfa-page">
      <h2>MFA Confirmation</h2>
      {mfaError && <p className="error">{mfaError}</p>}
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="MFA-token">MFA Token</label>
          <input
            type="text"
            id="mfaToken"
            value={mfaToken}
            onChange={(e) => setMfaToken(e.target.value)}
            required
          />
        </div>
        <button type="submit">Verify</button>
      </form>
    </div>
  );
}
