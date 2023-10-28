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
            {credentials.map(credential => (
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
  );
}

export default VaultDashboard;
