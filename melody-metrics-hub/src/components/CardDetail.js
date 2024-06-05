import React from "react";
import "./CardDetail.css"; // Make sure your CSS path is correct

function CardDetail({ card, onBack }) {
  if (!card) return null;

  return (
    <div className="card-detail-container">
      <h1 className="card-title">{card.name}</h1>
      <p className="card-grade">Posture Grade: {card.postureGrade}%</p>
      <p className="card-grade">Music Grade: {card.musicGrade}%</p>
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

        <div className="music-feedback-container">
          {card.musicFeedbackArray &&
            card.musicFeedbackArray.map((feedback, idx) => (
              <div
                key={idx}
                className={`feedback-note-box ${
                  feedback.rhythm_correctness && feedback.tone === "In tune"
                    ? "correct-feedback"
                    : "incorrect-feedback"
                }`}
              >
                <div>{feedback.note}</div>
                <div className="feedback-details">
                  Rhythm:{" "}
                  {feedback.rhythm_correctness ? "Correct" : "Incorrect"}
                  <br />
                  Tone: {feedback.tone}
                </div>
              </div>
            ))}
        </div>
      </div>
      <button className="back-button" onClick={onBack}>
        Back to Test Cards
      </button>
    </div>
  );
}

export default CardDetail;
