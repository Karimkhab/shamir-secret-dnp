# Shamir Secret Sharing Frontend

A simple React + TypeScript frontend for the **Shamir Secret Sharing** project.

This UI works as a thin client for the backend API and supports two main flows:

- **Split Secret**
- **Recover Secret**

The frontend does **not** implement the Shamir algorithm itself.  
It only sends requests to the backend and displays the results.

## Features

- Split a text secret into serialized shares
- Recover the original secret from pasted shares
- Clean two-panel layout:
    - input on the left
    - output on the right
- Tooltip help for `Threshold` and `Total Shares`
- Copy buttons for:
    - input secret
    - generated shares
    - recover input shares
    - recovered secret
- Error display with backend `request_id`
- Basic client-side validation
- Contract-driven integration with backend

## Tech Stack

- **React**
- **TypeScript**
- **Vite**

## Project Structure

```text
src/frontend/
├── public/
├── src/
│   ├── api/
│   │   └── secrets.ts
│   ├── components/
│   │   ├── RecoverForm.tsx
│   │   └── SplitForm.tsx
│   ├── types/
│   │   └── api.ts
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── README.md
```

## Backend Contract

The frontend is built against the following backend endpoints.

### Split Secret

POST /api/v1/secrets/split

- Request:
```json
{
  "secret": "hello",
  "threshold": 3,
  "total_shares": 5
}
```
- Response:
```json
{
  "shares": ["..."],
  "share_count": 5,
  "request_id": "..."
}
```
### Recover Secret

POST /api/v1/secrets/recover

- Request:
```json
{
  "shares": ["share1", "share2", "share3"]
}
```
- Response:
```json
{
  "secret": "hello",
  "request_id": "..."
}
``` 
### Error Format
```json
{
  "code": "INVALID_REQUEST",
  "message": "text",
  "request_id": "..."
}
```

## How Recover Input Works

The backend expects:
```python
list[str]
```
So in the UI, the user pastes shares one per line into a textarea.

### Example user input:

- share1
- share2
- share3

The frontend converts it into:
```python
const shares = textareaValue
  .split("\n")
  .map((s) => s.trim())
  .filter(Boolean)
```
Then sends:
```python
{
  "shares": ["share1", "share2", "share3"]
}
```

## Local Development

This frontend expects the backend to be available at:
```python
http://127.0.0.1:8000
```
### 1. Start RabbitMQ

If you use Docker:
```shell
docker run -d --hostname shamir-rabbit --name shamir-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
- RabbitMQ management UI:
```python
http://localhost:15672
```
### Default credentials:
```python
login: guest 
passrord: guest
```
## 2. Install backend dependencies

From the repository root:
```shell
py -m pip install -r requirements.txt
```
## 3. Start the worker

From src/:
```shell
py -m broker.worker
```
## 4. Start the API

From src/ in another terminal:
```shell
py -m uvicorn api.main:app --reload
```
## 5. Check backend docs

Open:
```python
http://127.0.0.1:8000/docs
```
- CORS Setup for Local Frontend Development

For local frontend development, the backend should allow requests from Vite.

Example FastAPI configuration:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
``` 
- Run the Frontend

From src/frontend/:
```shell
npm install
npm run dev
```
Vite usually starts at:
```shell
http://localhost:5173
```
## Expected Local Workflow

You typically need three terminals.

- Terminal 1 — worker
cd src
py -m broker.worker
- Terminal 2 — API
cd src
py -m uvicorn api.main:app --reload
- Terminal 3 — frontend
cd src/frontend
npm install
npm run dev
UI Behavior
Split

#### The user provides:

- secret
- threshold
- total shares

#### The frontend sends:
```json
{
  "secret": "hello",
  "threshold": 3,
  "total_shares": 5
}
```
#### The UI then displays:

- generated shares
- share_count
- request_id
## Recover

The user pastes shares line by line into a textarea.

#### The frontend converts them to a string array and sends:
```json
{
  "shares": ["share1", "share2", "share3"]
}
``` 
#### The UI then displays:

- recovered secret
- request_id
## Errors

When the backend returns an error, the UI displays:

- message
- request_id
## Validation

The frontend includes basic client-side validation.

Split validation
secret must not be empty
threshold must be a positive integer
total shares must be a positive integer
threshold must not be greater than total shares
Recover validation
at least one share must be provided
Notes
The frontend is intentionally kept independent from the Shamir core implementation.
All secret splitting and recovering is done by the backend.
The frontend only follows the backend JSON contract.
Shares are copied in a format that can be pasted directly into the Recover textarea.
The Recover textarea is designed for one share per line.
## Troubleshooting
```python
{"detail":"Not Found"} on 127.0.0.1:8000
```

This is normal for /.
Use:
```python
http://127.0.0.1:8000/docs
``` 
#### Frontend cannot connect to backend

Check:

- backend is running
- worker is running
- RabbitMQ is running
- CORS is configured
- frontend uses the correct API base URL
- RabbitMQ connection refused

RabbitMQ is not running on localhost:5672.

Failed to fetch or CORS error in browser

Check FastAPI CORS configuration and restart the backend.

