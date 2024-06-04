import React from "react";
import NavBar from "./components/NavBar";
import StartPracticing from "./components/StartPracticing";
import Confirmation from "./components/Confirmation";
import TestCards from "./components/TestCards";
import CardDetail from "./components/CardDetail";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

// Your existing routes and server setup

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path="/" element={<StartPracticing />} />
          <Route path="/confirmation" element={<Confirmation />} />

          <Route path="/testCards" element={<TestCards />} />
          <Route path="/cardDetail" element={<CardDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
