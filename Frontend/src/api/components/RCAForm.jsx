import { useState } from "react";
import { updateIncidentState } from "../api/incidents";

export default function RCAForm({ incidentId }) {

  const handleSubmit = async (e) => {
    e.preventDefault();

    await updateIncidentState(
      incidentId,
      "CLOSED",
      form
    );

    alert("Incident closed successfully");
  };

  return (
    <form onSubmit={handleSubmit}>

      <textarea
        placeholder="Root Cause"
        onChange={(e) =>
          setForm({
            ...form,
            root_cause: e.target.value
          })
        }
      />

      <textarea
        placeholder="Fix Applied"
        onChange={(e) =>
          setForm({
            ...form,
            fix_applied: e.target.value
          })
        }
      />

      <textarea
        placeholder="Prevention Steps"
        onChange={(e) =>
          setForm({
            ...form,
            prevention_steps: e.target.value
          })
        }
      />

      <button type="submit">
        Close Incident
      </button>

    </form>
  );
}