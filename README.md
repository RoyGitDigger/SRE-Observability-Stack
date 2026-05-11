# SRE Observability & Security Pipeline

A full-stack observability pipeline implementing the **Prometheus + Grafana + Loki** stack. This project mirrors production-grade SRE (Site Reliability Engineering) workflows for monitoring cloud infrastructure and responding to security incidents.

##  Overview

This repository contains a containerized environment that simulates a microservice with:
- **Metrics Scraping**: Prometheus pulls time-series data from a Flask `/metrics` endpoint.
- **Log Aggregation**: Promtail tails structured JSON logs and ships them to Loki.
- **Visual Analytics**: Grafana dashboards for unified observability (Metrics + Logs).
- **Automated Health Checks**: A Python-based external probe that simulates uptime monitoring.

##  Architecture

- **Flask App**: The core service generating metrics (CPU, Memory, Request counts) and structured logs.
- **Prometheus**: Time-series database for monitoring performance SLIs (Service Level Indicators).
- **Loki**: Log-aggregation system tailored for high-volume event storage.
- **Grafana**: The visualization layer, pre-configured with Prometheus and Loki data sources.
- **Promtail**: The agent that captures logs from the application and pushes them to Loki.

##  Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/SRE-Monitor.git
   cd SRE-Monitor
   ```
2. Launch the stack:
   ```bash
   docker-compose up --build -d
   ```
3. Access the dashboards:
   - **Grafana**: [http://localhost:3000](http://localhost:3000) (Admin / Admin)
   - **Prometheus**: [http://localhost:9090](http://localhost:9090)
   - **App Metrics**: [http://localhost:5000/metrics](http://localhost:5000/metrics)

##  Security & Incident Response
The stack is designed to detect brute-force attacks via the `/login` endpoint. When multiple authentication failures occur, they are logged as structured JSON and can be visualized/alerted in Grafana using LogQL.

See [docs/incident_response.md](./docs/incident_response.md) for the SRE triage playbook.

---
*Created as part of an InfoSec & SRE deep-dive into cloud-native observability.*
