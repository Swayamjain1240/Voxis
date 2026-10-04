import React from "react";

export default function Transcript({
  messages = [],
}) {
  if (!messages.length) {
    return (
      <div className="transcript empty">
        Conversation transcript is empty.
      </div>
    );
  }

  return (
    <div className="transcript">
      {messages.map((message) => (
        <article
          key={message.id}
          className={`transcript-message ${
            message.source || "system"
          }`}
        >
          <span>
            {(message.source || "system").toUpperCase()}
          </span>

          <p>{message.text}</p>
        </article>
      ))}
    </div>
  );
}
