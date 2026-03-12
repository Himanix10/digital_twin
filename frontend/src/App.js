import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Models from "./pages/Models";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";

function App(){

  return(

    <Routes>

      <Route path="/" element={<Dashboard />} />

      <Route path="/models" element={<Models />} />

      <Route path="/reports" element={<Reports />} />

      <Route path="/settings" element={<Settings />} />

    </Routes>

  )

}

export default App