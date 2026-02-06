import React, { useMemo, useState } from "react";
import axios from "axios";

const translations = {
  en: {
    title: "Financial Health Assessment",
    subtitle: "Upload statements or paste data to receive insights.",
    apiKey: "API Key",
    industry: "Industry",
    upload: "Upload File",
    analyze: "Analyze",
    analyzeSample: "Analyze Sample",
    metrics: "Key Metrics",
    recommendations: "Recommendations",
    flags: "Risk Flags",
    benchmarking: "Benchmarking",
    integrations: "Banking Integrations",
    credit: "Creditworthiness",
    riskScore: "Risk Score",
  },
  hi: {
    title: "वित्तीय स्वास्थ्य मूल्यांकन",
    subtitle: "इनसाइट्स के लिए स्टेटमेंट अपलोड करें या डेटा दें।",
    apiKey: "API कुंजी",
    industry: "उद्योग",
    upload: "फ़ाइल अपलोड",
    analyze: "विश्लेषण करें",
    analyzeSample: "सैंपल विश्लेषण",
    metrics: "मुख्य मेट्रिक्स",
    recommendations: "सिफारिशें",
    flags: "जोखिम संकेत",
    benchmarking: "बेंचमार्किंग",
    integrations: "बैंकिंग इंटीग्रेशन",
    credit: "क्रेडिट योग्यता",
    riskScore: "जोखिम स्कोर",
  }
};

const industries = [
  "Manufacturing",
  "Retail",
  "Agriculture",
  "Services",
  "Logistics",
  "E-commerce"
];

const defaultSample = [
  { revenue: 120000, expenses: 90000, cash_in: 115000, cash_out: 88000, ar: 25000, ap: 18000, inventory: 12000, debt: 15000 },
  { revenue: 135000, expenses: 98000, cash_in: 128000, cash_out: 92000, ar: 27000, ap: 20000, inventory: 13000, debt: 16000 }
];

const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
  const [language, setLanguage] = useState("en");
  const t = useMemo(() => translations[language], [language]);
  const [apiKey, setApiKey] = useState("dev-key");
  const [industry, setIndustry] = useState("Services");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [bankA, setBankA] = useState(null);
  const [bankB, setBankB] = useState(null);
  const [error, setError] = useState("");

  const headers = { "X-API-Key": apiKey };

  const runAnalysis = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post(`${apiBase}/analyze?industry=${industry}`, formData, { headers });
      setResult(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const runSample = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(`${apiBase}/analyze-json`, { industry, records: defaultSample }, { headers });
      setResult(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const loadIntegrations = async () => {
    try {
      const [a, b] = await Promise.all([
        axios.get(`${apiBase}/integrations/bank-a`, { headers }),
        axios.get(`${apiBase}/integrations/bank-b`, { headers })
      ]);
      setBankA(a.data);
      setBankB(b.data);
    } catch (err) {
      setError("Failed to load integrations");
    }
  };

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>{t.title}</h1>
          <p>{t.subtitle}</p>
        </div>
        <div className="lang-toggle">
          <button className={language === "en" ? "active" : ""} onClick={() => setLanguage("en")}>EN</button>
          <button className={language === "hi" ? "active" : ""} onClick={() => setLanguage("hi")}>HI</button>
        </div>
      </header>

      <section className="card">
        <div className="grid">
          <label>
            {t.apiKey}
            <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="dev-key" />
          </label>
          <label>
            {t.industry}
            <select value={industry} onChange={(e) => setIndustry(e.target.value)}>
              {industries.map((ind) => (
                <option key={ind} value={ind}>{ind}</option>
              ))}
            </select>
          </label>
          <label>
            {t.upload}
            <input type="file" accept=".csv,.xlsx,.xls,.pdf" onChange={(e) => setFile(e.target.files?.[0])} />
          </label>
        </div>
        <div className="actions">
          <button disabled={loading || !file} onClick={runAnalysis}>{t.analyze}</button>
          <button disabled={loading} onClick={runSample}>{t.analyzeSample}</button>
          <button disabled={loading} onClick={loadIntegrations}>{t.integrations}</button>
        </div>
        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <section className="grid-two">
          <div className="card">
            <h2>{t.metrics}</h2>
            <div className="metrics">
              <Metric label="Revenue" value={result.revenue} />
              <Metric label="Expenses" value={result.expenses} />
              <Metric label="Net Margin" value={toPercent(result.net_margin)} />
              <Metric label="Cashflow" value={result.net_cashflow} />
              <Metric label="Current Ratio" value={result.current_ratio?.toFixed(2)} />
              <Metric label="DSO (days)" value={result.dso_days?.toFixed(1)} />
              <Metric label={t.credit} value={result.creditworthiness} />
              <Metric label={t.riskScore} value={result.risk_score} />
            </div>
          </div>
          <div className="card">
            <h2>{t.benchmarking}</h2>
            <table>
              <thead>
                <tr><th>Metric</th><th>Actual</th><th>Benchmark</th></tr>
              </thead>
              <tbody>
                <tr><td>Net Margin</td><td>{toPercent(result.net_margin)}</td><td>{toPercent(result.benchmarks.net_margin)}</td></tr>
                <tr><td>Current Ratio</td><td>{result.current_ratio?.toFixed(2)}</td><td>{result.benchmarks.current_ratio}</td></tr>
                <tr><td>DSO Days</td><td>{result.dso_days?.toFixed(1)}</td><td>{result.benchmarks.dso_days}</td></tr>
              </tbody>
            </table>
          </div>
        </section>
      )}

      {result && (
        <section className="grid-two">
          <div className="card">
            <h2>{t.flags}</h2>
            <ul>
              {result.flags.length ? result.flags.map((flag) => <li key={flag}>{flag}</li>) : <li>No major risks detected.</li>}
            </ul>
          </div>
          <div className="card">
            <h2>{t.recommendations}</h2>
            <ul>
              {result.recommendations.map((rec) => <li key={rec}>{rec}</li>)}
            </ul>
          </div>
        </section>
      )}

      {(bankA || bankB) && (
        <section className="card">
          <h2>{t.integrations}</h2>
          <div className="grid-two">
            {bankA && <pre>{JSON.stringify(bankA, null, 2)}</pre>}
            {bankB && <pre>{JSON.stringify(bankB, null, 2)}</pre>}
          </div>
        </section>
      )}

      <footer className="footer">
        <span>Security: encryption in transit (TLS) and at rest (PostgreSQL + disk encryption).</span>
      </footer>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{formatValue(value)}</strong>
    </div>
  );
}

function toPercent(value) {
  if (value === null || value === undefined) return "-";
  return `${(value * 100).toFixed(1)}%`;
}

function formatValue(value) {
  if (value === null || value === undefined) return "-";
  if (typeof value === "number") return value.toLocaleString();
  return value;
}
