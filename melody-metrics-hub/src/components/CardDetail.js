import React from "react";
import "./CardDetail.css"; // Importing CSS for styling

function CardDetail({ card, onBack }) {
  if (!card) return null;

  const printMusicArray = () => {
    console.log(card);
  };
  return (
    <div className="card-detail-container">
      <h1 className="card-title">{card.name}</h1>
      <p className="card-grade">Posture Grade: {card.postureGrade}</p>
      <p className="card-grade">Music Grade: {card.musicGrade}</p>
      <div className="feedback-container">
        {card.postureFeedbackArray.map((feedback, idx) => (
          <div className="feedback-item" key={idx}>
            <img
              src={feedback.feedbackImage}
              alt={`Feedback ${idx + 1}`}
              className="feedback-image"
            />
            <p className="feedback-text">{feedback.feedbackText}</p>
          </div>
        ))}

        {/* {card.musicFeedbackArray.map((feedback, idx) => (
          <div className="feedback-item" key={idx}>
            <img
              src={feedback.feedbackImage}
              alt={`Feedback ${idx + 1}`}
              className="feedback-image"
            />
            <p className="feedback-text">{feedback.note}</p>
          </div>
        ))} */}
      </div>
      <button className="back-button" onClick={onBack}>
        Back to Test Cards
      </button>

      <button className="back-button" onClick={printMusicArray}>
        Test
      </button>
    </div>
  );
}

export default CardDetail;
