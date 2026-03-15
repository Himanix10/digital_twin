import { createContext, useContext, useState } from "react";

const ModelContext = createContext(null);

export function ModelProvider({ children }) {
  const [lastRun, setLastRun]     = useState(null);
  const [result, setResult]       = useState(null);
  const [chartData, setChartData] = useState([]);

  return (
    <ModelContext.Provider value={{
      lastRun,   setLastRun,
      result,    setResult,
      chartData, setChartData,
    }}>
      {children}
    </ModelContext.Provider>
  );
}

export function useModelContext() {
  return useContext(ModelContext);
}