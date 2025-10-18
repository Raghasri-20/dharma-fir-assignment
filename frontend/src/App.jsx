import React, { useState } from 'react'
import FIRForm from './FIRForm.jsx'
import FIRResult from './FIRResult.jsx'
import './styles.css'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [firText, setFirText] = useState('')

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚖️ Dharma FIR Assistant</h1>
        <p className="subtitle">AI-powered FIR analysis using Gemini 2.5 Flash</p>
      </header>
      
      <FIRForm 
        onResult={setResult} 
        onLoading={setLoading}
        onError={setError}
        onTextChange={setFirText}
      />
      
      <FIRResult 
        result={result} 
        loading={loading}
        error={error}
        firText={firText}
      />
    </div>
  )
}
