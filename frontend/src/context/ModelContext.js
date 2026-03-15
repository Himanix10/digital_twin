import { createContext, useContext, useState } from "react";

const ModelContext = createContext(null);

export function ModelProvider({ children }) {
  const [lastRun, setLastRun] = useState(null);

  return (
    <ModelContext.Provider value={{ lastRun, setLastRun }}>
      {children}
    </ModelContext.Provider>
  );
}

export function useModelContext() {
  return useContext(ModelContext);
}