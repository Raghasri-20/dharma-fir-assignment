import React from 'react'

export default function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <h3>🤖 Analyzing FIR with Gemini...</h3>
      <p>Please wait while AI extracts entities and maps legal sections</p>
      <div className="loading-steps">
        <div className="loading-step">
          <span className="step-icon">✓</span>
          <span>Connecting to Gemini 2.5 Flash</span>
        </div>
        <div className="loading-step">
          <span className="step-icon">⏳</span>
          <span>Extracting entities from FIR text</span>
        </div>
        <div className="loading-step">
          <span className="step-icon">⏳</span>
          <span>Mapping to legal sections</span>
        </div>
      </div>
    </div>
  )
}
