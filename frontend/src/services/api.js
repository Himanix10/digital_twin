import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

export const runModel = (data) => API.post("/run-model", data);

export const explainAI = (data) => API.post("/explain", data);