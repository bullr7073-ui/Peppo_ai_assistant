import { useEffect, useState } from "react";
import "./PeppoAssistant.css";
import sampleResponseImage from "./sample-response.svg";

const defaultResponse = {
  eyebrow: "Peppo says",
  title: "Here is what I found.",
  description:
    "This is the glassmorphism response area. Your backend can replace this image, heading, and description with the assistant result.",
  imageUrl: sampleResponseImage,
  imageAlt: "Warm abstract illustration for Peppo's response",
};

export default function PeppoAssistant({
  response = defaultResponse,
  onStartListening,
  onEndListening,
  mockResponseDelay = 1200,
}) {
  const [state, setState] = useState("idle");

  useEffect(() => {
    if (state !== "listening") return undefined;

    const timer = window.setTimeout(() => {
      setState("responding");
    }, mockResponseDelay);

    return () => window.clearTimeout(timer);
  }, [state, mockResponseDelay]);

  function startVoiceFlow() {
    setState("listening");
    onStartListening?.();
  }

  function endVoiceFlow() {
    setState("idle");
    onEndListening?.();
  }

  return (
    <main className="peppo-stage" data-state={state}>
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <section className="assistant-layout" aria-label="Peppo voice assistant">
        <div className="peppo-zone">
          <button
            className="orb-button"
            type="button"
            aria-label="Tap Peppo to speak"
            onClick={startVoiceFlow}
          >
            <span className="orb">
              <span className="orb-layer orb-sheen" />
              <span className="orb-layer orb-upper" />
              <span className="orb-layer orb-golden" />
              <span className="orb-layer orb-apricot" />
              <span className="orb-layer orb-sunset" />
              <span className="orb-layer orb-mesh" />
              <span className="eye eye-left" />
              <span className="eye eye-right" />
            </span>
          </button>

          <p className="tap-copy">TAP TO SPEAK !</p>

          <button
            className="end-button"
            type="button"
            aria-label="End voice session"
            onClick={endVoiceFlow}
          />
        </div>

        <article
          className="response-panel"
          aria-live="polite"
          aria-label="Peppo response"
        >
          <div className="response-media">
            <img src={response.imageUrl} alt={response.imageAlt || ""} />
          </div>
          <div className="response-copy">
            <p className="eyebrow">{response.eyebrow}</p>
            <h1>{response.title}</h1>
            <p>{response.description}</p>
          </div>
        </article>
      </section>
    </main>
  );
}
