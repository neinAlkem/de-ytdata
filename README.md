<div align="left">
    <img src="assets/Screenshot 2026-03-12 051520.png" width="100%" align="center" style="margin-right: 15px"/>
    <div style="display: inline-block;">
        <h1 style="display: inline-block; vertical-align: middle; margin-top: 0;">BATCH YOUTUBE CHANNEL DATA STATISTIC PIPELINE</h1>
        <p>
</p>
        <p>
	<!-- Shields.io badges disabled, using skill icons. --></p>
        <p>Built with the tools and technologies:</p>
        <p>
        <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="docker">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python">
        <img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white" alt="airflow">
        <img src="https://img.shields.io/badge/postgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="postgresql">
        <img src="https://img.shields.io/badge/Soda-white?style=for-the-badge" alt="Soda">
        <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="Soda">
	</p>
    </div>
</div>

## Project Overview

de-ytdata is an end-to-end data engineering pipeline built with Apache Airflow that extracts YouTube video statistics and processes them through a structured ETL workflow.
The project simulates a production-style data pipeline where raw API data is collected, stored, transformed, validated, and loaded into a relational data warehouse. It demonstrates how modern data engineering systems orchestrate automated workflows, manage dependencies, and ensure data quality using containerized infrastructure.

### Background

Many organizations rely on data pipelines to collect and transform external data sources into structured datasets for analytics and reporting. APIs such as the YouTube Data API provide valuable information about content performance, engagement metrics, and audience trends.
However, transforming raw API responses into reliable analytics datasets requires several steps:
- Extracting raw data from external APIs
- Persisting raw payloads for reproducibility
- Loading data into structured databases
- Applying transformations and enrichment
- Validating data quality before analytics consumption
- This project demonstrates how these processes can be automated using Apache Airflow orchestration, containerized services, and reproducible infrastructure.

### Project Goal

The main objectives of this project are:
- Build a complete end-to-end ETL pipeline using Apache Airflow
- Extract YouTube channel video statistics through the YouTube Data API
- Persist raw API responses as JSON for traceability
- Load structured data into a Postgres-based data warehouse
- Apply transformations for analytics-ready datasets
- Validate data quality using Soda SQL checks
- Provide a containerized development environment using Docker

## What this project does

- Pulls video statistics from the **YouTube Data API** for a given channel handle
- Persists the raw API response as JSON in `data/video_stats_YYYY-MM-DD.json`
- Loads the JSON into a **Postgres ELT database** (staging + warehouse schemas)
- Applies basic transformations (duration parsing + video type labeling)
- Runs **Soda SQL data quality checks** to validate the warehouse tables

## Project structure

- `dags/` - Airflow DAG definitions (pipeline orchestration)
  - `main.py` - top-level DAG definitions (produce_video_stats, update_db, data_quality_check)
- `dags/api/` - YouTube API extraction logic
- `dags/warehouse/` - Postgres load/transformation logic
- `dags/data_quality_check/` - Soda SQL integration for data quality checks
- `include/soda/` - Soda configuration and checks
- `data/` - Output folder for JSON payloads created by the pipeline
- `docker-compose.yaml` - Local development stack (Airflow + Postgres + Redis)
- `Dockerfile` + `requirements.txt` - Image build definition
- `tests/` - Pytest-based unit + integration tests

## Getting started

### Prerequisites

- Docker (engine)
- Docker Compose
- A **YouTube Data API key** (for `API_KEY`)
- (Optional) A GitHub account if you want to use the included GitHub Actions CI

### Setup (local development)

1. **Configure environment variables**

   Copy or create a `.env` file at the repo root and set the required values.

   ```bash
   cp .env .env.local
   # Edit .env.local with your own credentials
   ```

   Required variables (minimum):

   - `API_KEY`: YouTube Data API key
   - `CHANNEL_HANDLE`: YouTube channel handle to extract stats from
   - `POSTGRES_CONN_HOST`, `POSTGRES_CONN_PORT`: Postgres host/port
   - `POSTGRES_CONN_USERNAME`, `POSTGRES_CONN_PASSWORD`: Postgres admin user (used to create databases)
   - `ELT_DATABASE_*`, `METADATA_DATABASE_*`, `CELERY_BACKEND_*`: DB credentials for Airflow and ELT databases
   - `AIRFLOW_WWW_USER_USERNAME`, `AIRFLOW_WWW_USER_PASSWORD`: Airflow UI credentials

   > ⚠️ This repo includes a `.env` file with example values for local testing, but **do not commit secrets**.

2. **Start the stack**

   ```bash
   docker compose up -d
   ```

3. **Verify Airflow is running**

   Open: http://localhost:8080

   Use the credentials from your `.env` file (`AIRFLOW_WWW_USER_USERNAME` / `AIRFLOW_WWW_USER_PASSWORD`).

4. **Trigger the pipeline**

   - In the Airflow UI, trigger the `produce_video_stats` DAG.
   - This will run the full pipeline: fetch API stats → persist JSON → load to Postgres → run Soda checks.

### Running tests

Tests are designed to run inside the Airflow Docker environment.

```bash
# Start the stack (if not already running)
docker compose up -d

# Run unit + integration tests
docker exec airflow-worker sh -c "pytest tests/ -v"
```

### Quick debug / manual commands

```bash
# Run a DAG without waiting for scheduler (useful for local debugging)
docker exec airflow-worker sh -c "airflow dags test produce_video_stats"

# Inspect generated JSON data
docker exec airflow-worker sh -c "ls -1 /opt/airflow/data"
```
