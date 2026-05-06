import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import IncidentDetail from "./pages/IncidentDetail";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />

        <Route
          path="/incident/:incidentId"
          element={<IncidentDetail />}
        />
      </Routes>
    </BrowserRouter>
  );
}