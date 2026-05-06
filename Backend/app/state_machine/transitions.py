from fastapi import HTTPException
from datetime import datetime, timezone
from app.state_machine.states import (
    OpenState,
    InvestigatingState,
    ResolvedState,
    ClosedState
)

STATE_MAP = {
    "OPEN": OpenState(),
    "INVESTIGATING": InvestigatingState(),
    "RESOLVED": ResolvedState(),
    "CLOSED": ClosedState(),
}


def validate_rca(rca_data):
    required_fields = [
        "root_cause",
        "fix_applied",
        "prevention_steps"
    ]

    for field in required_fields:
        if not rca_data.get(field):
            return False

    return True


def transition_state(current_state, next_state, rca_data, incident):

    current_state = current_state.strip().upper()
    next_state = next_state.strip().upper()

    current = STATE_MAP.get(current_state)

    if current is None:
        raise HTTPException(400, "Invalid current state")

    if not current.can_transition(next_state):
        raise HTTPException(400, f"Invalid transition {current_state} → {next_state}")

    if next_state == "CLOSED":

        if not rca_data or not validate_rca(rca_data):
            raise HTTPException(400, "RCA required to close incident")

        if incident is None:
            raise HTTPException(500, "Incident missing")

        incident.resolved_at = datetime.now(timezone.utc)

        created = incident.created_at
        resolved = incident.resolved_at

        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)

        if resolved.tzinfo is None:
            resolved = resolved.replace(tzinfo=timezone.utc)

        incident.mttr_seconds = int(
            (resolved - created).total_seconds()
        )

    return next_state