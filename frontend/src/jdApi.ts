const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

export interface JDSample {
  id: string
  name: string
}

export interface JDRequirement {
  experience: string[]
  education: string[]
}

export interface JDCategory {
  code: string
  name: string
  skills: string[]
}

export interface JDAnalysis {
  title: string | null
  company: string | null
  requirements: JDRequirement
  technical_skills: string[]
  soft_skills: string[]
  responsibilities: string[]
  radix_categories: JDCategory[]
  unmatched_skills: string[]
  extraction_method: string
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init)
  if (!response.ok) {
    const detail = await response.json().catch(() => null) as { detail?: string } | null
    throw new Error(detail?.detail || `Request failed (${response.status}).`)
  }
  return response.json() as Promise<T>
}

export function listJDSamples(): Promise<JDSample[]> {
  return requestJson('/api/jd-analytics/samples')
}

export function getJDSample(id: string): Promise<JDSample & { text: string }> {
  return requestJson(`/api/jd-analytics/samples/${encodeURIComponent(id)}`)
}

export function analyzeJD(text: string): Promise<JDAnalysis> {
  return requestJson('/api/jd-analytics/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
}
