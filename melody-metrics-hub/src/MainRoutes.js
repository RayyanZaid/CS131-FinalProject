import React, { useState } from "react";
import StartPracticing from "./components/StartPracticing";
import Confirmation from "./components/Confirmation";
import TestCards from "./components/TestCards";
import CardDetail from "./components/CardDetail";
import { Routes, Route, useNavigate } from "react-router-dom";

function MainRoutes() {
  const [selectedCard, setSelectedCard] = useState(null);
  const navigate = useNavigate();

  const onCardClick = (card) => {
    setSelectedCard(card);
    navigate("/cardDetail");
  };

  const onBackCardClick = () => {
    navigate("/testcards");
  };

  return (
    <Routes>
      <Route path="/" element={<StartPracticing />} />
      <Route path="/confirmation" element={<Confirmation />} />
      <Route
        path="/testCards"
        element={<TestCards onCardClick={onCardClick} />}
      />
      <Route
        path="/cardDetail"
        element={<CardDetail card={selectedCard} onBack={onBackCardClick} />}
      />
    </Routes>
  );
}

export default MainRoutes;
