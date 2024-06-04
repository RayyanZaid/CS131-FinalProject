// StartPracticing.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function StartPracticing() {
  const [title, setTitle] = useState("");
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("title", title);
    formData.append("image", image);

    try {
      const response = await fetch("http://192.168.4.45:5000/submit", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
      const imageUrl = URL.createObjectURL(image);
      navigate("/confirmation", { state: { title, imageUrl } });
    } catch (error) {
      console.error("Error submitting data:", error);
    }
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
