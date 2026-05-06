#   INCIDENT MANAGEMENT SYSTEM            

- A real-time Incident Management System built using FastAPI, Redis, and PostgreSQL.

- The system ingests monitoring signals, applies debounce logic to prevent duplicate   incidents, stores active incidents, and exposes APIs for retrieval.


## Overview

Modern infrastructure environments generate massive volumes of monitoring events.  
Without proper event correlation and debouncing, duplicate alerts can rapidly overwhelm operations teams.

This project demonstrates a scalable backend architecture for:

- high-throughput signal ingestion
- incident deduplication
- asynchronous event handling
- persistent incident tracking
- API-driven observability workflows

The system is designed around production-inspired backend patterns using Redis for fast event handling and PostgreSQL for durable incident persistence.

---

## Core Features

- Real-time signal ingestion
- Debounce-based duplicate suppression
- Incident lifecycle management
- Redis-backed queue/cache workflow
- PostgreSQL persistence layer
- RESTful API architecture
- Modular FastAPI service structure
- Dockerized infrastructure setup
- Async-ready backend design

---

## System Architecture

Signal -> Redis -> Debounce -> Incident Creation -> PostgreSQL



                ┌─────────────────┐
                │ React Frontend  │
                └────────┬────────┘
                         │ REST API
                         ▼
               ┌──────────────────┐
               │ FastAPI Backend  │
               └───────┬──────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    ┌────────┐   ┌──────────┐   ┌──────────┐
    │ Redis  │   │ MongoDB  │   │PostgreSQL│
    │ Queue  │   │RawSignals│   │ Incidents│
    └────┬───┘   └──────────┘   └──────────┘
         │
         ▼
   ┌─────────────┐
   │ Async Worker│
   └─────────────┘

---

## Technology Stack

| Component        | Technology |
| ---------------- | ---------- |
| Backend API      | FastAPI    |
| Database         | PostgreSQL |
| Cache / Queue    | Redis      |
| ORM              | SQLAlchemy |
| Containerization | Docker     |
| API Validation   | Pydantic   |
| Async Server     | Uvicorn    |


---

## Functional Workflow 

1.Signal Ingestion
Monitoring systems send signals to: POST /signals
Each signal contains:
- Component identifier
- Severity
- Timestamp
- Event Message

2. Raw Signal Persistence

Incoming monitoring signals are first archived in MongoDB before incident processing.

This enables:

- raw event retention
- auditability
- replay/debugging workflows
- separation of transient events from incident state management

MongoDB is used as a flexible document store for high-volume unstructured signal ingestion.

3. Debounce Processing

Incoming signals are processed through Redis-backed debounce logic.

If multiple identical signals arrive within the configured debounce window:

- Duplicate incidents are suppressed
- Existing incidents are reused
- Unnecessary incident storms are avoided

This simulates real-world alert correlation systems used in SRE and NOC environments.

4. Incident Creation

Validating signals create or update incidents in PostgreSQL.

Incident states include: 

- OPEN 
- CLOSED

Each incident stores: 
- Incident ID
- Component ID
- State
- Timestamps

5. Incident Retrieval APIs

- The system exposes APIs for operational visibility: 

Get all incidents : GET /incidents

Get incident by ID : GET /incidents/{incident_id}

## API Endpoints

'''http
POST /signals
'''
- Accepts incoming monitoring signals.

Example Request:
{
  "component_id": "CACHE_CLUSTER_01",
  "severity": "HIGH",
  "message": "CPU usage exceeded threshold",
  "timestamp": "2026-05-05T10:30:00"
}

'''http
GET /incidents
'''
- Returns all incidents stored in PostgreSQL.

'''http
GET /incidents/{incident_id}
'''
- Returns details for a single incident.

## Project Structure

Backend/
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── workers/
│
├── docker-compose.yml
├── requirements.txt
└── README.md

## Setup Instructions 

1. Clone Repository
'''bash
 git clone <repository-url>
 cd Incident-Management-System
 '''

2. Start Infrastructure Services
'''bash
 docker compose up -d
 '''             

Starts: PostgreSQL, Redis, mongodb

3. Create Python Environment
'''bash
 python -m venv venv
 source venv/bin/activate
'''

4. Install Dependencies
'''bash
 pip install -r requirements.txt
'''

5. Start FastAPI Server
'''bash
 uvicorn app.main:app --reload
'''

API Documentation

- FastAPI automatically exposes Swagger documentation at:
http://localhost:8000/docs


Example Test Request:

curl -X POST http://localhost:8000/signals \
-H "Content-Type: application/json" \
-d '{
  "component_id":"CACHE_CLUSTER_01",
  "severity":"HIGH",
  "message":"CPU spike detected",
  "timestamp":"2026-05-05T10:30:00"
}'

## Design Considerations

| Requirement                 | Solution                |
| --------------------------- | ----------------------- |
| High-throughput ingestion   | FastAPI async endpoints |
| Backpressure handling       | Redis queue             |
| Duplicate suppression       | Redis debounce TTL      |
| Raw signal archival         | MongoDB document storage|
| Persistent incident storage | PostgreSQL              |
| Fast temporary state access | Redis cache             |
| Async-ready processing      | Worker architecture     |
| API observability           | REST endpoints          |
| Containerized deployment    | Docker                  |

## Non-Functional Improvements

The system incorporates multiple production-oriented backend engineering considerations:

- Redis-backed debounce logic for duplicate suppression
- Async-ready FastAPI architecture
- Dockerized infrastructure deployment
- Modular service-oriented backend structure
- Queue-oriented event processing workflow
- PostgreSQL-backed persistent incident storage
- RESTful API design principles
- OpenAPI/Swagger auto-generated API documentation
- Scalable worker-oriented architecture design
- Structured separation of routes, services, and models
- Low-latency Redis cache integration

## Security & Validation

The backend includes multiple foundational security and validation mechanisms:

- Request payload validation using Pydantic schemas
- Strict typed API contracts
- Input validation at API boundary
- Structured backend routing architecture
- Separation of business logic and API layers
- Controlled database access through SQLAlchemy ORM
- Dockerized isolated service deployment
- Rate limiting middleware support for API protection

## Scalability Notes

The current implementation is intentionally modular and can be extended with:

- Kafka/RabbitMQ event streaming
- Distributed workers
- Incident escalation workflows
- Authentication and RBAC
- Metrics and tracing
- WebSocket real-time dashboards
- Kubernetes deployment
- Alert correlation engines

## Future Improvements

- Incident acknowledgement workflows
- SLA tracking
- Retry and dead-letter queues
- Prometheus/Grafana integration
- Distributed tracing
- Event-driven microservices
- CI/CD automation pipeline

## Conclusion

- This project demonstrates the backend architecture of a modern incident management platform using production-inspired engineering patterns.

The system focuses on:

- Reliability
- Scalability
- Operational Efficiency
- Event Deduplication
- Asynchronous Processing
- Clean API Design

while maintaining a modular and extensible architecture suitable for future scaling.


