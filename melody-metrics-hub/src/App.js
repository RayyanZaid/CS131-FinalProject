import React, { useState } from "react";
import NavBar from "./components/NavBar";
import StartPracticing from "./components/StartPracticing";
import Confirmation from "./components/Confirmation";
import ImageDisplay from "./components/ImageDisplay";
import TestCards from "./components/TestCards";
import CardDetail from "./components/CardDetail";

function App() {
  const [screen, setScreen] = useState("start");
  const [formData, setFormData] = useState(null);
  const [selectedCard, setSelectedCard] = useState(null);

  const handleFormSubmit = (data) => {
    setFormData(data);
    setScreen("confirmation");
  };

  const handleCardClick = (card) => {
    setSelectedCard(card);
    setScreen("cardDetail");
  };

  const handleNavigate = (targetScreen) => {
    setScreen(targetScreen);
  };

  return (
    <div className="App">
      <NavBar onNavigate={handleNavigate} />
      {screen === "start" && <StartPracticing onSubmit={handleFormSubmit} />}
      {screen === "confirmation" && (
        <Confirmation
          data={formData}
          onConfirm={() => setScreen("imageDisplay")}
        />
      )}
      {screen === "imageDisplay" && (
        <ImageDisplay
          data={formData}
          onBack={() => setScreen("start")}
          onGoToTestCards={() => setScreen("testCards")}
        />
      )}
      {screen === "testCards" && <TestCards onCardClick={handleCardClick} />}
      {screen === "cardDetail" && (
        <CardDetail card={selectedCard} onBack={() => setScreen("testCards")} />
      )}
    </div>
  );
}

export default App;
