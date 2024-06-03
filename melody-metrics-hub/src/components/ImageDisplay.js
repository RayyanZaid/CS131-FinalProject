import React from "react";

function ImageDisplay({ data, onBack, onGoToTestCards }) {
  if (!data) return null;

  const imageUrl = URL.createObjectURL(data.image);

  return (
    <div>
      <h1>{data.title}</h1>
      <img src={imageUrl} alt={data.title} style={{ maxWidth: "100%" }} />
    </div>
  );
}

export default ImageDisplay;
