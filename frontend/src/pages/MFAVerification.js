import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuthToken } from "../utilities/passwordUtils";
import axios from "axios";

export default function MFAVerification({ setIsAuthenticated }) {
  const [mfaToken, setMfaToken] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const token = getAuthToken();
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      const response = await axios.get(
        `${process.env.REACT_APP_FASTAPI_URL}/otp_verify/${mfaToken}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        setIsAuthenticated(true);
        navigate("/vault");
      } else {
        console.error("MFA verification failed.");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="mfa-page">
      <h2>MFA Confirmation</h2>
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
      </form>
      <button type="submit">Verify</button>
    </div>
  );
}
