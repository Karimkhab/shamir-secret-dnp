# Shamir Secret Sharing

This project implements Shamir Secret Sharing for splitting a text secret into
multiple shares and reconstructing it from a threshold number of shares.

The demo backend is a synchronous FastAPI service: the API calls the Shamir core
directly and returns the generated shares or reconstructed secret immediately.

## Overview

- Split a UTF-8 text secret into `total_shares` serialized shares.
- Recover the original secret from at least `threshold` valid shares.
- Use SHA-256 to verify that the reconstructed secret matches the original.
- Log generation and reconstruction metadata for auditability.

## Architecture

```mermaid
flowchart LR
    UI["Frontend / Demo UI"] --> API["FastAPI API"]
    API --> CORE["Shamir Core"]
    CORE --> API
```

The `broker/` and `worker/` modules are kept as optional RabbitMQ experiments,
but they are not required for the main demo flow.

## Project Structure

```text
src/
├── api/        # FastAPI endpoints
├── shamir/     # Core Shamir algorithm
├── frontend/   # UI work area
├── broker/     # Optional RabbitMQ publisher
└── worker/     # Optional RabbitMQ worker
tests/          # Core and API contract tests
```


## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
cd src
python -m uvicorn api.main:app --reload
```

Example split request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/secrets/split \
  -H "Content-Type: application/json" \
  -d '{
    "secret": "hello",
    "threshold": 3,
    "total_shares": 5
  }'
```

Run tests:

```bash
pytest
```

## Validation Checklist

- Hash integrity: `split` returns a SHA-256 hash, and `recover` verifies the reconstructed secret against `expectedHash`.
- Insufficient shares: reconstruction with fewer than `threshold` shares fails with `INVALID_REQUEST`.
- Audit logs: split and recover operations log request metadata such as request id, threshold, and share count without logging the secret value.

## Notes

- Shares are serialized as `threshold:prime:byte_length:x:y`.
- The code uses finite field arithmetic over `GF(p)`, cryptographically secure randomness from `secrets`, and Lagrange interpolation for reconstruction.
- Do not log the original secret or the full list of shares in production logs.

## Links and Articles
- Original [paper](https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf)
- [Visualization](https://iancoleman.io/shamir/)