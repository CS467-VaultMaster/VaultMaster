import React, { useState } from "react";
import axios from "axios";

export default function AddCredential() {
  const [credential, setCredential] = useState({
    nickname: "",
    category: "",
    url: "",
    password: "",
    note: "",
  });
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredential({ ...credential, [name]: value });
  };

  const handleSubmit = async (e) => {
    try {
      const token = sessionStorage.getItem("authToken");

      if (!token) {
        setErrorMessage("No authentication token found.");
        return;
      }

      const response = await axios.post(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/vault`,
        credential,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        setSuccessMessage("Credential added successfully!");
        setCredential({
          nickname: "",
          category: "",
          url: "",
          password: "",
          note: "",
        });
      } else {
        setErrorMessage("Failed to add credential.");
      }
    } catch (error) {
      console.error("Error adding credential:", error);
      setErrorMessage("An error occurred while adding the credential.");
    }
  };

  return <div>AddCredential</div>;
}
