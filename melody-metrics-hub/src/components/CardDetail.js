import React from "react";

function CardDetail({ card, onBack }) {
  if (!card) return null;

  return (
    <div>
      <h1>{card.name}</h1>
      <p>Grade: {card.postureGrade}</p>
      {card.postureFeedbackArray.map((feedback, idx) => (
        <div key={idx}>
          <img src={feedback.feedbackImage} alt={`Feedback ${idx + 1}`} />
          <p>{feedback.feedbackText}</p>
        </div>
      ))}
      <button onClick={onBack}>Back to Test Cards</button>
    </div>
  );
}

export default CardDetail;
