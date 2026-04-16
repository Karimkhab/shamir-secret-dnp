# Shamir Secret Sharing (Distributed System)

This project implements **Shamir Secret Sharing** in a **distributed architecture** using FastAPI and RabbitMQ.

It demonstrates how a cryptographic algorithm can be integrated into an asynchronous system with message brokers.

---

## Overview

- Split a secret into multiple shares
- Recover the secret from a subset of shares (threshold-based)
- Validate reconstruction using SHA-256 hash
- Process tasks asynchronously via RabbitMQ

---

## Architecture

```mermaid
flowchart LR
    classDef blue fill:#f0f6ff,stroke:#3b82f6,color:#000;

    UI["Frontend (React)"]:::blue
    API["FastAPI API"]:::blue
    MQ["RabbitMQ"]:::blue
    WORKER["Worker"]:::blue

    UI --> API
    API --> MQ
    MQ --> WORKER
````

---

## Message Flow

```mermaid
flowchart LR
    CLIENT["Client"] --> API["API"]
    API -->|publish| MQ["Queue"]
    MQ -->|consume| WORKER["Worker"]
    WORKER --> RESULT["Result"]
```

---

## Project Structure

```
src/
├── api/        # FastAPI endpoints (split / recover)
├── broker/     # RabbitMQ publisher
├── worker/     # Background worker (processing tasks)
├── shamir/     # Core Shamir algorithm (math + logic)
├── frontend/   # React UI
```

---

## Components

### 🔹 API (FastAPI)

* Accepts client requests
* Sends tasks to RabbitMQ
* Does not perform heavy computation

### 🔹 RabbitMQ

* Message broker
* Decouples API and worker
* Enables async processing

### 🔹 Worker

* Consumes tasks from queue
* Executes:

  * `split_secret`
  * `recover_secret`
* Logs results

### 🔹 Shamir Core

* Polynomial-based secret sharing
* Lagrange interpolation for recovery
* Hash validation for correctness

---

## Security

* Finite field arithmetic: `GF(p)` where `p > secret`
* Cryptographically secure randomness (`secrets`)
* Integrity check via SHA-256

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Start RabbitMQ

```bash
brew services start rabbitmq
```

---

### 3. Run worker

```bash
cd src
python -m worker.worker
```

---

### 4. Run API

```bash
cd src
python -m uvicorn api.main:app --reload
```

---

### 5. Example request

```bash
curl -X POST http://127.0.0.1:8000/api/v1/secrets/split \
-H "Content-Type: application/json" \
-d '{
  "secret": "hello",
  "threshold": 3,
  "total_shares": 5
}'
```

---

## 📌 Notes

* Processing is asynchronous (via RabbitMQ)
* Worker handles computation independently
* API returns immediately after publishing task

---

## 🎯 Summary

This project demonstrates:

* Shamir Secret Sharing implementation
* Integrity validation using hashing
* Distributed processing with message broker
* Clear separation between API and computation layers

