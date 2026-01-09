
# EcoOps - Intelligent Waste Management System

EcoOps is a comprehensive platform designed to optimize municipal waste collection through data-driven insights. 

**Current Status**: Phase 1 (Core API & Data) is complete.

## 🚀 Key Features (V1)
*   **Robust Backend**: built with **FastAPI** for high performance and auto-documentation.
*   **Smart Data Modeling**: Relational schema handling **Areas**, **Waste Logs**, and **Trucks** using **SQLModel** (SQLAlchemy + Pydantic).
*   **Reliable Storage**: **PostgreSQL** database containerized for consistency.
*   **Data Simulation**: Built-in seeder capable of generating **100,000+** realistic waste records contextually relevant to **South West Nigeria** (Lagos, Ibadan, etc.).
*   **Automated Testing**: Comprehensive test suite using **Pytest**.
*   **Developer Friendly**: Makefile for one-command setup.

## 🛠 Tech Stack
*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **Database**: PostgreSQL 15
*   **ORM**: SQLModel / SQLAlchemy
*   **Migrations**: Alembic
*   **Testing**: Pytest
*   **Infrastructure**: Docker & Docker Compose

## ⚡️ Quick Start

### Prerequisites
*   Docker & Docker Compose

### 1. Start the System
```bash
make up
# OR
docker compose up -d --build
```

### 2. Verify Installation
Check the API health:
```bash
curl http://localhost:8000/health
# {"status": "ok"}
```
Access the interactive API docs at: `http://localhost:8000/docs`

### 3. Seed Data (Optional)
Populate the database with 100k synthetic records (Nigerian Context):
```bash
make seed
```

### 4. Run Tests
Execute the automated test suite:
```bash
make test
```

## 📡 API Usage Examples

### Create a New Area
```bash
curl -X 'POST' \
  'http://localhost:8000/areas/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Ikeja",
  "code": "LAG-001",
  "description": "Lagos Capital - Commercial Hub"
}'
```

### Log Waste Collection
```bash
curl -X 'POST' \
  'http://localhost:8000/logs/' \
  -H 'Content-Type: application/json' \
  -d '{
  "area_id": 1,
  "waste_type": "general",
  "weight_kg": 250.5,
  "truck_id": "TRUCK-005"
}'
```

## 🔮 Roadmap (Phase 2)
*   **Frontend Dashboard**: Vue.js application for visualization.
*   **Data Pipelines**: Apache Airflow for automated ETL.
*   **Machine Learning**: Forecasting models to predict waste generation trends.

## 📂 Project Structure
```
.
├── backend/
│   ├── app/
│   │   ├── main.py        # Entry point
│   │   ├── models.py      # DB Models
│   │   ├── router.py      # API Endpoints
│   │   └── database.py    # DB Setup
│   ├── migrations/        # Alembic versions
│   ├── scripts/
│   │   └── seed.py        # Data generator
│   └── tests/             # Pytest suite
├── docker-compose.yaml
└── Makefile
```
