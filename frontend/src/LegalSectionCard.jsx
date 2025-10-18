import React, { useState } from 'react'

export default function LegalSectionCard({ section, index }) {
  const [isExpanded, setIsExpanded] = useState(index === 0) // First card expanded by default

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <div className={`legal-card ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="legal-card-header" onClick={toggleExpand}>
        <div className="legal-card-title">
          <span className="legal-icon">⚖️</span>
          <div>
            <h4>{section.section_number || section.code}</h4>
            <p className="legal-subtitle">{section.title}</p>
          </div>
        </div>
        <button className="expand-btn" aria-label={isExpanded ? 'Collapse' : 'Expand'}>
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>
      
      {isExpanded && (
        <div className="legal-card-body">
          <div className="legal-description">
            <strong>Explanation:</strong>
            <p>{section.explanation || section.description}</p>
          </div>
          
          {section.matched_keywords && section.matched_keywords.length > 0 && (
            <div className="matched-keywords">
              <strong>Matched Keywords:</strong>
              <div className="keyword-tags">
                {section.matched_keywords.map((keyword, idx) => (
                  <span key={idx} className="keyword-tag">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {section.punishment && (
            <div className="punishment-info">
              <strong>⚠️ Punishment:</strong>
              <p>{section.punishment}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
