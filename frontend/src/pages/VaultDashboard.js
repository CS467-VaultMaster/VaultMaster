import React, { useState, useEffect } from "react";
import Navigation from "../components/Navigation";
import axios from "axios";

function VaultDashboard() {
  const [credentials, setCredentials] = useState([]);

  useEffect(() => {
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
    fetchCredentials();
  }, []);

  return (
    <div className="vault-dashboard">
      <h2>Dashboard</h2>
      <ul>
        {credentials.map((credential) => (
          <li key={credential.id}>
            <strong>Nickname:</strong> {credential.nickname}
            <br />
            <strong>URL:</strong> {credential.url}
            <br />
            <strong>Password:</strong> {credential.password}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default VaultDashboard;
