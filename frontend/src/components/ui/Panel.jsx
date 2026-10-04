import React from "react";

export default function Panel({
  title,
  kicker,
  children,
  className = "",
}) {
  return (
    <section className={`panel ${className}`}>
      {(title || kicker) && (
        <header className="panel-header">
          <div>
            {kicker && (
              <span className="panel-kicker">
                {kicker}
              </span>
            )}

            {title && <h2>{title}</h2>}
          </div>
        </header>
      )}

      {children}
    </section>
  );
}
