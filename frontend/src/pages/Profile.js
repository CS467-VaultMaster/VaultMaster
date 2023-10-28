import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Profile({ handleLogout }) {
  const [userData, setUserData] = useState({
    username: "",
    password1: "",
    password2: "",
    first_name: "",
    last_name: "",
    email: "",
  });
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    // Fetch user data and update the userData state
    const fetchUserData = async () => {
      const token = sessionStorage.getItem("authToken");
      if (!token) {
        setErrorMessage("No token found!");
        return;
      }
      const headers = { Authorization: `Bearer ${token}` };
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/user/account`,
          { headers }
        );
        setUserData(response.data);
        console.log(response.data);
      } catch (error) {
        setErrorMessage("No token found!");
      }
    };

    fetchUserData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserData((prevData) => ({ ...prevData, [name]: value })); // Destructure and update proper userData value
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();

    const { password1, password2 } = userData;
    if (password1 !== password2) {
      setErrorMessage("Passwords do not match!");
      setUserData((prevData) => ({ ...prevData, password1: "", password2: "" }));
      return;
    }

    const token = sessionStorage.getItem("authToken");
    if (!token) {
      console.error("No token found.");
      return;
    }

    const headers = {
      Authorization: `Bearer ${token}`,
    };

    try {
      await axios.put(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/user/account`,
        userData,
        { headers }
      );
      setSuccessMessage("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  const handleDelete = async () => {
    const isConfirmed = window.confirm(
      "Are you sure you want to permanently delete your profile?"
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
        handleLogout();
      } catch (error) {
        console.error("Error deleting the account:", error);
      }
    }
  };

  return (
    <div className="profile">
      <h2>User Profile</h2>
      {errorMessage && <p className="error">{errorMessage}</p>}
      <form onSubmit={handleProfileUpdate}>
        <div>
          <label>First Name:</label>
          <input
            type="text"
            name="first_name"
            value={userData.first_name}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            name="last_name"
            value={userData.last_name}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={userData.username}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={userData.email}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password1"
            value={userData.password1}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Confirm Password:</label>
          <input
            type="password"
            name="password2"
            value={userData.password2}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit">Update Profile</button>
      </form>
      <button onClick={handleDelete}>Delete Profile</button>
      {successMessage && <p className="success">{successMessage}</p>}
    </div>
  );
}
