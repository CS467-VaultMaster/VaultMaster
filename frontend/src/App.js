import React, { useState, useEffect } from "react";
import { Route, Routes, Router, Link } from "react-router-dom";
import Navigation from "./components/Navigation";
import VaultDashboard from "./pages/VaultDashboard";
import Login from "./pages/Login";
import Tools from "./pages/Tools";
import Register from "./pages/Register";

function App() {
  const [items, setItems] = useState([]);

  //   useEffect(() => {
  //     console.log("Starting the fetch operation...");

  //     fetch(`${process.env.REACT_APP_FASTAPI_URL || "http://127.0.0.1:8000"}/items/`)
  //       .then((response) => {
  //         console.log("Received the response:", response);
  //         return response.json();
  //       })
  //       .then((data) => {
  //         console.log("Parsed JSON data:", data);
  //         setItems(data);
  //       })
  //       .catch((error) => {
  //         console.error("Error during the fetch operation:", error);
  //       });
  //   }, []);
  const isAuthenticated = false;

  return (
    <div className="App">
      {/* <Navigation /> */}
      <header>
        <h1>VaultMaster</h1>
      </header>
      <main>
        <Routes>
          {/* Default route for base URL */}
          <Route path="/" element={isAuthenticated ? <Link to="/vault" /> : <Login />} />

          {/* Registration Route */}
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route
            path="/login"
            element={isAuthenticated ? <Link to="/vault" /> : <Login />}
          />
          <Route
            path="/vault"
            element={isAuthenticated ? <VaultDashboard /> : <Link to="/login" />}
          />
          <Route
            path="/tools"
            element={isAuthenticated ? <Tools /> : <Link to="/login" />}
          />
          {/* Add similar routes for "/profile" and any other pages you have, ensuring they're protected */}
        </Routes>
      </main>
      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
