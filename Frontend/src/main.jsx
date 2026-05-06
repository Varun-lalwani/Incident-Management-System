import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import IncidentList from "./pages/ IncidentList";
import IncidentDetail from "./pages/ IncidentDetail";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/incidents" element={<IncidentList />} />
      <Route path="/incidents/:incidentId" element={<IncidentDetail />} />
    </Routes>
  </BrowserRouter>
);