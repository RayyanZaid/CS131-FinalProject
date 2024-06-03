import React from "react";

function Confirmation({ data, onConfirm }) {
  return (
    <div>
      <h1>Confirmation</h1>
      <p>Your data has been submitted:</p>
      <p>Title: {data.title}</p>
      <p>Image: {data.image.name}</p>
      <button onClick={onConfirm}>View Image</button>
    </div>
  );
}

export default Confirmation;
