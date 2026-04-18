import { useState } from "react"
import { splitSecret } from "../api/secrets"
import type { ApiError, SplitResponse } from "../types/api"

export default function SplitForm() {
    const [secret, setSecret] = useState("")
    const [threshold, setThreshold] = useState("3")
    const [totalShares, setTotalShares] = useState("5")
    const [copied, setCopied] = useState(false)
    const [secretCopied, setSecretCopied] = useState(false)


    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<ApiError | null>(null)
    const [result, setResult] = useState<SplitResponse | null>(null)
    const [validationError, setValidationError] = useState("")

    const handleCopyShares = async () => {
        if (!result) {
            return
        }

        const textToCopy = result.shares.join("\n")

        try {
            await navigator.clipboard.writeText(textToCopy)
            setCopied(true)

            setTimeout(() => {
                setCopied(false)
            }, 1500)
        } catch (error) {
            console.error("Failed to copy shares:", error)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        setValidationError("")
        setError(null)
        setResult(null)
        setCopied(false)
        setSecretCopied(false)

        const thresholdNumber = Number(threshold)
        const totalSharesNumber = Number(totalShares)

        if (!secret.trim()) {
            setValidationError("Secret is required")
            return
        }

        if (!Number.isInteger(thresholdNumber) || thresholdNumber <= 0) {
            setValidationError("Threshold must be a positive integer")
            return
        }

        if (!Number.isInteger(totalSharesNumber) || totalSharesNumber <= 0) {
            setValidationError("Total shares must be a positive integer")
            return
        }

        if (thresholdNumber > totalSharesNumber) {
            setValidationError("Threshold cannot be greater than total shares")
            return
        }

        try {
            setLoading(true)

            const data = await splitSecret({
                secret: secret.trim(),
                threshold: thresholdNumber,
                totalShares: totalSharesNumber,
            })

            setResult(data)
        } catch (err) {
            setError(err as ApiError)
        } finally {
            setLoading(false)
        }
    }
    const handleCopySecret = async () => {
        if (!secret.trim()) {
            return
        }

        try {
            await navigator.clipboard.writeText(secret)
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
                        <span className="field-label">Secret</span>
                        <button
                            type="button"
                            className="copy-btn"
                            onClick={handleCopySecret}
                            disabled={!secret.trim()}
                        >
                            {secretCopied ? "Copied!" : "Copy"}
                        </button>
                    </div>

                    <textarea
                        value={secret}
                        onChange={(e) => setSecret(e.target.value)}
                        placeholder="Enter secret text"
                        rows={12}
                    />
                </label>

                <div className="field-row">
                    <label className="field">
  <span className="field-label with-help">
    Threshold
    <span className="tooltip">
      <button type="button" className="help-btn">
        ?
      </button>
      <span className="tooltip-box">
        Minimum number of shares required to recover the secret.
        For example, if threshold is 3, then any 3 valid shares can restore it.
      </span>
    </span>
  </span>

                        <input
                            type="number"
                            value={threshold}
                            onChange={(e) => setThreshold(e.target.value)}
                            min="1"
                        />
                    </label>

                    <label className="field">
  <span className="field-label with-help">
    Total Shares
    <span className="tooltip tooltip-right">
      <button type="button" className="help-btn">
        ?
      </button>
      <span className="tooltip-box">
        Total number of shares generated from the secret.
        This value must be greater than or equal to threshold.
      </span>
    </span>
  </span>

                        <input
                            type="number"
                            value={totalShares}
                            onChange={(e) => setTotalShares(e.target.value)}
                            min="1"
                        />
                    </label>
                </div>

                {validationError && (
                    <div className="message-box error">
                        <strong>Validation error:</strong> {validationError}
                    </div>
                )}
            </form>

            <div className="center-action">
                <button
                    type="submit"
                    form={undefined}
                    className="action-btn"
                    onClick={() => {
                        const form = document.querySelector(".panel-left") as HTMLFormElement | null
                        form?.requestSubmit()
                    }}
                    disabled={loading}
                >
                    {loading ? "Processing..." : "Split Secret"}
                </button>
            </div>

            <div className="panel panel-right">
                <div className="panel-header">
                    <h2>Output</h2>
                </div>

                {!result && !error && !validationError && (
                    <div className="placeholder">
                        Generated shares, share count and request ID will appear here.
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
                        <div className="result-meta">
                            <p><strong>Share Count:</strong> {result.share_count}</p>
                            <p><strong>Request ID:</strong> {result.request_id}</p>
                        </div>

                        <div className="result-section">
                            <div className="result-section-header">
                                <strong>Shares</strong>
                                <button
                                    type="button"
                                    className="copy-btn"
                                    onClick={handleCopyShares}
                                >
                                    {copied ? "Copied!" : "Copy all"}
                                </button>
                            </div>

                            <div className="shares-list">
                                {result.shares.map((share, index) => (
                                    <div key={index} className="share-item">
                                        <span className="share-index">{index + 1}.</span>
                                        <span className="share-text">{share}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}