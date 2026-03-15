import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { FaBrain, FaClock, FaChartLine, FaExclamationTriangle } from "react-icons/fa";
import "../styles/dashboard.css";
import { useModelContext } from "../context/ModelContext";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const MODELS = [
  {
    name:       "Linear Regression",
    speed:      "Fast",
    accuracy:   "Medium",
    complexity: "Low",
    best:       "Simple / small datasets",
    icon:       <FaChartLine />,
  },
  {
    name:       "Random Forest",
    speed:      "Medium",
    accuracy:   "High",
    complexity: "Medium",
    best:       "Complex sensor relationships",
    icon:       <FaBrain />,
  },
  {
    name:       "LSTM",
    speed:      "Slow",
    accuracy:   "Very High",
    complexity: "High",
    best:       "Time-series forecasting",
    icon:       <FaClock />,
  },
  {
    name:       "Autoencoder",
    speed:      "Medium",
    accuracy:   "High",
    complexity: "Medium",
    best:       "Anomaly detection",
    icon:       <FaExclamationTriangle />,
  },
];

const modelComparison = [
  { model: "Linear Regression", speed: 9, accuracy: 6, complexity: 2 },
  { model: "Random Forest",     speed: 7, accuracy: 8, complexity: 6 },
  { model: "LSTM",              speed: 4, accuracy: 9, complexity: 9 },
  { model: "Autoencoder",       speed: 6, accuracy: 8, complexity: 7 },
];

function getRecommendation(lastRun) {
  if (!lastRun) return null;

  const sensorCount = lastRun.sensors?.length || 0;

  if (sensorCount <= 2) {
    return {
      model:  "Linear Regression",
      reason: "Few sensors selected. Linear Regression works well for simple relationships.",
    };
  }

  if (sensorCount <= 8) {
    return {
      model:  "Random Forest",
      reason: "Multiple sensors detected. Random Forest handles nonlinear interactions effectively.",
    };
  }

  return {
    model:  "LSTM",
    reason: "Large sensor set detected. LSTM can model temporal dependencies in sensor data.",
  };
}

function Models() {
  const { lastRun } = useModelContext();

  console.log("LAST RUN:", lastRun);

  const recommendation = getRecommendation(lastRun);

  return (
    <div className="layout">
      <Sidebar />

      <div className="main">
        <Header />

        <div className="content">

          {/* Page Header */}
          <div className="pageHeader">
            <h1>AI Models</h1>
            <p>Choose the right model for your sensor data</p>
          </div>

          {/* Recommendation */}
          {recommendation && (
            <div className="chartArea">
              <h2>Recommended Model Based on Your Dashboard Run</h2>
              <div className="metricCard">
                <h4>{recommendation.model}</h4>
                <p style={{ fontSize: 13, marginTop: 10 }}>
                  {recommendation.reason}
                </p>
              </div>
            </div>
          )}

          {/* Hint if no run yet */}
          {!lastRun && (
            <div className="emptyState">
              <p>Run a model from the Dashboard to see recommendations.</p>
            </div>
          )}

          {/* Model Cards */}
          <div className="metrics">
            {MODELS.map((model) => (
              <div key={model.name} className="metricCard">
                <h4 style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  {model.icon} {model.name}
                </h4>
                <div style={{ marginTop: 10, fontSize: 12, lineHeight: 1.8 }}>
                  <div><strong>⚡ Speed:</strong> {model.speed}</div>
                  <div><strong>🎯 Accuracy:</strong> {model.accuracy}</div>
                  <div><strong>🧠 Complexity:</strong> {model.complexity}</div>
                </div>
                <p style={{ marginTop: 12, fontSize: 13 }}>
                  <strong>Best for:</strong> {model.best}
                </p>
              </div>
            ))}
          </div>

          {/* Model Comparison Chart */}
          <div className="chartArea">
            <h2>Model Comparison</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelComparison}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="model" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    background: "#080f1c",
                    border: "1px solid rgba(0,200,255,0.35)",
                    borderRadius: "8px",
                    fontFamily: "'Space Mono', monospace",
                    fontSize: "12px",
                  }}
                />
                <Bar dataKey="accuracy"   fill="#00c8ff" />
                <Bar dataKey="speed"      fill="#00ff9d" />
                <Bar dataKey="complexity" fill="#ff4060" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Quick Model Guide */}
          <div className="chartArea">
            <h2>Quick Model Selection Guide</h2>
            <div className="metrics">
              <div className="metricCard">
                <h4>Simple Data</h4>
                <p style={{ fontSize: 13 }}>Use <strong>Linear Regression</strong></p>
              </div>
              <div className="metricCard">
                <h4>Complex Sensor Interactions</h4>
                <p style={{ fontSize: 13 }}>Use <strong>Random Forest</strong></p>
              </div>
              <div className="metricCard">
                <h4>Time-Series Data</h4>
                <p style={{ fontSize: 13 }}>Use <strong>LSTM</strong></p>
              </div>
              <div className="metricCard">
                <h4>Anomaly Detection</h4>
                <p style={{ fontSize: 13 }}>Use <strong>Autoencoder</strong></p>
              </div>
            </div>
          </div>

          {/* Hybrid Pipeline */}
          <div className="explanation">
            <h2>Hybrid Digital Twin Pipeline</h2>
            <pre>
Sensors
   ↓
Data Quality Analysis
   ↓
Sensor Fusion
   ↓
Prediction Models
   ↓
Anomaly Detection
   ↓
Health Score & AI Explanation
            </pre>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Models;