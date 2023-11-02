import React, { useState, useEffect } from "react";
// import Navigation from "../components/Navigation";
import axios from "axios";
import AddCredential from "../components/AddCredential";
import CredentialsTable from "../components/CredentialsTable";

function VaultDashboard() {
  const [credentials, setCredentials] = useState([]);
  const [password, setPassword] = useState("");
  const [isPwdVerified, setIsPwdVerified] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handlePasswordSubmit = async () => {
    const token = sessionStorage.getItem("authToken");

    if (!token) {
      console.error("Token not found!");
      return;
    }
    const headers = {
      Authorization: `Bearer ${token}`,
    };

    try {
      setErrorMessage("");
      console.log(`Password: ${password}`);
      // Need to provide token
      const response = await axios.put(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/vault/open`,
        {
          password: password,
        },
        { headers }
      );
      if (response.status === 200) {
        setIsPwdVerified(true);
        setSuccessMessage("Verification successful. Unlocking vault...");
        setTimeout(() => {
          fetchCredentials();
          setSuccessMessage("");
        }, 2000);
      } else {
        setErrorMessage("Incorrect password.");
      }
    } catch (error) {
      console.error("An error occured while verifying the password: ", error);
      setErrorMessage("An error occured while verifying the password.");
    }
  };

  const fetchCredentials = async () => {
    try {
      const token = sessionStorage.getItem("authToken");
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      const response = await axios.get(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/vault`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setCredentials(response.data);
    } catch (error) {
      console.error("Error fetching credentials:", error);
    }
  };

  return (
    <div className="vault-dashboard">
      <h2>Vault Dashboard</h2>
      {!isPwdVerified ? (
        <div>
          <label>
            Password:
            <input type="password" value={password} onChange={handlePasswordChange} />
          </label>
          <button onClick={handlePasswordSubmit}>Verify</button>
          {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
        </div>
      ) : (
        <div>
          {successMessage && <p>{successMessage}</p>}
          {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
          <AddCredential
            onAdd={(newCredential) => setCredentials([...credentials, newCredential])}
          />
          <CredentialsTable credentials={credentials} />
        </div>
      )}
    </div>
  );
}

export default VaultDashboard;
