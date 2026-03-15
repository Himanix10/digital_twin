import { runModel, explainAI, uploadCSV, previewCSV } from "../services/api";
import { useState, useEffect } from "react";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import MetricCard from "../components/MetricCard";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

import "../styles/dashboard.css";

const MODELS = ["Linear Regression", "Random Forest", "LSTM", "Autoencoder"];

const LEGEND_ITEMS = [
  { key: "actual",    color: "#00c8ff", label: "Actual Signal",       dash: false },
  { key: "predicted", color: "#ff4060", label: "Predicted Signal",    dash: true  },
  { key: "anomaly",   color: "#ff4060", label: "Anomaly Point",       dot: true   },
];

function Dashboard() {
  const [result, setResult]                   = useState(null);
  const [chartData, setChartData]             = useState([]);
  const [explanation, setExplanation]         = useState("");
  const [model, setModel]                     = useState("Random Forest");
  const [horizon, setHorizon]                 = useState(10);
  const [loading, setLoading]                 = useState(false);
  const [explLoading, setExplLoading]         = useState(false);
  const [dataMode, setDataMode]               = useState("simulated");
  const [csvFile, setCsvFile]                 = useState(null);
  const [csvSensors, setCsvSensors]           = useState([]);
  const [selectedSensors, setSelectedSensors] = useState([]);
  const [apiError, setApiError]               = useState("");

  const extractError = (err) => {
    if (err.response?.data?.detail) return err.response.data.detail;
    if (err.response?.data?.error)  return err.response.data.error;
    if (err.response?.data)         return JSON.stringify(err.response.data);
    return err.message;
  };

  const handleCSVUpload = async (file) => {
    try {
      const response = await previewCSV(file);
      const numeric = response.data.numeric_columns;
      setCsvSensors(numeric);
      setSelectedSensors(numeric.slice(0, 2));
    } catch (err) {
      setApiError(extractError(err));
    }
  };

  const toggleSensor = (sensor) => {
    if (selectedSensors.includes(sensor)) {
      setSelectedSensors(selectedSensors.filter((s) => s !== sensor));
    } else {
      setSelectedSensors([...selectedSensors, sensor]);
    }
  };

  const selectAllSensors = () => setSelectedSensors(csvSensors);
  const clearSensors     = () => setSelectedSensors([]);

  const runPrediction = async () => {
    setLoading(true);
    setApiError("");
    setResult(null);
    setExplanation("");

    try {
      let response;

      if (dataMode === "csv" && csvFile) {
        response = await uploadCSV(csvFile, selectedSensors.join(","), model);
      } else {
        const sampleData = {
          data: [
            { temperature: 50, vibration: 30, pressure: 100 },
            { temperature: 52, vibration: 31, pressure: 102 },
            { temperature: 49, vibration: 29, pressure: 101 },
            { temperature: 51, vibration: 30, pressure: 103 },
            { temperature: 48, vibration: 28, pressure: 99  },
            { temperature: 53, vibration: 32, pressure: 104 },
            { temperature: 47, vibration: 27, pressure: 98  },
          ],
          sensors: ["temperature", "vibration"],
          model,
          horizon,
        };
        response = await runModel(sampleData);
      }

      const data = response.data;

      if (
        data.actual    === undefined ||
        data.predicted === undefined ||
        data.health    === undefined ||
        data.noise     === undefined ||
        data.anomalies === undefined
      ) {
        setApiError(`Unexpected response shape: ${JSON.stringify(data)}`);
        return;
      }

      setResult(data);
      setChartData(
        data.actual.map((value, index) => ({
          index,
          actual:    value,
          predicted: data.predicted[index],
          anomaly:   data.anomalies[index] ? value : null,
        }))
      );

    } catch (err) {
      setApiError(extractError(err));
    } finally {
      setLoading(false);
    }
  };

  const generateExplanation = async () => {
    setExplLoading(true);
    try {
      const response = await explainAI({
        health:    result.health,
        anomalies: result.anomalies.length,
        noise:     result.noise,
      });
      setExplanation(response.data.explanation);
    } catch (err) {
      setApiError(extractError(err));
    } finally {
      setExplLoading(false);
    }
  };

  const fmt = (val) =>
    val != null && !isNaN(val) ? Number(val).toFixed(2) : "—";

  return (
    <div className="layout">
      <Sidebar />

      <div className="main">
        <Header />

        <div className="content">

          {/* Controls */}
          <div className="controls">

            <div>
              <label>Model</label>
              <select value={model} onChange={(e) => setModel(e.target.value)}>
                {MODELS.map((m) => <option key={m}>{m}</option>)}
              </select>
            </div>

            <div>
              <label>Prediction Horizon</label>
              <input
                type="number"
                value={horizon}
                onChange={(e) => setHorizon(Number(e.target.value))}
                min={1}
                max={50}
              />
            </div>

            <div>
              <label>Data Source</label>
              <select value={dataMode} onChange={(e) => setDataMode(e.target.value)}>
                <option value="simulated">Simulated Data</option>
                <option value="csv">Upload CSV</option>
              </select>
            </div>

            {dataMode === "csv" && (
              <div>
                <label>CSV File</label>
                <input
                  type="file"
                  accept=".csv"
                  className="fileInput"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    setCsvFile(file);
                    handleCSVUpload(file);
                  }}
                />
              </div>
            )}

            {dataMode === "csv" && csvSensors.length > 0 && (
              <div>
                <label>Sensors ({selectedSensors.length} selected)</label>
                <div className="sensorActions">
                  <button onClick={selectAllSensors}>Select All</button>
                  <button onClick={clearSensors}>Clear</button>
                </div>
                <div className="sensorChipContainer">
                  {csvSensors.slice(0, 200).map((sensor) => (
                    <div
                      key={sensor}
                      className={`sensorChip ${selectedSensors.includes(sensor) ? "active" : ""}`}
                      onClick={() => toggleSensor(sensor)}
                    >
                      {sensor}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              className="primaryBtn"
              onClick={runPrediction}
              disabled={loading}
            >
              {loading ? "⚙ Processing..." : "▶ Run Model"}
            </button>

          </div>

          {/* Error Banner */}
          {apiError && (
            <div className="errorBanner">
              <span className="errorIcon">⚠</span>
              <pre>{apiError}</pre>
            </div>
          )}

          {/* Metrics */}
          {result && (
            <div className="metrics">
              <MetricCard title="Health Score" value={fmt(result.health)}            accent="cyan"  />
              <MetricCard title="Anomalies"    value={result.anomalies?.length ?? 0} accent="red"   />
              <MetricCard title="Noise Level"  value={fmt(result.noise)}             accent="amber" />
            </div>
          )}

          {/* Chart */}
          {chartData.length > 0 && (
            <div className="chartArea">
              <h2>System Prediction — {model}</h2>

              {/* Custom Legend */}
              <div className="chartLegend">
                <span className="legendItem">
                  <span className="legendDot" style={{ background: "#00c8ff" }}></span>
                  Actual — Mean-fused sensor signal (ground truth)
                </span>
                <span className="legendItem">
                  <span className="legendDot" style={{ background: "#ff4060", opacity: 0.7 }}></span>
                  Predicted — Model output
                </span>
                <span className="legendItem">
                  <span style={{
                    display: "inline-block", width: 10, height: 10,
                    borderRadius: "50%", background: "#ff4060",
                    border: "1.5px solid #fff", marginRight: 8, flexShrink: 0
                  }}></span>
                  Anomaly — Detected deviation point
                </span>
              </div>

              {/* Axis Labels */}
              <div className="axisLabels">
                <span className="axisLabel xLabel">
                  X-axis: Time Step — sequential index of each sensor observation
                </span>
                <span className="axisLabel yLabel">
                  Y-axis: Fused Sensor Value — weighted mean of selected sensor readings (e.g. temperature + vibration)
                </span>
              </div>

              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={chartData} margin={{ top: 4, right: 16, left: 10, bottom: 30 }}>
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis
                    dataKey="index"
                    tick={{ fontSize: 11 }}
                    label={{
                      value: "Time Step (Observation Index)",
                      position: "insideBottom",
                      offset: -16,
                      style: { fill: "#8aa0be", fontSize: 11 }
                    }}
                  />

                  <YAxis
                    tick={{ fontSize: 11 }}
                    label={{
                      value: "Fused Sensor Value",
                      angle: -90,
                      position: "insideLeft",
                      offset: 10,
                      style: { fill: "#8aa0be", fontSize: 11 }
                    }}
                  />

                  <Tooltip
                    formatter={(value, name) => {
                      if (value == null) return "—";
                      if (name === "anomaly") return "Anomaly";
                      return Number(value).toFixed(2);
                    }}
                    labelFormatter={(label) => `Time Step: ${label}`}
                    contentStyle={{
                      background: "#080f1c",
                      border: "1px solid rgba(0,200,255,0.35)",
                      borderRadius: "8px",
                      fontFamily: "'Space Mono', monospace",
                      fontSize: "12px",
                    }}
                  />

                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="#00c8ff"
                    strokeWidth={2.5}
                    dot={false}
                  />

                  <Line
                    type="monotone"
                    dataKey="predicted"
                    stroke="#ff4060"
                    strokeWidth={2.5}
                    dot={false}
                    strokeDasharray="5 3"
                  />

                  <Line
                    type="monotone"
                    dataKey="anomaly"
                    stroke="none"
                    dot={{ r: 6, fill: "#ff4060", stroke: "#ffffff", strokeWidth: 1 }}
                    activeDot={{ r: 8 }}
                  />

                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Explain Button */}
          {result && (
            <div className="actions">
              <button
                className="primaryBtn"
                onClick={generateExplanation}
                disabled={explLoading}
              >
                {explLoading ? "Generating…" : "⚡ Generate AI Explanation"}
              </button>
            </div>
          )}

          {/* Explanation */}
          {explanation && (
            <div className="explanation">
              <h2>AI Explanation</h2>
              <pre>{explanation}</pre>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default Dashboard;