import React, { useState } from "react";

function StartPracticing({ onSubmit }) {
  const [title, setTitle] = useState("");
  const [image, setImage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ title, image });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Start Practicing</h1>
      <label>
        Title:
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </label>
      <label>
        Image:
        <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default StartPracticing;
