import React, { useState, useEffect } from "react";
import axios from "axios";

export default function ExportPasswords() {
  const [credentials, setCredentials] = useState([]);

  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = async () => {
    try {
      const token = sessionStorage.getItem("authToken");
      if (!token) {
        console.error("No authentication token found.");
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
      setCredentials(response.data);
    } catch (error) {
      console.error("Error fetching credentials:", error);
    }
  };

  const handleExport = () => {
    const confirmExport = window.confirm(
        "Warning: The exported file will contain all passwords in plain text. Do you want to proceed?"
    )
    if (confirmExport){
        // Creates a temporary download link, triggers the download, then cleans it up
        const blob = new Blob([JSON.stringify(credentials, null, 2)], {
          type: "application/json",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "vaultmaster-credentials.json";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="export-passswords">
      <button onClick={handleExport}>Export Credentials</button>
    </div>
  );
}
