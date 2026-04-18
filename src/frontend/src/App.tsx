import { useState } from "react"
import SplitForm from "./components/SplitForm"
import RecoverForm from "./components/RecoverForm"

type Mode = "split" | "recover"

export default function App() {
    const [mode, setMode] = useState<Mode>("split")

    return (
        <div className="app">
            <div className="page">
                <header className="page-header">
                    <h1>Secret Sharing</h1>
                    <p className="subtitle">
                        Split a secret into shares or recover it from shares through backend API
                    </p>
                </header>

                <div className="mode-switch">
                    <button
                        className={mode === "split" ? "mode-btn active" : "mode-btn"}
                        onClick={() => setMode("split")}
                        type="button"
                    >
                        Split
                    </button>

                    <button
                        className={mode === "recover" ? "mode-btn active" : "mode-btn"}
                        onClick={() => setMode("recover")}
                        type="button"
                    >
                        Recover
                    </button>
                </div>

                {mode === "split" ? <SplitForm /> : <RecoverForm />}
                <footer className="page-footer">
                    <a
                        className="footer-link"
                        href="https://github.com/Karimkhab/shamir-secret-dnp/"
                        target="_blank"
                        rel="noreferrer"
                    >
    <span className="footer-icon github-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.59 2 12.25c0 4.53 2.87 8.37 6.84 9.73.5.1.66-.22.66-.49 0-.24-.01-1.04-.01-1.88-2.78.62-3.37-1.21-3.37-1.21-.45-1.2-1.11-1.51-1.11-1.51-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.85.09-.67.35-1.12.64-1.38-2.22-.26-4.56-1.14-4.56-5.08 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.72 0 0 .84-.28 2.75 1.05A9.3 9.3 0 0 1 12 7.82c.85 0 1.71.12 2.51.36 1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.46.1 2.72.64.72 1.03 1.63 1.03 2.75 0 3.95-2.34 4.82-4.57 5.08.36.32.68.95.68 1.92 0 1.39-.01 2.5-.01 2.84 0 .27.17.59.67.49A10.27 10.27 0 0 0 22 12.25C22 6.59 17.52 2 12 2Z" />
      </svg>
    </span>

                        <span>
      Open source project:
      <span className="footer-link-text"> link</span>
    </span>
                    </a>

                    <a
                        className="footer-link"
                        href="https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing"
                        target="_blank"
                        rel="noreferrer"
                    >
    <span className="footer-icon wiki-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M4 5h2.1l2.18 11.2L10.8 9l-1.1-2.2H12l1.12 2.23L12.08 12l1.88 4.25L17 5h2l-3.48 14h-1.6L12 14.7 10.12 19H8.5L5.94 7.26 5.08 5H4Z" />
      </svg>
    </span>

                        <span>
      Shamir&apos;s secret sharing scheme:
      <span className="footer-link-text"> link</span>
    </span>
                    </a>
                </footer>
            </div>
        </div>
    )
}