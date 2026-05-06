import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


// GET ALL INCIDENTS
export const getIncidents = async () => {
  const response = await API.get("/incidents");
  return response.data;
};


// GET SINGLE INCIDENT
export const getIncidentById = async (incidentId) => {
  const response = await API.get(`/incidents/${incidentId}`);
  return response.data;
};


// UPDATE STATE
export const updateIncidentState = async (
  incidentId,
  nextState,
  rcaData
) => {
  const response = await API.patch(
    `/incidents/${incidentId}/state`,
    {
      current_state: "RESOLVED", // you can later make this dynamic
      next_state: nextState,
      rca_data: rcaData
    }
  );

  return response.data;
};