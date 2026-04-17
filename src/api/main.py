import logging
import uuid
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .router import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="Shamir Secret Sharing API")


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Attach a request id to every request and response."""
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-Id"] = request.state.request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, _exc: RequestValidationError):
    """Return validation errors in the project-wide JSON format."""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": "INVALID_REQUEST",
            "message": "invalid request body",
            "request_id": request_id,
        },
    )


app.include_router(router)
