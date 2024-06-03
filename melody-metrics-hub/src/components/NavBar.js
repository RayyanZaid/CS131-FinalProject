import React from "react";

function NavBar({ onNavigate }) {
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
        <button onClick={() => onNavigate("start")}>Start Practicing</button>
        <button onClick={() => onNavigate("testCards")}>Test Cards</button>
      </div>
    </nav>
  );
}

export default NavBar;
