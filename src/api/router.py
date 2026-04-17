from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from broker.rabbit import call_worker

router = APIRouter(prefix="/api/v1/secrets")


class SplitSecretRequest(BaseModel):
    """Request body for splitting a text secret into Shamir shares."""
    secret: str
    threshold: int
    total_shares: int


class RecoverSecretRequest(BaseModel):
    """Request body for recovering a secret and checking it against SHA-256."""
    shares: list[str]


def invalid_request(message: str, request_id: str) -> JSONResponse:
    """Return an API error response in the project-wide JSON format."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": "INVALID_REQUEST",
            "message": message,
            "request_id": request_id,
        },
    )


@router.post("/split")
def split_secret(request: Request, data: SplitSecretRequest):
    """Send a split task to the worker and return its result."""

    request_id = request.state.request_id

    try:
        # send msg to queue and wait response
        response = call_worker({
            "type": "split",
            "request_id": request_id,
            "payload": data.model_dump(),
        }, request_id=request_id)
    except TimeoutError as exc:
        return invalid_request(str(exc), request_id)

    if response["status"] == "failed":
        return invalid_request(response["error"], request_id)

    result = response["result"]

    # return response
    return {
        "shares": result["shares"],
        "share_count": len(result["shares"]),
        "request_id": request_id,
    }


@router.post("/recover")
def recover_secret(request: Request, data: RecoverSecretRequest):
    """Send a recovery task to the worker and return its result."""

    request_id = request.state.request_id

    try:
        # send msg to queue and wait response
        response = call_worker({
            "type": "recover",
            "request_id": request_id,
            "payload": data.model_dump(),
        }, request_id=request_id)
    except TimeoutError as exc:
        return invalid_request(str(exc), request_id)

    if response["status"] == "failed":
        return invalid_request(response["error"], request_id)

    # return response
    return {
        "secret": response["result"]["secret"],
        "request_id": request_id,
    }
