import React from 'react'

export default function ErrorMessage({ message }) {
  const handleRetry = () => {
    window.location.reload()
  }

  return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <h3>Gemini couldn't process this FIR</h3>
      <p className="error-message">{message}</p>
      <div className="error-suggestions">
        <p><strong>Try:</strong></p>
        <ul>
          <li>Rephrasing the FIR text</li>
          <li>Checking your internet connection</li>
          <li>Verifying the API key is valid</li>
          <li>Ensuring the text is not too long (&lt;10,000 characters)</li>
        </ul>
      </div>
      <button className="btn btn-primary" onClick={handleRetry}>
        🔄 Retry
      </button>
    </div>
  )
}
