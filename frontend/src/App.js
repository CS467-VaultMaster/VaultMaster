import React, { useState, useEffect } from "react";
import { Route, Routes, Link, Navigate } from "react-router-dom";
import Navigation from "./components/Navigation";
import VaultDashboard from "./pages/VaultDashboard";
import Login from "./pages/Login";
import Tools from "./pages/Tools";
import Register from "./pages/Register";

function PrivateRoute({ children, ...rest }) {
  const isAuthenticated = true; // Just for now

  if (isAuthenticated) {
    return children;
  }

  return <Navigate to="/login" replace />
}

function App() {
  const [items, setItems] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(true)  // For now

  const handleLogout = () => {
    setIsAuthenticated(false)
  }

  return (
    <div className="App">
      {isAuthenticated && <Navigation onLogout={handleLogout}/>}
      <header>
        <h1>VaultMaster</h1>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/vault" replace />} />
          {/* Replace - new location replaces current entry to back button nav still works */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          <PrivateRoute path="/vault" element={<VaultDashboard />} />
          <PrivateRoute path="/tools" element={<Tools />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
