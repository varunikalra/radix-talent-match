import { useEffect, useState } from 'react'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

const modules = [
  ['01', 'JD Analytics', 'Understand the expectations hidden inside job descriptions.'],
  ['02', 'Resume Parsing', 'Turn candidate documents into structured, usable profiles.'],
  ['03', 'Profile Builder', 'Create a clear and complete candidate readiness profile.'],
  ['04', 'Talent Check', 'Identify readiness signals and areas for improvement.'],
  ['05', 'Skill Matching', 'Connect verified candidate capabilities with role requirements.'],
]

const API_HEALTH_URL = `${API_BASE_URL}/api/health`

function JDAnalytics() {
  const [samples, setSamples] = useState([])
  const [selectedId, setSelectedId] = useState('')
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const controller = new AbortController()

    async function loadSamples() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/jd-analytics/samples`, {
          signal: controller.signal,
        })
        if (!response.ok) throw new Error(`Sample list unavailable (${response.status}).`)
        setSamples(await response.json())
      } catch (sampleError) {
        if (sampleError.name !== 'AbortError') {
          setError('Sample job descriptions could not be loaded. You can still paste custom text.')
        }
      }
    }

    loadSamples()
    return () => controller.abort()
  }, [])

  async function selectSample(sampleId) {
    setSelectedId(sampleId)
    setError('')
    setResult(null)
    if (!sampleId) {
      setText('')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/jd-analytics/samples/${encodeURIComponent(sampleId)}`)
      if (!response.ok) throw new Error(`Sample unavailable (${response.status}).`)
      const sample = await response.json()
      setText(sample.text)
    } catch (selectionError) {
      setError(selectionError.message)
    }
  }

  async function analyzeJob(event) {
    event.preventDefault()
    setError('')
    setResult(null)

    if (!text.trim()) {
      setError('Enter a job description or select a sample first.')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/jd-analytics/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      if (!response.ok) {
        const details = await response.json().catch(() => null)
        throw new Error(details?.detail || `Analysis failed (${response.status}).`)
      }
      setResult(await response.json())
    } catch (analysisError) {
      setError(analysisError.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="jd-analytics" aria-labelledby="jd-heading">
      <div className="jd-heading">
        <p className="eyebrow">JD Analytics</p>
        <h2 id="jd-heading">Turn a role description into a structured brief.</h2>
      </div>

      <form className="jd-workbench" onSubmit={analyzeJob}>
        <div className="jd-controls">
          <label htmlFor="sample-jd">Sample job description</label>
          <select id="sample-jd" value={selectedId} onChange={(event) => selectSample(event.target.value)}>
            <option value="">Choose a sample</option>
            {samples.map((sample) => (
              <option key={sample.id} value={sample.id}>{sample.name}</option>
            ))}
          </select>
          <label htmlFor="jd-text">Or paste a job description</label>
          <textarea
            id="jd-text"
            value={text}
            onChange={(event) => {
              setSelectedId('')
              setText(event.target.value)
            }}
            placeholder="Paste responsibilities, qualifications, and role requirements…"
            rows={13}
          />
          <button className="analyze-button" type="submit" disabled={loading}>
            {loading ? 'Analyzing…' : 'Analyze job description'}
          </button>
        </div>

        <div className="jd-results" aria-live="polite">
          {loading && <div className="result-empty"><span className="result-mark" /> Extracting requirements…</div>}
          {!loading && error && <div className="result-error" role="alert">{error}</div>}
          {!loading && !error && !result && (
            <div className="result-empty">
              <span className="result-mark" />
              <strong>Ready for analysis</strong>
              Select a sample or paste text to reveal structured requirements.
            </div>
          )}
          {!loading && result && <AnalysisResults result={result} />}
        </div>
      </form>
    </section>
  )
}

function AnalysisResults({ result }) {
  const listedCategories = result.radix_categories.filter((category) => category.skills.length)

  return (
    <div className="analysis-results">
      <div className="analysis-overview">
        <div>
          <span>Role</span>
          <strong>{result.title || 'Not identified'}</strong>
        </div>
        <div>
          <span>Company</span>
          <strong>{result.company || 'Not identified'}</strong>
        </div>
      </div>

      <div className="result-section">
        <h3>RADIX skills</h3>
        {listedCategories.length ? (
          <div className="category-grid">
            {listedCategories.map((category) => (
              <article className="category" key={category.code}>
                <span>{category.code}</span>
                <h4>{category.name}</h4>
                <ul>{category.skills.map((skill) => <li key={skill}>{skill}</li>)}</ul>
              </article>
            ))}
          </div>
        ) : <p className="muted">No curated skills were identified.</p>}
      </div>

      <div className="result-columns">
        <div className="result-section">
          <h3>Experience</h3>
          <RequirementList items={result.requirements.experience} empty="Not identified" />
        </div>
        <div className="result-section">
          <h3>Education</h3>
          <RequirementList items={result.requirements.education} empty="Not identified" />
        </div>
      </div>

      <div className="result-section">
        <h3>Responsibilities</h3>
        <RequirementList items={result.responsibilities} empty="Not identified" />
      </div>

      {result.unmatched_skills.length > 0 && (
        <div className="result-section">
          <h3>Other detected terms</h3>
          <p className="unmatched">{result.unmatched_skills.join(' · ')}</p>
        </div>
      )}
      <p className="extraction-note">Method: {result.extraction_method}</p>
    </div>
  )
}

function RequirementList({ items, empty }) {
  if (!items.length) return <p className="muted">{empty}</p>
  return <ul className="requirement-list">{items.map((item) => <li key={item}>{item}</li>)}</ul>
}

function App() {
  const [health, setHealth] = useState({ state: 'loading' })

  useEffect(() => {
    const controller = new AbortController()

    async function checkHealth() {
      try {
        const response = await fetch(API_HEALTH_URL, {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error(`The backend returned HTTP ${response.status}.`)
        }

        const data = await response.json()
        setHealth({ state: 'connected', service: data.service, version: data.version })
      } catch (error) {
        if (error.name !== 'AbortError') {
          setHealth({
            state: 'error',
            message: 'Backend unavailable. Start FastAPI on port 8000 and refresh.',
          })
        }
      }
    }

    checkHealth()
    return () => controller.abort()
  }, [])

  return (
    <main>
      <section className="masthead">
        <div className="brand-row">
          <p className="brand">RADIX</p>
          <div className={`status status-${health.state}`} role="status">
            <span aria-hidden="true" />
            {health.state === 'loading' && 'Checking backend'}
            {health.state === 'connected' && 'Connected'}
            {health.state === 'error' && 'Backend unavailable'}
          </div>
        </div>

        <div className="masthead-copy">
          <p className="eyebrow">Talent Match / Hackathon 2026</p>
          <h1>Where candidate potential meets the right opportunity.</h1>
          <p className="intro">
            A focused foundation for turning resumes, role requirements, and skill signals
            into clearer hiring decisions.
          </p>
        </div>
      </section>

      {health.state === 'error' && (
        <div className="connection-note" role="alert">{health.message}</div>
      )}
      {health.state === 'connected' && (
        <div className="connection-note">
          {health.service} v{health.version} is ready.
        </div>
      )}

      <JDAnalytics />

      <section className="modules" aria-labelledby="module-heading">
        <div className="section-heading">
          <p className="eyebrow">Project modules</p>
          <h2 id="module-heading">One pathway, five capabilities</h2>
        </div>
        <div className="module-grid">
          {modules.map(([number, title, description]) => (
            <article className="module" key={title}>
              <span>{number}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}

export default App
