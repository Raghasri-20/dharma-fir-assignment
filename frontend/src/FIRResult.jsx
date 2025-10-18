import React, { useState } from 'react'
import HighlightedText from './HighlightedText.jsx'
import LegalSectionCard from './LegalSectionCard.jsx'
import LoadingSpinner from './LoadingSpinner.jsx'
import ErrorMessage from './ErrorMessage.jsx'

export default function FIRResult({ result, loading, error, firText }) {
  const [copiedJSON, setCopiedJSON] = useState(false)
  const [copiedSummary, setCopiedSummary] = useState(false)

  // Show loading state
  if (loading) {
    return <LoadingSpinner />
  }

  // Show error state
  if (error) {
    return <ErrorMessage message={error} />
  }

  // Show placeholder when no result
  if (!result) {
    return (
      <div className="result-placeholder">
        <div className="placeholder-icon">📄</div>
        <p>Enter FIR text above and click "Analyze with Gemini" to see results</p>
      </div>
    )
  }

  const { entities, legal_sections, summary, extraction_method } = result

  // Copy to clipboard functions
  const copyJSON = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2))
    setCopiedJSON(true)
    setTimeout(() => setCopiedJSON(false), 2000)
  }

  const copySummary = () => {
    navigator.clipboard.writeText(summary)
    setCopiedSummary(true)
    setTimeout(() => setCopiedSummary(false), 2000)
  }

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `fir-analysis-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="result-container">
      {/* Header with export buttons */}
      <div className="result-header">
        <h2>✨ Analysis Results</h2>
        <div className="export-buttons">
          <button className="btn btn-small" onClick={copySummary} title="Copy summary">
            {copiedSummary ? '✓ Copied!' : '📋 Copy Summary'}
          </button>
          <button className="btn btn-small" onClick={copyJSON} title="Copy full JSON">
            {copiedJSON ? '✓ Copied!' : '📋 Copy JSON'}
          </button>
          <button className="btn btn-small" onClick={downloadJSON} title="Download as file">
            💾 Download
          </button>
        </div>
      </div>

      {extraction_method && (
        <div className="extraction-badge">
          🤖 Extracted using: {extraction_method}
        </div>
      )}

      {/* Summary Section */}
      <section className="result-section">
        <h3>📝 Summary</h3>
        <div className="summary-card">
          <p>{summary}</p>
        </div>
      </section>

      {/* Highlighted FIR Text */}
      {firText && entities && (
        <section className="result-section">
          <h3>🔍 Highlighted FIR Text</h3>
          <HighlightedText text={firText} entities={entities} />
        </section>
      )}

      {/* Entities Section */}
      <section className="result-section">
        <h3>👥 Extracted Entities</h3>
        <div className="entities-grid">
          {Object.entries(entities || {}).map(([key, values]) => (
            <div key={key} className="entity-card">
              <div className="entity-header">
                <span className="entity-icon">{getEntityIcon(key)}</span>
                <span className="entity-label">{formatEntityLabel(key)}</span>
                <span className="entity-count">{values?.length || 0}</span>
              </div>
              <div className="entity-values">
                {values?.length > 0 ? (
                  values.map((val, idx) => (
                    <span key={idx} className={`entity-tag entity-${key}`}>
                      {val}
                    </span>
                  ))
                ) : (
                  <span className="entity-empty">None found</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Legal Sections */}
      <section className="result-section">
        <h3>⚖️ Legal Sections</h3>
        {legal_sections?.length > 0 ? (
          <div className="legal-sections">
            {legal_sections.map((section, idx) => (
              <LegalSectionCard key={idx} section={section} index={idx} />
            ))}
          </div>
        ) : (
          <div className="no-sections">
            <p>No legal sections matched</p>
          </div>
        )}
      </section>
    </div>
  )
}

// Helper functions
function getEntityIcon(key) {
  const icons = {
    names: '👤',
    dates: '📅',
    locations: '📍',
    phone_numbers: '📞',
    crimes: '⚠️',
    threats: '💢',
    objects: '📦'
  }
  return icons[key] || '📌'
}

function formatEntityLabel(key) {
  return key.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}
