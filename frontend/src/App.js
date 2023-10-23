import React, { useState, useEffect } from "react";
import { Route, Routes, Link, Navigate, useNavigate } from "react-router-dom";
import Navigation from "./components/Navigation";
import VaultDashboard from "./pages/VaultDashboard";
import Login from "./pages/Login";
import Tools from "./pages/Tools";
import Register from "./pages/Register";

function PrivateRoute({ children, isAuthenticated }) {
  // const isAuthenticated = true; // Just for now

  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  return isAuthenticated ? children : null;
}

function App() {
  const [items, setItems] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(true); // For now

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <div className="App">
      {isAuthenticated && <Navigation onLogout={handleLogout} />}
      <header>
        <h1>VaultMaster</h1>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/vault" replace />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />

          <Route
            path="/vault"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                <VaultDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/tools"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                <Tools />
              </PrivateRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
