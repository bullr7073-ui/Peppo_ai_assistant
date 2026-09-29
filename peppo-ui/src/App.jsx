import { useState } from "react";
import "./App.css";
import Orb from "./components/Orb";

function App() {
  const [isListening, setIsListening] = useState(false);

  const handleOrbClick = () => {
    setIsListening(true);
  };

  const stopListening = () => {
    setIsListening(false);
  };

  return (
    <main className="peppo-app">

      {/* Peppo Orb */}
      <button
        className="orb-button"
        onClick={handleOrbClick}
        aria-label="Speak to Peppo"
      >
        <Orb />
      </button>

      {/* Idle state */}
      {!isListening && (
        <p className="tap-text">
          TAP TO SPEAK !
        </p>
      )}

      {/* Listening state */}
      {isListening && (
        <div className="listening-ui">

          <p className="listening-text">
            Listening...
          </p>

          <button
            className="stop-button"
            onClick={stopListening}
            aria-label="Stop listening"
          >
            ×
          </button>

        </div>
      )}

    </main>
  );
}

export default App;