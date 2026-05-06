import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getIncidents } from "../api/incidents";

export default function IncidentList() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const loadIncidents = async () => {
    try {
      setLoading(true);
      const data = await getIncidents();

      setIncidents(Array.isArray(data) ? data : data.data);
    } catch (err) {
      setError("Failed to load incidents");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIncidents();

    const interval = setInterval(loadIncidents, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading incidents...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Incidents</h1>

      {incidents.length === 0 ? (
        <p>No incidents found</p>
      ) : (
        incidents.map((incident) => (
          <div
            key={incident.incident_id}
            onClick={() =>
              navigate(`/incidents/${incident.incident_id}`)
            }
            style={{
              border: "1px solid #ccc",
              padding: "12px",
              marginBottom: "10px",
              cursor: "pointer",
              borderRadius: "6px"
            }}
          >
            <h3>{incident.incident_id}</h3>
            <p><b>Component:</b> {incident.component_id}</p>
            <p><b>Severity:</b> {incident.severity}</p>
            <p><b>State:</b> {incident.state}</p>

            <p>
              <b>MTTR:</b>{" "}
              {incident.mttr_seconds !== null
                ? `${incident.mttr_seconds} sec`
                : "N/A"}
            </p>
          </div>
        ))
      )}
    </div>
  );
}