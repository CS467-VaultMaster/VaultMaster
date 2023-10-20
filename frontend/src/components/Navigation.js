import React from "react";
import { Link } from "react-router-dom"

export default function Navigation() {
  return (
    <div className="App-nav">
      <nav>
        <Link to="/vault">Vault</Link>
        <Link to="/tools">Tools</Link>
        <Link to="/profile">Profile</Link>
      </nav>
    </div>
  );
}
