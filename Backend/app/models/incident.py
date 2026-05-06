from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import Text, String, Integer, DateTime
from app.services.postgres import Base

class Incident(Base):

    __tablename__ = "incidents"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    incident_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    component_id: Mapped[str] = mapped_column(String)

    severity: Mapped[str] = mapped_column(String, nullable=False)

    state: Mapped[str] = mapped_column(String, default="OPEN", nullable=False)

   #Use the callable default to ensure the timestamp is generated at the time of record creation
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc),
        nullable=False
        )
    
    root_cause: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    fix_applied: Mapped[str | None] = mapped_column(Text, nullable=True)

    prevention_steps: Mapped[str | None] = mapped_column(Text, nullable=True)

    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    mttr_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
