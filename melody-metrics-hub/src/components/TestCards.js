import React, { useEffect, useState } from "react";
import { db, doc, getDoc } from "./firebaseConfig";

function TestCards({ onCardClick }) {
  const [testCards, setTestCards] = useState([]);

  useEffect(() => {
    const fetchTestCards = async () => {
      const docRef = doc(db, "users", "user1");
      const docSnap = await getDoc(docRef);

      if (docSnap.exists()) {
        const data = docSnap.data();
        const tests = data.tests.map((test) => ({
          name: test.name,
          postureGrade: test.postureGrade,
          postureFeedbackArray: test.postureFeedbackArray,
        }));

        // console.log(data.tests[0].postureFeedbackArray[0].feedbackText);

        setTestCards(tests);
      } else {
        console.log("No such document!");
      }
    };

    fetchTestCards();
  }, []);

  return (
    <div>
      <h1>Test Cards</h1>
      <div style={{ overflowY: "scroll", maxHeight: "80vh" }}>
        {testCards.map((card, index) => (
          <div key={index} onClick={() => onCardClick(card)}>
            <h2>{card.name}</h2>
            <p>Grade: {card.postureGrade}</p>
            {card.postureFeedbackArray.map((feedback, idx) => (
              <div key={idx}>
                <img
                  src={feedback[0]}
                  alt={`Feedback ${idx + 1}`}
                  style={{ width: "100px", height: "100px" }}
                />
                <p>{feedback[1]}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default TestCards;
