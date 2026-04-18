import { useState } from "react"
import { recoverSecret } from "../api/secrets"
import type { ApiError, RecoverResponse } from "../types/api"

export default function RecoverForm() {
    const [sharesText, setSharesText] = useState("")
    const [sharesCopied, setSharesCopied] = useState(false)
    const [secretCopied, setSecretCopied] = useState(false)

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<ApiError | null>(null)
    const [result, setResult] = useState<RecoverResponse | null>(null)
    const [validationError, setValidationError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        setValidationError("")
        setError(null)
        setResult(null)
        setSharesCopied(false)
        setSecretCopied(false)

        const shares = sharesText
            .split("\n")
            .map((item) => item.trim())
            .filter(Boolean)

        if (shares.length === 0) {
            setValidationError("At least one share is required")
            return
        }

        try {
            setLoading(true)
            const data = await recoverSecret({ shares })
            setResult(data)
        } catch (err) {
            setError(err as ApiError)
        } finally {
            setLoading(false)
        }
    }

    const handleCopyShares = async () => {
        if (!sharesText.trim()) {
            return
        }

        try {
            await navigator.clipboard.writeText(sharesText)
            setSharesCopied(true)

            setTimeout(() => {
                setSharesCopied(false)
            }, 1500)
        } catch (error) {
            console.error("Failed to copy shares:", error)
        }
    }

    const handleCopySecret = async () => {
        if (!result?.secret) {
            return
        }

        try {
            await navigator.clipboard.writeText(result.secret)
            setSecretCopied(true)

            setTimeout(() => {
                setSecretCopied(false)
            }, 1500)
        } catch (error) {
            console.error("Failed to copy secret:", error)
        }
    }

    return (
        <div className="workspace">
            <form onSubmit={handleSubmit} className="panel panel-left">
                <div className="panel-header">
                    <h2>Input</h2>
                </div>

                <label className="field">
                    <div className="result-section-header">
                        <span className="field-label">Shares</span>
                        <button
                            type="button"
                            className="copy-btn"
                            onClick={handleCopyShares}
                            disabled={!sharesText.trim()}
                        >
                            {sharesCopied ? "Copied!" : "Copy"}
                        </button>
                    </div>

                    <textarea
                        value={sharesText}
                        onChange={(e) => setSharesText(e.target.value)}
                        placeholder={"Enter one share per line\nshare1\nshare2\nshare3"}
                        rows={14}
                    />
                </label>

                {validationError && (
                    <div className="message-box error">
                        <strong>Validation error:</strong> {validationError}
                    </div>
                )}
            </form>

            <div className="center-action">
                <button
                    type="submit"
                    className="action-btn"
                    onClick={() => {
                        const form = document.querySelector(".panel-left") as HTMLFormElement | null
                        form?.requestSubmit()
                    }}
                    disabled={loading}
                >
                    {loading ? "Processing..." : "Recover Secret"}
                </button>
            </div>

            <div className="panel panel-right">
                <div className="panel-header">
                    <h2>Output</h2>
                </div>

                {!result && !error && !validationError && (
                    <div className="placeholder">
                        Recovered secret and request ID will appear here.
                    </div>
                )}

                {error && (
                    <div className="message-box error">
                        <p><strong>Error:</strong> {error.message}</p>
                        <p><strong>Request ID:</strong> {error.request_id}</p>
                    </div>
                )}

                {result && (
                    <div className="result-content">
                        <div className="result-section">
                            <div className="result-section-header">
                                <strong>Recovered Secret</strong>
                                <button
                                    type="button"
                                    className="copy-btn"
                                    onClick={handleCopySecret}
                                >
                                    {secretCopied ? "Copied!" : "Copy"}
                                </button>
                            </div>

                            <div className="secret-box">{result.secret}</div>
                        </div>

                        <div className="result-meta">
                            <p><strong>Request ID:</strong> {result.request_id}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}