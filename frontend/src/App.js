import React, { useState, useEffect } from "react";
import { Route, Routes, Navigate, useNavigate } from "react-router-dom";
import Navigation from "./components/Navigation";
import VaultDashboard from "./pages/VaultDashboard";
import Login from "./pages/Login";
import Tools from "./pages/Tools";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import MFAVerification from "./pages/MFAVerification";

// FastAPI endpoint URL, defined so that you can run React either locally or in the container w/o issues.
// Looked into how best to pass this - useContext()? set the value on window? - but I'll let you pick. (- Will)
export const FASTAPI_BASE_URL =
  process.env.REACT_APP_FASTAPI_URL;

function PrivateRoute({ children, isAuthenticated, isGoodPassword }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (!isAuthenticated && !isGoodPassword) {
      navigate("/login");
    }
  }, [isAuthenticated, isGoodPassword, navigate]); // Rerun this function when any of these things change (dependency array)

  return isAuthenticated || isGoodPassword ? children : null;
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Default to not authenticated
  const [isGoodPassword, setIsGoodPassword] = useState(false); // Intermediate authorization to trigger MFA page
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem("authToken");
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    sessionStorage.removeItem("authToken"); // Delete token from local storage
    setIsAuthenticated(false);
    navigate("/login");
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
          <Route
            path="/login"
            element={
              <Login
                setIsAuthenticated={setIsAuthenticated}
                setIsGoodPassword={setIsGoodPassword}
              />
            }
          />
          <Route
            path="/tools"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>{<Tools />}</PrivateRoute>
            }
          />
          <Route
            path="/vault"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                {<VaultDashboard />}
              </PrivateRoute>
            }
          />
          <Route
            path="/mfa"
            element={
              <PrivateRoute isGoodPassword={isGoodPassword}>
                {<MFAVerification setIsAuthenticated={setIsAuthenticated} />}
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                {<Profile handleLogout={handleLogout} />}
              </PrivateRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
