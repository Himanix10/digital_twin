import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});


// ─────────────────────────────────────
// RUN MODEL (SIMULATED DATA)
// ─────────────────────────────────────

export const runModel = (data) => {
  return API.post("/run-model", data);
};


// ─────────────────────────────────────
// AI EXPLANATION
// ─────────────────────────────────────

export const explainAI = (data) => {
  return API.post("/explain", data);
};


// ─────────────────────────────────────
// PREVIEW CSV (GET NUMERIC COLUMNS)
// ─────────────────────────────────────

export const previewCSV = (file) => {

  const formData = new FormData();
  formData.append("file", file);

  return API.post("/preview-csv", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};


// ─────────────────────────────────────
// UPLOAD CSV + SELECTED SENSORS
// ─────────────────────────────────────

export const uploadCSV = (file, sensors, model) => {

  const formData = new FormData();

  formData.append("file", file);
  formData.append("sensors", sensors); // comma separated
  formData.append("model", model);

  return API.post("/upload-csv", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};