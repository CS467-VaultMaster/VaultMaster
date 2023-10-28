import React, { useState, useEffect } from "react";
import { Route, Routes, Link, Navigate, useNavigate } from "react-router-dom";
import Navigation from "./components/Navigation";
import VaultDashboard from "./pages/VaultDashboard";
import Login from "./pages/Login";
import Tools from "./pages/Tools";
import Register from "./pages/Register";

// FastAPI endpoint URL, defined so that you can run React either locally or in the container w/o issues. 
// Looked into how best to pass this - useContext()? set the value on window? - but I'll let you pick. (- Will)
export const FASTAPI_BASE_URL = process.env.REACT_APP_FASTAPI_URL || "http://127.0.0.1:8000";

function PrivateRoute({ children, isAuthenticated }) {
  const navigate = useNavigate();
  // const isAuthenticated = true; // Just for now
  
  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);
  
  return isAuthenticated ? children : null;
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false); // For now
  const navigate = useNavigate();

  const handleLogout = () => {
    setIsAuthenticated(false);
    navigate("/login")
  };

  return (
    <div className="App">
      {/* {isAuthenticated && <Navigation onLogout={handleLogout} />} */}
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
