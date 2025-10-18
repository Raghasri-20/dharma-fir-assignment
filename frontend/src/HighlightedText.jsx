import React, { useState } from 'react'

export default function HighlightedText({ text, entities }) {
  const [hoveredEntity, setHoveredEntity] = useState(null)

  // Build a map of all entity values to their types
  const entityMap = {}
  Object.entries(entities).forEach(([type, values]) => {
    values.forEach(value => {
      if (value && value.trim()) {
        entityMap[value.toLowerCase()] = type
      }
    })
  })

  // Function to highlight text
  const highlightText = () => {
    if (!text) return null

    // Sort entities by length (longest first) to avoid partial matches
    const sortedEntities = Object.keys(entityMap).sort((a, b) => b.length - a.length)
    
    let highlightedText = text
    const replacements = []

    // Find all matches
    sortedEntities.forEach((entity, idx) => {
      const regex = new RegExp(`\\b${escapeRegex(entity)}\\b`, 'gi')
      let match
      while ((match = regex.exec(text)) !== null) {
        replacements.push({
          start: match.index,
          end: match.index + match[0].length,
          text: match[0],
          type: entityMap[entity.toLowerCase()],
          id: `entity-${idx}-${match.index}`
        })
      }
    })

    // Sort by position and remove overlaps
    replacements.sort((a, b) => a.start - b.start)
    const nonOverlapping = []
    let lastEnd = 0
    replacements.forEach(r => {
      if (r.start >= lastEnd) {
        nonOverlapping.push(r)
        lastEnd = r.end
      }
    })

    // Build the highlighted JSX
    if (nonOverlapping.length === 0) {
      return <span>{text}</span>
    }

    const parts = []
    let currentPos = 0

    nonOverlapping.forEach((r, idx) => {
      // Add text before highlight
      if (r.start > currentPos) {
        parts.push(
          <span key={`text-${idx}`}>{text.substring(currentPos, r.start)}</span>
        )
      }

      // Add highlighted entity
      parts.push(
        <span
          key={r.id}
          className={`highlight highlight-${r.type}`}
          onMouseEnter={() => setHoveredEntity(r)}
          onMouseLeave={() => setHoveredEntity(null)}
          data-tooltip={formatEntityType(r.type)}
        >
          {r.text}
        </span>
      )

      currentPos = r.end
    })

    // Add remaining text
    if (currentPos < text.length) {
      parts.push(
        <span key="text-end">{text.substring(currentPos)}</span>
      )
    }

    return parts
  }

  return (
    <div className="highlighted-text-container">
      <div className="highlight-legend">
        <span className="legend-title">Legend:</span>
        {Object.keys(entities).map(type => (
          entities[type]?.length > 0 && (
            <span key={type} className="legend-item">
              <span className={`legend-color highlight-${type}`}></span>
              {formatEntityType(type)}
            </span>
          )
        ))}
      </div>
      
      <div className="highlighted-text">
        {highlightText()}
      </div>

      {hoveredEntity && (
        <div className="entity-tooltip">
          <strong>{formatEntityType(hoveredEntity.type)}</strong>: {hoveredEntity.text}
        </div>
      )}
    </div>
  )
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function formatEntityType(type) {
  return type.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}
