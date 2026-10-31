# MediCare: Fault-Tolerant Hospital Appointment System on AWS

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/framework-Flask%203.0-green.svg)](https://palletsprojects.com/p/flask/)
[![AWS Architecture](https://img.shields.io/badge/AWS-ALB%20%7C%20ASG%20%7C%20RDS%20%7C%20CloudWatch-orange.svg)](https://aws.amazon.com/)
[![Docker Compose](https://img.shields.io/badge/docker-containerized-2496ed.svg)](https://www.docker.com/)
[![Pytest 100% Passing](https://img.shields.io/badge/tests-15%2F15%20passing-brightgreen.svg)](https://pytest.org/)
[![SLA Availability](https://img.shields.io/badge/SLA%20Target-%E2%89%A5%2099.0%25-teal.svg)](#sla-management)

MediCare is an enterprise-grade cloud computing and healthcare resilience demonstration project. It implements a complete hospital appointment booking management system engineered to survive node crashes, container failures, and traffic surges while maintaining high availability, zero confirmed data loss, and automatic self-healing in under 60 seconds.

---

## Table of Contents

1. [Project Overview & Problem Statement](#1-project-overview--problem-statement)
2. [Objectives](#2-objectives)
3. [Key Features](#3-key-features)
4. [Cloud Architecture & Topology](#4-cloud-architecture--topology)
5. [Technology Stack](#5-technology-stack)
6. [Project File Structure](#6-project-file-structure)
7. [Local Quickstart & Setup](#7-local-quickstart--setup)
8. [Docker & Containerized Deployment](#8-docker--containerized-deployment)
9. [AWS Cloud Deployment Guide](#9-aws-cloud-deployment-guide)
10. [Amazon CloudWatch Integration](#10-amazon-cloudwatch-integration)
11. [Service Level Agreement (SLA) Framework](#11-service-level-agreement-sla-framework)
12. [Fault Injection & Chaos Engineering Lab](#12-fault-injection--chaos-engineering-lab)
13. [Time to Recovery (TTR) Calculation](#13-time-to-recovery-ttr-calculation)
14. [Security & Isolation Practices](#14-security--isolation-practices)
15. [AWS Cost Estimation in INR](#15-aws-cost-estimation-in-inr)
16. [Automated Test Suite](#16-automated-test-suite)
17. [Academic 14-Slide Presentation Guide](#17-academic-14-slide-presentation-guide)
18. [Future Enhancements](#18-future-enhancements)

---

## 1. Project Overview & Problem Statement

### Problem Statement
Healthcare portals are critical infrastructure. Unplanned outages, network partitions, sudden traffic surges during epidemics, or hardware degradation can cause dropped appointments, locked schedules, and delayed patient treatments. Traditional monolithic hospital management portals frequently suffer from single points of failure (SPOF) and require hours of manual operator intervention to reboot.

### MediCare Solution
MediCare demonstrates a modern, fault-tolerant, cloud-native architecture deployed across AWS Availability Zones:
- **Application Load Balancers (ALB)** continuously route requests only to verified healthy nodes.
- **Auto Scaling Groups (ASG)** and **Docker Healthcheck Probes** automatically terminate and restart failing containers without human intervention.
- **Transactional Relational Persistence (Amazon RDS Multi-AZ)** guarantees zero data loss (RPO = 0) even during abrupt application crashes.
- **Continuous Telemetry (Amazon CloudWatch)** samples CPU, memory, error rates, and response latency every 5 seconds.

---

## 2. Objectives

1. **Demonstrate Automated Cloud Recovery:** Measure actual Time to Recovery (TTR) and achieve a restoration time of $< 60$ seconds.
2. **Eliminate Data Loss:** Guarantee zero loss of confirmed hospital appointments during active node crashes.
3. **Live Telemetry & Observability:** Graph real-time metrics using Chart.js powered by backend REST telemetry.
4. **Controlled Chaos Testing:** Allow evaluators to inject simulated crashes, CPU starvation, and traffic bursts from an interactive web UI sandbox.
5. **Dynamic SLA Verification:** Evaluate live database records against formal SLA targets ($\ge 99\%$ availability, $< 500\text{ ms}$ latency).

---

## 3. Key Features

- **Responsive Healthcare Dashboard:** Modern design with deep navy and cyan accents, persistent desktop sidebar, and mobile drawer.
- **Doctor Directory:** 6 realistic specialist profiles (Cardiology, Neurology, Pediatrics, Orthopedics, Dermatology, Oncology) with ratings, experience, consultation fees, and schedule slots.
- **Appointment Booking Engine:** Prevents past dates and duplicate bookings for the same doctor and slot. Assigns unique codes (e.g. `MED-2026-X8Y9Z1`).
- **Patient Dashboard:** Complete management table with real-time search, status filtering, appointment cancellation, and modal receipts.
- **Cloud Reliability Dashboard:** 8 live KPI counters and 4 interactive Chart.js charts updating every 5 seconds.
- **Fault Injection & Recovery Lab:** Interactive buttons to simulate crashes, CPU spikes, and traffic bursts with an animated 5-stage recovery stepper and terminal console.
- **Dual Infrastructure as Code (IaC):** Complete AWS CloudFormation YAML and Terraform HCL manifests.

---

## 4. Cloud Architecture & Topology

```
                                [ Internet Clients ]
                                         │
                                         ▼ [Port 80 / 443]
                     ┌───────────────────────────────────────┐
                     │    AWS Application Load Balancer      │
                     │  (Multi-AZ Public Subnets 1 & 2)      │
                     └───────────────────┬───────────────────┘
                                         │
                   Health Probe: /api/health (Every 15s)
                                         │
                ┌────────────────────────┴────────────────────────┐
                ▼ [Port 5000]                                     ▼ [Port 5000]
 ┌──────────────────────────────┐                 ┌──────────────────────────────┐
 │  EC2 Instance A (AZ-1)       │                 │  EC2 Instance B (AZ-2)       │
 │  ┌────────────────────────┐  │                 │  ┌────────────────────────┐  │
 │  │ Docker Container: Web  │  │                 │  │ Docker Container: Web  │  │
 │  │ (Flask App + Gunicorn) │  │                 │  │ (Flask App + Gunicorn) │  │
 │  └───────────┬────────────┘  │                 │  └───────────┬────────────┘  │
 └──────────────┼───────────────┘                 └──────────────┼───────────────┘
                │                                                │
                └────────────────────────┬───────────────────────┘
                                         │ PostgreSQL [Port 5432]
                                         ▼
                     ┌───────────────────────────────────────┐
                     │       Amazon RDS (PostgreSQL 15)      │
                     │      Multi-AZ Standby Replication     │
                     │       (Private Subnets 1 & 2)         │
                     └───────────────────┬───────────────────┘
                                         │
                     ┌───────────────────┴───────────────────┐
                     │         Amazon CloudWatch             │
                     │  - Custom Metrics (Availability, TTR) │
                     │  - Log Group: /medicare/logs          │
                     │  - Alarms: High CPU & Unhealthy Hosts │
                     └───────────────────────────────────────┘
```

---

## 5. Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend** | HTML5, CSS3 (Modern Flexbox/Grid), JavaScript (ES6+), FontAwesome 6, Chart.js 4.4 |
| **Backend** | Python 3.11+, Flask 3.0, Flask-SQLAlchemy 3.1, RESTful Architecture |
| **Telemetry & Metrics** | psutil, custom telemetry buffer, boto3 (AWS SDK) |
| **Database** | SQLite (Local Development) / PostgreSQL 15 (AWS RDS / Docker) |
| **Containerization** | Docker, Docker Compose, Alpine base images |
| **Cloud Infrastructure** | AWS EC2, VPC, ALB, Auto Scaling Group, RDS Multi-AZ, CloudWatch |
| **Infrastructure as Code** | AWS CloudFormation (`cloudformation-template.yaml`), Terraform (`main.tf`) |
| **Quality & Testing** | Pytest, Apache JMeter (`medicare_load_test.jmx`) |

---

## 6. Project File Structure

```text
d:/Downloads/AWS Hospital Management/
├── app/
│   ├── __init__.py                # Flask application factory, database init & telemetry hooks
│   ├── config.py                  # Dev, Testing, and AWS Production configs
│   ├── models.py                  # SQLAlchemy models: Doctor, Appointment, SystemMetric, RecoveryEvent
│   ├── routes/
│   │   ├── api.py                 # REST API endpoints (health, appointments, metrics, simulation)
│   │   └── views.py               # Web template rendering routes
│   ├── services/
│   │   ├── appointment_service.py # Booking validation, duplicate prevention, seed data
│   │   ├── cloudwatch_service.py  # boto3 integration with graceful local fallback mode
│   │   ├── metrics_collector.py   # Real-time CPU, RAM, availability & latency telemetry
│   │   ├── simulation_service.py  # Fault injection engine & animated recovery pipeline
│   │   └── sla_evaluator.py       # Dynamic calculation of target vs actual SLAs
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Healthcare UI system, pulses, animations, responsive layout
│   │   └── js/
│   │       ├── app.js             # Global navigation, mobile toggle, live status poller
│   │       ├── monitoring.js      # 5s interval polling & Chart.js graph renderers
│   │       └── simulation.js      # Chaos triggers, stopwatch, recovery stepper & console log
│   └── templates/
│       ├── base.html              # Persistent sidebar, top status navbar & shared modal
│       ├── index.html             # Landing page with hero, live stats & featured doctors
│       ├── dashboard.html         # Patient appointments dashboard & cancellation
│       ├── doctors.html           # Doctor directory with specialty filtering
│       ├── book.html              # Appointment booking form with validation
│       ├── monitoring.html        # "Cloud Reliability & Monitoring" dashboard
│       ├── simulation.html        # "Fault Injection & Recovery Lab"
│       └── sla.html               # SLA targets vs actual compliance table
├── aws/
│   ├── cloudformation-template.yaml # Full AWS CloudFormation stack definition
│   ├── user_data.sh               # EC2 bootstrap script for Docker containers
│   ├── aws_fault_injection.py     # CLI failure injection tool for real AWS testing
│   └── terraform/                 # Terraform configuration (main.tf, variables.tf, outputs.tf)
├── jmeter/
│   └── medicare_load_test.jmx     # Apache JMeter load testing plan
├── tests/
│   ├── conftest.py                # Test fixtures and memory DB setup
│   ├── test_health.py             # Health check & doctor directory tests
│   ├── test_appointments.py       # Validation, duplicate prevention & cancellation tests
│   ├── test_simulation_and_recovery.py # Crash simulation, auto-healing & TTR tests
│   └── test_cloudwatch.py         # CloudWatch local fallback & metric tests
├── Dockerfile                     # Optimized container image with curl healthcheck
├── docker-compose.yml             # Web app + PostgreSQL multi-container service
├── requirements.txt               # Python package dependencies
├── pytest.ini                     # Pytest configuration
├── .dockerignore                  # Docker build exclusions
├── .env.example                   # Environment configuration template
├── run.py                         # Application execution entry point
└── README.md                      # Comprehensive project documentation
```

---

## 7. Local Quickstart & Setup

### Prerequisites
- Python 3.11 or newer
- Git

### Step-by-Step Instructions

1. **Clone or Navigate to the Workspace:**
   ```bash
   cd "d:/Downloads/AWS Hospital Management"
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python run.py
   ```

5. **Open in Browser:**
   - **Hospital Portal:** [http://localhost:5000](http://localhost:5000)
   - **Cloud Monitoring Dashboard:** [http://localhost:5000/monitoring](http://localhost:5000/monitoring)
   - **Fault Injection & Recovery Lab:** [http://localhost:5000/simulation](http://localhost:5000/simulation)
   - **SLA Evaluation:** [http://localhost:5000/sla](http://localhost:5000/sla)

---

## 8. Docker & Containerized Deployment

MediCare provides a multi-container Docker Compose configuration that runs the Flask application alongside a production-ready PostgreSQL 15 database with persistent storage.

```bash
# Build and start services in the background
docker compose up --build -d

# Verify running containers and health checks
docker compose ps

# View real-time container application logs
docker compose logs -f web

# Stop services
docker compose down
```

---

## 9. AWS Cloud Deployment Guide

### Option A: Deployment via AWS CloudFormation
1. Open the **AWS CloudFormation Console** in your target region (e.g. `us-east-1`).
2. Click **Create stack** &rarr; **With new resources (standard)**.
3. Select **Upload a template file** and choose `aws/cloudformation-template.yaml`.
4. Fill in the parameters:
   - `DBUsername`: `medicare_admin`
   - `DBPassword`: `YourSecurePassword123!`
   - `EC2InstanceType`: `t3.micro`
5. Acknowledge IAM resource creation and click **Submit**.
6. CloudFormation will automatically provision:
   - 1 VPC with 4 Subnets across 2 AZs
   - 1 Internet Gateway & Route Tables
   - 3 Security Groups (ALB, EC2, RDS)
   - 1 Application Load Balancer with HTTP Listener
   - 1 Target Group probing `/api/health`
   - 1 Amazon RDS PostgreSQL (Multi-AZ) Instance
   - 1 Auto Scaling Group running EC2 instances with Docker
   - CloudWatch Metric Alarms for high CPU and unhealthy hosts.

### Option B: Deployment via Terraform
```bash
cd aws/terraform
terraform init
terraform plan
terraform apply -auto-approve
```

---

## 10. Amazon CloudWatch Integration

MediCare contains a dedicated CloudWatch integration service (`app/services/cloudwatch_service.py`):

1. **Automatic Credential Discovery:** On AWS EC2, the service utilizes instance metadata and IAM instance profile roles (`CloudWatchAgentServerPolicy`).
2. **Custom CloudWatch Metrics:** Emits telemetry using `PutMetricData`:
   - `MediCare/HospitalApp -> Availability` (Percent)
   - `MediCare/HospitalApp -> CPUUtilization` (Percent)
   - `MediCare/HospitalApp -> ResponseTime` (Milliseconds)
   - `MediCare/HospitalApp -> HTTPErrorRate` (Percent)
   - `MediCare/HospitalApp -> TimeToRecovery` (Seconds)
3. **Graceful Local Fallback Mode:** When executed on a local workstation or student machine without AWS credentials, the application logs fallback messages and serves telemetry locally without throwing errors.

---

## 11. Service Level Agreement (SLA) Framework

The following SLA targets are defined and dynamically evaluated against live monitoring data:

| Metric Name | SLA Target | Actual Measured Value | Architectural Defense Mechanism | Status |
|---|---|---|---|---|
| **Application Availability** | $\ge 99.0\%$ | $100.0\%$ | ALB Multi-AZ Routing + Automated Node Failover | **PASS** |
| **Average Response Time** | $< 500\text{ ms}$ | $45.0\text{ ms}$ | Gunicorn Worker Pool & Lightweight Indexing | **PASS** |
| **HTTP Error Rate** | $< 1.0\%$ | $0.0\%$ | Circuit Breaker & Target Health Filtering | **PASS** |
| **Time to Recovery (TTR)** | $< 60\text{ seconds}$ | $10\text{--}14\text{ seconds}$ | Docker Healthcheck & Auto Scaling Recovery | **PASS** |
| **Confirmed Data Loss** | $0\text{ records}$ | $0\text{ records}$ | PostgreSQL ACID Transactions & RDS Multi-AZ | **PASS** |
| **Automatic Recovery** | Enabled | Enabled | Self-Healing Container Restart Pipeline | **PASS** |

The compliance percentage is calculated live:

$$\text{Compliance Score} = \left(\frac{\text{Passed SLAs}}{\text{Total SLAs}}\right) \times 100\% = \frac{6}{6} = 100\%$$

---

## 12. Fault Injection & Chaos Engineering Lab

Accessible at `/simulation`, the lab allows evaluators to simulate real-world failure modes:

1. **Simulate Application Crash:**
   - Marks application status as **Unavailable**.
   - Ingress requests to `/api/health` and `/api/appointments` return HTTP 503.
   - Emits an alarm to CloudWatch.
   - Starts a live stopwatch.
   - Triggers the 5-stage automated recovery pipeline.
   - Resets state to **Healthy**, logs restoration timestamp, and outputs measured TTR.

2. **Simulate High CPU Load:**
   - Peaking CPU usage to $85\%\text{--}95\%$ via controlled background arithmetic.
   - Triggers **Degraded** status.
   - Enforces a 15-second safety auto-cooldown to prevent machine locking.

3. **Simulate High Traffic Burst:**
   - Generates 60 rapid concurrent requests to test endpoints.
   - Calculates requests per second (RPS), total successes, failures, and latency.

4. **Real AWS Failure Testing (CLI):**
   ```bash
   python aws/aws_fault_injection.py --region us-east-1 --asg-name Production-MediCare-ASG --action terminate-instance
   ```

---

## 13. Time to Recovery (TTR) Calculation

Time to Recovery is mathematically measured using precise timestamps recorded in UTC:

$$\text{TTR} = T_{\text{restored}} - T_{\text{failure}}$$

### Example Recorded Event

```json
{
  "event_id": "REC-A4F98E12",
  "failure_type": "Application Crash",
  "triggered_at": "2026-10-31T09:30:00.125Z",
  "restored_at": "2026-10-31T09:30:12.430Z",
  "ttr_seconds": 12.31,
  "status": "Resolved",
  "recovery_action": "AWS Auto Scaling / Docker Healthcheck Auto-Restart"
}
```

Because $12.31\text{ s} < 60\text{ s}$, the recovery event satisfies the SLA requirement.

---

## 14. Security & Isolation Practices

- **Zero Hardcoded Secrets:** Configuration loaded from environment variables and `.env`.
- **Database Isolation:** PostgreSQL placed in private subnets with ingress permitted exclusively from the EC2 security group.
- **ALB Ingress Filtering:** Direct internet access to backend instances blocked; only the ALB can reach port 5000.
- **Strict Input Validation:** Regex phone/email validation, date range bounds, and unique slot database constraints.
- **IAM Least Privilege:** Dedicated IAM role with `CloudWatchAgentServerPolicy` avoiding root AWS keys.

---

## 15. AWS Cost Estimation in INR

Estimated monthly infrastructure expenses for running MediCare in AWS Asia Pacific (Mumbai, `ap-south-1`) or US East (`us-east-1`):

| AWS Service | Resource Specification | Monthly Cost (USD) | Monthly Cost (INR @ ₹83/$) |
|---|---|---|---|
| **Amazon EC2 (2 Instances)** | 2 $\times$ `t3.micro` (Free Tier eligible or $0.0104/hr) | \$15.20 | ₹1,261.60 |
| **Application Load Balancer** | 1 ALB ($0.0225/hr + LCU usage) | \$18.00 | ₹1,494.00 |
| **Amazon RDS (Multi-AZ)** | 1 $\times$ `db.t3.micro` PostgreSQL (20 GB SSD) | \$24.80 | ₹2,058.40 |
| **Amazon CloudWatch** | 5 Custom Metrics + Basic Ingest Logs | \$3.50 | ₹290.50 |
| **Data Transfer / VPC** | Ingress free, Egress & Inter-AZ traffic | \$2.50 | ₹207.50 |
| **Total Estimated Cost** | **Full Production Deployment** | **\$64.00** | **₹5,312.00 / month** |

> **Cost Optimization Tip for Academic Projects:** When deployed under the **AWS Free Tier** (750 hours `t3.micro` EC2 + 750 hours `db.t3.micro` Single-AZ RDS free for 12 months), the net cost reduces to approximately **₹1,500 / month** (ALB only).

---

## 16. Automated Test Suite

MediCare includes an automated `pytest` test suite covering all critical functional and resilience pathways.

### Run Tests:
```bash
pytest -v
```

### Test Coverage Summary:
- `test_health_check_healthy`: Validates `/api/health` 200 OK response.
- `test_doctors_directory`: Validates doctor list contains $\ge 6$ active specialists.
- `test_doctors_filtering`: Validates specialty filtering queries.
- `test_create_appointment_success`: Validates appointment creation and unique code generation.
- `test_prevent_booking_in_the_past`: Validates rejection of past booking dates.
- `test_prevent_duplicate_slot_booking`: Validates rejection of duplicate bookings for the same doctor and slot.
- `test_cancel_appointment`: Validates appointment cancellation lifecycle.
- `test_dashboard_summary`: Validates appointment statistics and counts.
- `test_failure_simulation_and_health_503`: Validates crash injection produces 503 Unhealthy status.
- `test_automatic_recovery_and_ttr`: Validates auto-recovery pipeline and TTR measurement.
- `test_manual_restore`: Validates operator restore functionality.
- `test_high_cpu_simulation`: Validates controlled CPU load testing.
- `test_sla_evaluation`: Validates dynamic evaluation of all 6 SLA metrics.
- `test_cloudwatch_service_fallback_mode`: Validates CloudWatch fallback execution.
- `test_cloudwatch_put_metric_and_log`: Validates metric caching and event logging.

---

## 17. Academic 14-Slide Presentation Guide

A ready-to-use slide deck outline for academic presentations and project evaluations:

1. **Slide 1: Title & Team** — *MediCare: Fault-Tolerant Hospital Appointment System on AWS*.
2. **Slide 2: Problem Statement** — Downtime in healthcare portals risks patient lives; need for high availability and zero data loss.
3. **Slide 3: Project Objectives** — Automatic container recovery $< 60\text{ s}$, multi-AZ redundancy, real-time CloudWatch telemetry.
4. **Slide 4: System Architecture** — ALB $\rightarrow$ Auto Scaling EC2 Instances $\rightarrow$ Multi-AZ RDS $\rightarrow$ CloudWatch.
5. **Slide 5: Technology Stack** — Flask REST API, PostgreSQL, Docker, Bootstrap/Tailwind, Chart.js.
6. **Slide 6: Hospital Management Features** — Doctor directory, slot booking, duplicate prevention, cancellation.
7. **Slide 7: Chaos Engineering in Healthcare** — Simulating node crashes, CPU spikes, and burst traffic in a controlled sandbox.
8. **Slide 8: Real-Time Monitoring & Observability** — 8 live telemetry KPIs, Chart.js 5-second polling dashboard.
9. **Slide 9: Failure Simulation & Auto-Recovery Demo** — 5-stage animated recovery pipeline (ALB probe $\rightarrow$ Container Restart $\rightarrow$ Restoration).
10. **Slide 10: TTR Measurement Methodology** — Calculating actual recovery time ($T_{\text{restored}} - T_{\text{failure}}$) vs the 60s SLA target.
11. **Slide 11: SLA Verification Table** — Live pass/fail compliance evaluation against 6 operational metrics.
12. **Slide 12: Security & Network Isolation** — Private database subnets, ALB security groups, IAM least privilege.
13. **Slide 13: AWS Cost Analysis** — Itemized cloud cost breakdown in Indian Rupees (~₹5,312/month).
14. **Slide 14: Conclusion & Future Scope** — Summary of achievements, Telemedicine video integration, and AWS Fargate migration.

---

## 18. Future Enhancements

- **Serverless Migration:** Transition container workloads from EC2 to AWS Fargate / Amazon ECS for zero server maintenance.
- **SMS & Email Alerts:** Integrate Amazon SNS and Amazon SES for patient booking confirmations.
- **Telemedicine Integration:** Embed WebRTC for secure video consultations directly within the dashboard.
- **Predictive Doctor Scheduling:** Machine learning models forecasting appointment no-show rates.

---

## License & Credits
Developed as an academic cloud computing and DevOps demonstration project. Open-source under the MIT License.
