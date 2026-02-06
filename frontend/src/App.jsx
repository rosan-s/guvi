import React, { useMemo, useRef, useState } from "react";
import axios from "axios";

const translations = {
  en: {
    title: "AI-Powered Financial Health Assessment",
    subtitle: "Upload statements or paste data to receive AI-driven insights.",
    apiKey: "API Key",
    industry: "Industry",
    upload: "Upload File",
    analyze: "Analyze",
    analyzeSample: "Analyze Sample",
    metrics: "Key Metrics",
    recommendations: "Smart Recommendations",
    flags: "Risk Flags",
    benchmarking: "Benchmarking",
    integrations: "Banking Integrations",
    credit: "Creditworthiness",
    riskScore: "Risk Score",
    forecast: "3-Month Forecast",
    scenarios: "Scenario Analysis",
    anomalies: "Detected Anomalies",
    defaultRisk: "Credit Default Risk",
    riskFactors: "Key Risk Factors",
  },
  hi: {
    title: "AI-संचालित वित्तीय स्वास्थ्य मूल्यांकन",
    subtitle: "इनसाइट्स के लिए स्टेटमेंट अपलोड करें या डेटा दें।",
    apiKey: "API कुंजी",
    industry: "उद्योग",
    upload: "फ़ाइल अपलोड",
    analyze: "विश्लेषण करें",
    analyzeSample: "सैंपल विश्लेषण",
    metrics: "मुख्य मेट्रिक्स",
    recommendations: "स्मार्ट सिफारिशें",
    flags: "जोखिम संकेत",
    benchmarking: "बेंचमार्किंग",
    integrations: "बैंकिंग इंटीग्रेशन",
    credit: "क्रेडिट योग्यता",
    riskScore: "जोखिम स्कोर",
    forecast: "3-मास पूर्वानुमान",
    scenarios: "परिदृश्य विश्लेषण",
    anomalies: "पहचाने गए विसंगतियां",
    defaultRisk: "क्रेडिट डिफ़ॉल्ट जोखिम",
    riskFactors: "मुख्य जोखिम कारक",
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

// Get API base URL
const getApiBase = () => {
  // Use environment variable first (set by Render)
  if (import.meta.env.VITE_API_BASE_URL) {
    const apiUrl = import.meta.env.VITE_API_BASE_URL;
    return apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
  }

  // For local development
  if (typeof window !== "undefined" && window.location.hostname === "localhost") {
    return "http://localhost:8000";
  }

  // Fallback: same origin
  if (typeof window !== "undefined") {
    return window.location.origin;
  }

  return "http://localhost:8000";
};

const apiBase = getApiBase();

export default function App() {
  const [language, setLanguage] = useState("en");
  const t = useMemo(() => translations[language], [language]);
  const [apiKey, setApiKey] = useState("dev-key");
  const [industry, setIndustry] = useState("Services");
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [bankA, setBankA] = useState(null);
  const [bankB, setBankB] = useState(null);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

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
            <div className="file-picker">
              <button
                type="button"
                className="file-button"
                onClick={() => fileInputRef.current?.click()}
              >
                Choose File
              </button>
              <span className="file-name">{fileName || "No file selected"}</span>
              <input
                ref={fileInputRef}
                className="file-input"
                type="file"
                accept=".csv,.xlsx,.xls,.pdf"
                onChange={(e) => {
                  const selected = e.target.files?.[0] || null;
                  setFile(selected);
                  setFileName(selected?.name || "");
                }}
              />
            </div>
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

      {result && result.default_probability !== undefined && (
        <section className="grid-two">
          <div className="card">
            <h2>{t.defaultRisk}</h2>
            <div className="metric">
              <span>Default Probability</span>
              <strong>{result.default_probability?.toFixed(1)}%</strong>
            </div>
            <div style={{ marginTop: "12px" }}>
              <RiskGauge risk={result.default_probability} />
            </div>
          </div>
          <div className="card">
            <h2>{t.riskFactors}</h2>
            <ul>
              {result.credit_risk_factors?.map((factor) => <li key={factor}>{factor}</li>)}
            </ul>
          </div>
        </section>
      )}

      {result && result.forecast && result.forecast.revenue?.length > 0 && (
        <section className="card">
          <h2>{t.forecast}</h2>
          <table>
            <thead>
              <tr><th>Period</th><th>Revenue</th><th>Expenses</th><th>Net Margin</th></tr>
            </thead>
            <tbody>
              {result.forecast.revenue.map((rev, idx) => (
                <tr key={idx}>
                  <td>Month {idx + 1}</td>
                  <td>{formatValue(rev)}</td>
                  <td>{formatValue(result.forecast.expenses[idx])}</td>
                  <td>{toPercent(result.forecast.net_margin[idx])}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {result && result.scenarios && (
        <section className="card">
          <h2>{t.scenarios}</h2>
          <table>
            <thead>
              <tr><th>Scenario</th><th>Revenue</th><th>Expenses</th><th>Net Margin</th></tr>
            </thead>
            <tbody>
              {Object.entries(result.scenarios).map(([key, scenario]) => (
                <tr key={key}>
                  <td className={`scenario-${key}`}>{key.toUpperCase()}</td>
                  <td>{formatValue(scenario.revenue)}</td>
                  <td>{formatValue(scenario.expenses)}</td>
                  <td>{toPercent(scenario.net_margin)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {result && result.anomalies && result.anomalies.length > 0 && (
        <section className="card alert-anomalies">
          <h2>{t.anomalies}</h2>
          <ul>
            {result.anomalies.map((anom) => <li key={anom}>{anom}</li>)}
          </ul>
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

function RiskGauge({ risk }) {
  const color = risk < 20 ? "green" : risk < 40 ? "yellow" : risk < 60 ? "orange" : "red";
  const width = `${Math.min(risk, 100)}%`;
  return (
    <div style={{
      width: "100%",
      height: "20px",
      backgroundColor: "#eee",
      borderRadius: "4px",
      overflow: "hidden",
    }}>
      <div style={{
        width,
        height: "100%",
        backgroundColor: color,
        transition: "width 0.3s ease",
      }} />
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
