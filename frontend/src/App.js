import { Routes, Route, Navigate } from "react-router-dom";
import { ModelProvider } from "./context/ModelContext";
import { useEffect, useState } from "react";
import { auth } from "./firebase";
import { onAuthStateChanged } from "firebase/auth";

import Login     from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Models    from "./pages/Models";
import Reports   from "./pages/Reports";
import Settings  from "./pages/Settings";

function App() {
  const [user, setUser]       = useState(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      setUser(u || null);
      setChecking(false);
    });
    return () => unsub();
  }, []);

  if (checking) return null; // wait for auth before rendering

  if (!user) return <Login />;

  return (
    <ModelProvider>
      <Routes>
        <Route path="/"         element={<Dashboard />} />
        <Route path="/models"   element={<Models />}    />
        <Route path="/reports"  element={<Reports />}   />
        <Route path="/settings" element={<Settings />}  />
        <Route path="*"         element={<Navigate to="/" />} />
      </Routes>
    </ModelProvider>
  );
}

export default App;