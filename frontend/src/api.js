// Vite serves the API locally during development; deployed containers proxy /api.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')

export async function submitAssessment(values) {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(values),
  })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail?.[0]?.msg || body.detail || 'Unable to assess risk. Please check the values and try again.')
  }
  return response.json()
}
