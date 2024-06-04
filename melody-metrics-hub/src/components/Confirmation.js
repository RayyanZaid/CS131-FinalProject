// Confirmation.js
import React from "react";
import { useLocation } from "react-router-dom";

function Confirmation() {
  const location = useLocation();
  const data = location.state;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        textAlign: "center",
      }}
    >
      <h1>You are now practicing: {data.title}</h1>
      <img src={data.imageUrl} alt={data.title} style={{ maxWidth: "100%" }} />
      <h2>Tell the Nano "Play" to hear the rhythm</h2>
      <h2>Tell the Nano "Test" to test yourself on Music and Posture</h2>
    </div>
  );
}

export default Confirmation;
