import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Profile() {
  const [userData, setUserData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
  });
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState("");

  // useEffect(() => {
  //   const fetchedData = {
  //     ...
  //   }
  // })

  const handleDelete = async () => {
    const isConfirmed = window.confirm(
      "Are you sure you want to permanently delete your account?"
    );

    if (isConfirmed) {
      const token = sessionStorage.getItem("authToken");

      if (!token) {
        console.error("Token not found!");
        return;
      }

      const headers = {
        Authorization: `Bearer ${token}`,
      };

      try {
        const response = await axios.delete(
          `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/user/account`,
          { headers }
        );
        sessionStorage.removeItem("authToken");
        setSuccessMessage("Account successfully deleted. Redirecting to /login...")
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } catch (error) {
        console.error("Error deleting the account:", error);
      }
    }
  };

  return (
    <div className="profile">
      <h2>User Profile</h2>
      {successMessage && <p className="success">{successMessage}</p>}
      <button onClick={handleDelete}>Delete Profile</button>
    </div>
  );
}
