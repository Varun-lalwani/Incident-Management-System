import { useEffect, useState } from "react";
import { getIncidents } from "../api/incidents";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const [incidents, setIncidents] = useState([]);

  const loadIncidents = async () => {
    const data = await getIncidents();
    setIncidents(data);
  };

  useEffect(() => {
    loadIncidents();

    const interval = setInterval(() => {
      loadIncidents();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>IMS Dashboard</h1>

      {incidents.map((incident) => (
        <Link
          key={incident.incident_id}
          to={`/incident/${incident.incident_id}`}
        >
          <div>
            <h3>{incident.incident_id}</h3>
            <p>{incident.component_id}</p>
            <p>{incident.severity}</p>
            <p>{incident.state}</p>
          </div>
        </Link>
      ))}
    </div>
  );
}