import { useState } from 'react'
import { submitAssessment } from './api'

const fields = [
  ['age', 'Age', 'number', { min: 18, max: 120, placeholder: 'e.g. 54' }],
  ['sex', 'Biological sex', 'select', [['1', 'Male'], ['0', 'Female']]],
  ['cp', 'Chest pain type', 'select', [['0', 'Typical angina'], ['1', 'Atypical angina'], ['2', 'Non-anginal pain'], ['3', 'Asymptomatic']]],
  ['trestbps', 'Resting blood pressure (mm Hg)', 'number', { min: 70, max: 260, placeholder: 'e.g. 130' }],
  ['chol', 'Serum cholesterol (mg/dL)', 'number', { min: 80, max: 700, placeholder: 'e.g. 246' }],
  ['fbs', 'Fasting blood sugar > 120 mg/dL', 'select', [['0', 'No'], ['1', 'Yes']]],
  ['restecg', 'Resting ECG result', 'select', [['0', 'Normal'], ['1', 'ST-T abnormality'], ['2', 'Left ventricular hypertrophy']]],
  ['thalach', 'Maximum heart rate achieved', 'number', { min: 40, max: 240, placeholder: 'e.g. 150' }],
  ['exang', 'Exercise-induced angina', 'select', [['0', 'No'], ['1', 'Yes']]],
  ['oldpeak', 'ST depression (oldpeak)', 'number', { min: 0, max: 10, step: '0.1', placeholder: 'e.g. 1.4' }],
  ['slope', 'Peak exercise ST slope', 'select', [['0', 'Upsloping'], ['1', 'Flat'], ['2', 'Downsloping']]],
  ['ca', 'Major vessels (0–4)', 'select', [['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4']]],
  ['thal', 'Thalassemia result', 'select', [['0', 'Unknown'], ['1', 'Normal'], ['2', 'Fixed defect'], ['3', 'Reversible defect']]],
]

const sample = { age: '54', sex: '1', cp: '2', trestbps: '130', chol: '246', fbs: '0', restecg: '1', thalach: '150', exang: '0', oldpeak: '1.4', slope: '1', ca: '0', thal: '2' }

export default function App() {
  const [values, setValues] = useState({})
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const update = (name, value) => setValues(current => ({ ...current, [name]: value }))
  const useSample = () => { setValues(sample); setResult(null); setError('') }
  const handleSubmit = async event => {
    event.preventDefault()
    setError(''); setResult(null); setLoading(true)
    try {
      const payload = Object.fromEntries(fields.map(([name, , type]) => [name, type === 'number' ? Number(values[name]) : Number(values[name])]))
      setResult(await submitAssessment(payload))
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }

  return <main>
    <section className="hero">
      <div><p className="eyebrow">EDUCATIONAL SCREENING TOOL</p><h1>Understand heart-health risk factors.</h1><p className="lede">Enter clinical measurements to get an educational risk estimate. It is designed to support—not replace—a conversation with a healthcare professional.</p></div>
      <aside><span aria-hidden="true">♥</span><strong>Not for emergencies</strong><p>If you have chest pain, shortness of breath, or another emergency symptom, contact local emergency services immediately.</p></aside>
    </section>
    <section className="workspace">
      <form onSubmit={handleSubmit}>
        <div className="form-heading"><div><p className="eyebrow">PATIENT MEASUREMENTS</p><h2>Assessment details</h2></div><button type="button" className="secondary" onClick={useSample}>Use sample data</button></div>
        <div className="grid">{fields.map(([name, label, type, config]) => <label key={name}>{label}
          {type === 'select' ? <select required value={values[name] ?? ''} onChange={e => update(name, e.target.value)}><option value="" disabled>Select an option</option>{config.map(([value, text]) => <option key={value} value={value}>{text}</option>)}</select>
          : <input required type="number" value={values[name] ?? ''} onChange={e => update(name, e.target.value)} {...config} />}
        </label>)}</div>
        {error && <p className="error" role="alert">{error}</p>}
        <button className="primary" disabled={loading}>{loading ? 'Calculating…' : 'Calculate risk estimate'}</button>
      </form>
      <section className="result-panel" aria-live="polite">
        {result ? <><p className="eyebrow">ASSESSMENT RESULT</p><div className={`badge ${result.risk_level.toLowerCase()}`}>{result.risk_level} estimated risk</div><p className="percentage">{result.probability}%</p><p className="result-copy">{result.message}</p><p className="disclaimer">{result.disclaimer}</p></> : <><div className="empty-icon">⌁</div><h2>Your result will appear here</h2><p>Complete all fields and calculate an estimate. Results are interpreted as low, moderate, or high educational risk.</p></>}
      </section>
    </section>
    <footer>CardioCheck is an academic project. Do not use it to diagnose, treat, or delay medical care.</footer>
  </main>
}
