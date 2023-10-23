import React from "react";
import { Link, useNavigate } from "react-router-dom"

export default function Navigation({onLogout}) {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Delete session cookies or whatever we need to do to logout
    onLogout()
    navigate("/login")
  }

  return (
    <div className="navigation">
      <nav>
        <Link to="/vault">Vault</Link>
        <Link to="/tools">Tools</Link>
        <Link to="/profile">Profile</Link>
        <button onClick={handleLogout}>Logout</button>
        {/* Add a logout button to delete cookies and whatever else? */}
      </nav>
    </div>
  );
}
