from abc import ABC


class IncidentState(ABC):
    name = "BASE"
    allowed_transitions = []

    def can_transition(self, next_state: str):
        return next_state in self.allowed_transitions


class OpenState(IncidentState):
    name = "OPEN"
    allowed_transitions = ["INVESTIGATING"]


class InvestigatingState(IncidentState):
    name = "INVESTIGATING"
    allowed_transitions = ["RESOLVED"]


class ResolvedState(IncidentState):
    name = "RESOLVED"
    allowed_transitions = ["CLOSED"]


class ClosedState(IncidentState):
    name = "CLOSED"
    allowed_transitions = []