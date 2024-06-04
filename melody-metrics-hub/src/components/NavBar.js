// NavBar.js
import React from "react";
import { Link } from "react-router-dom";

function NavBar() {
  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "10px",
        backgroundColor: "#ccc",
      }}
    >
      <div>
        <Link to="/">Start Practicing</Link>
        <a href="/testCards" target="_blank" rel="noopener noreferrer">
          Test Cards
        </a>
      </div>
    </nav>
  );
}

export default NavBar;
