import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getIncidentById, updateIncidentState } from "../api/incidents";

export default function IncidentDetail() {

  const { incidentId } = useParams();
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadIncident = async () => {
    const data = await getIncidentById(incidentId);
    setIncident(data);
    setLoading(false);
  };

  useEffect(() => {
    loadIncident();

    const interval = setInterval(() => {
      loadIncident();
    }, 5000);

    return () => clearInterval(interval);

  }, [incidentId]);

  const moveToInvestigating = async () => {
    await updateIncidentState(
      incidentId,
      "INVESTIGATING",
      null
    );
    loadIncident();
  };

  const moveToResolved = async () => {
    await updateIncidentState(
      incidentId,
      "RESOLVED",
      null
    );
    loadIncident();
  };

  const closeIncident = async () => {
    await updateIncidentState(
      incidentId,
      "CLOSED",
      {
        root_cause: "DB overload",
        fix_applied: "Scaled cluster",
        prevention_steps: "Add rate limiting"
      }
    );
    loadIncident();
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!incident) {
    return <div>Incident not found</div>;
  }

  return (
    <div>

      <h1>{incident.incident_id}</h1>

      <p>Component: {incident.component_id}</p>
      <p>Severity: {incident.severity}</p>
      <p>State: {incident.state}</p>

      <p><b>MTTR:</b> {incident.mttr_seconds ?? "N/A"} seconds</p>

      <button onClick={moveToInvestigating}>
        Investigating
      </button>

      <button onClick={moveToResolved}>
        Resolve
      </button>

      <button onClick={closeIncident}>
        Close (RCA)
      </button>

      {/* SIGNALS SECTION */}
      <h2>Signals (MongoDB)</h2>

      {incident?.signals?.length > 0 ? (
        incident.signals.map((signal, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ccc",
              margin: "8px",
              padding: "8px"
            }}
          >
            <p><b>Component:</b> {signal.component_id}</p>
            <p><b>Message:</b> {signal.message}</p>
            <p><b>Severity:</b> {signal.severity}</p>
            <p><b>Time:</b> {signal.timestamp}</p>
          </div>
        ))
      ) : (
        <p>No signals found</p>
      )}

    </div>
  );
}