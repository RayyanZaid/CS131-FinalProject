import React from "react";
import NavBar from "./components/NavBar";
import MainRoutes from "./MainRoutes"; // Make sure this path is correct
import { BrowserRouter as Router } from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <MainRoutes />
      </div>
    </Router>
  );
}

export default App;
