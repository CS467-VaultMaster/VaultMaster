import React from "react";
import { useNavigate } from "react-router-dom";

export default function MFAVerification({ setIsAuthenticated }) {
  const [mfaToken, setMfaToken] = useState("")
  const navigate = useNavigate();

  const handleSubmit = () => {
    setIsAuthenticated(true);
    //
    // Put POST request to API here
    //
    navigate("/vault");
  };

  return (
    <div className="mfa-page">
      <h2>MFA Confirmation</h2>
      <form onSubmit={handleMFA}>
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
      <button onClick={handleSubmit}>MFA Good</button>
    </div>
  );
}
