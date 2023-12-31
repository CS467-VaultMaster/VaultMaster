import React, { useState, useEffect } from "react";
import axios from "axios";
import AddCredential from "../components/AddCredential";
import CredentialsTable from "../components/CredentialsTable";
import { hasPasswordBeenPwned, verifyToken } from "../utilities/passwordUtils";
import GeneratePassword from "../components/GeneratePassword";

function VaultDashboard() {
  const [credentials, setCredentials] = useState([]);
  const [password, setPassword] = useState("");
  const [isPwdVerified, setIsPwdVerified] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [hasPwnedPassword, setHasPwnedPassword] = useState(false);

  useEffect(() => {
    const isVerified = sessionStorage.getItem("isPwdVerified") === "true"
    if (isVerified) {
      setIsPwdVerified(true)
      fetchCredentials()
    }
  }, [])

  const handlePasswordSubmit = async (event) => {
    event.preventDefault();

    const token = verifyToken();
    if (!token) {
      return;
    }

    const headers = {
      Authorization: `Bearer ${token}`,
    };

    try {
      setErrorMessage("");
      const response = await axios.put(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/vault/open`,
        {
          password: password,
        },
        { headers }
      );
      if (response.status === 200) {
        setIsPwdVerified(true); // Save this in session storage to persist across pages
        sessionStorage.setItem("isPwdVerified", "true");
        fetchCredentials();
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
      const token = verifyToken();
      if (!token) {
        return;
      }

      const response = await axios.get(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Check passwords on fetch() to see if they've been Pwned
      const checkPasswordPwnedStatus = await Promise.all(
        response.data.map(async (credential) => {
          const isPwned = await hasPasswordBeenPwned(credential.password);
          return { ...credential, isPwned }; // Add breach status to each credential
        })
      );

      setCredentials(checkPasswordPwnedStatus);
      setHasPwnedPassword(checkPasswordPwnedStatus.some((cred) => cred.isPwned));
    } catch (error) {
      console.error("Error fetching credentials:", error);
    }
  };

  const handleAddCredential = () => {
    fetchCredentials();
  };

  const handleDeleteCredential = async (id) => {
    try {
      const token = verifyToken();
      if (!token) {
        return;
      }

      const response = await axios.delete(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 204) {
        fetchCredentials();
      }
    } catch (error) {
      console.error("Error deleting credential:", error);
    }
  };

  return (
    <div className="vault-dashboard">
      <h2>Vault Dashboard</h2>
      {!sessionStorage.getItem("isPwdVerified") ? (
        <form onSubmit={handlePasswordSubmit}>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="submit">Verify</button>
          {errorMessage && <p style={{ color: "darkred" }}>{errorMessage}</p>}
        </form>
      ) : (
        <div>
          <AddCredential onAdd={handleAddCredential} />
          <GeneratePassword />
          {hasPwnedPassword && (
            <p className="warning-message">
              Warning: One or more of your passwords may have been exposed in a data
              breach. It is recommended to change them.
            </p>
          )}
          <CredentialsTable
            credentials={credentials}
            onDelete={handleDeleteCredential}
            fetchCredentials={fetchCredentials}
          />
        </div>
      )}
    </div>
  );
}

export default VaultDashboard;
