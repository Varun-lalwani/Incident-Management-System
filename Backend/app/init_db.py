from app.services.postgres import engine
from app.models.incident import Incident 

Incident.metadata.create_all(bind=engine)

print("Tables created successfully")

