import axios from 'axios'

const client = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 60000,  // Increased to 60 seconds for Gemini processing
  headers: { 'Content-Type': 'application/json' }
})

export async function processFIR(text) {
  const res = await client.post('/parse-fir', { text })
  return res.data
}
