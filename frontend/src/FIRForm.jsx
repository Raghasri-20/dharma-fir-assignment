import React, { useState } from 'react'
import { processFIR } from './api.js'

export default function FIRForm({ onResult, onLoading, onError, onTextChange }) {
  const [text, setText] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    onLoading(true)
    onError(null)
    onResult(null)
    onTextChange(text)
    
    try {
      const data = await processFIR(text)
      if (data.error) {
        onError(data.message || 'Gemini couldn\'t process this FIR')
      } else {
        onResult(data)
      }
    } catch (err) {
      onError(err?.message || 'Failed to process FIR. Check your connection.')
    } finally {
      onLoading(false)
    }
  }

  const handleRetry = () => {
    if (text.trim()) {
      handleSubmit({ preventDefault: () => {} })
    }
  }

  return (
    <div className="fir-form-container">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="fir-text">FIR Text</label>
          <textarea
            id="fir-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your FIR text here for AI-powered analysis...\n\nExample:\nOn 14th September 2025, complainant Rahul Verma reported that he was assaulted and his mobile phone was stolen near Narsapur Road by accused Ramu Singh..."
            rows={12}
            className="fir-textarea"
          />
        </div>
        
        <div className="form-actions">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={!text.trim()}
          >
            <span className="btn-icon">🔍</span>
            Analyze with Gemini
          </button>
          
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => setText('')}
          >
            <span className="btn-icon">🗑️</span>
            Clear
          </button>
        </div>
      </form>
    </div>
  )
}
