import React, { useState, useEffect } from "react";
import Navigation from "../components/Navigation";
import axios from "axios";

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
    try {
      setErrorMessage("");
      console.log(`Password: ${password}`)
      // Getting a 401 for some reason even with the correct password
      const response = await axios.put(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/vault/open`,
        {
          password: password,
        }
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
          {credentials.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Nickname</th>
                  <th>URL</th>
                  <th>Password</th>
                  <th>Category</th>
                </tr>
              </thead>
              <tbody>
                {credentials.map((credential) => (
                  <tr key={credential.id}>
                    <td>{credential.nickname}</td>
                    <td>{credential.url}</td>
                    <td>{credential.password}</td>
                    <td>{credential.category}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No credentials found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default VaultDashboard;
