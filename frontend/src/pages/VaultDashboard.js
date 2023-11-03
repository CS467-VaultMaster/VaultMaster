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
        fetchCredentials();
        setTimeout(() => {
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
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential`,
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

  const handleAddCredential = (newCredential) => {
    setCredentials(prevCredentials => [...prevCredentials, newCredential])
  }

  const handleEditCredential = (index) => {
    // logic to handle editing a credential
    console.log("Edit credential at index:", index);
  };

  const handleDeleteCredential = async (id) => {
    try {
      const token = sessionStorage.getItem('authToken');
      if (!token) {
        console.error('No authentication token found.');
        return;
      }
  
      // Make DELETE request to API endpoint
      const response = await axios.delete(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
  
      // If the DELETE operation was successful, remove the credential from the local state
      if (response.status === 204) { // Check for successful response status
        const updatedCredentials = credentials.filter(credential => credential.id !== id);
        setCredentials(updatedCredentials);
        console.log("Deleted credential with ID:", id);
      }
    } catch (error) {
      console.error('Error deleting credential:', error);
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
          <AddCredential onAdd={handleAddCredential} />
          <CredentialsTable
            credentials={credentials}
            onEdit={handleEditCredential}
            onDelete={handleDeleteCredential}
          />
        </div>
      )}
    </div>
  );
}

export default VaultDashboard;
