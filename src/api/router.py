from fastapi import APIRouter, Request
from pydantic import BaseModel

from broker.rabbit import publish_message

router = APIRouter(prefix="/api/v1/secrets")


class SplitSecretRequest(BaseModel):
    """Request body for splitting a text secret into Shamir shares."""
    secret: str
    threshold: int
    total_shares: int


class RecoverSecretRequest(BaseModel):
    """Request body for recovering a secret and checking it against SHA-256."""
    shares: list[str]
    expected_hash: str


@router.post("/split")
def split_secret(request: Request, data: SplitSecretRequest):
    """Queue a split task and return its request id."""

    request_id = request.state.request_id

    # publish msg to rabbit
    publish_message({
        "type": "split",
        "request_id": request_id,
        "payload": data.model_dump(),
    })

    # return response
    return {
        "status": "accepted",
        "request_id": request_id,
    }


@router.post("/recover")
def recover_secret(request: Request, data: RecoverSecretRequest):
    """Queue a recovery task and return its request id."""

    request_id = request.state.request_id

    # publish msg to rabbit
    publish_message({
        "type": "recover",
        "request_id": request_id,
        "payload": data.model_dump(),
    })

    # return response
    return {
        "status": "accepted",
        "request_id": request_id,
    }
