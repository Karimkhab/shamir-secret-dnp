from fastapi import APIRouter
from broker.rabbit import publish_message
import uuid

router = APIRouter(prefix="/api/v1/secrets")


@router.post("/split")
def split_secret(data: dict):
    request_id = str(uuid.uuid4())

    publish_message({
        "type": "split",
        "request_id": request_id,
        "payload": data
    })

    return {
        "status": "accepted",
        "requestId": request_id
    }


@router.post("/recover")
def recover_secret(data: dict):
    request_id = str(uuid.uuid4())

    publish_message({
        "type": "recover",
        "request_id": request_id,
        "payload": data
    })

    return {
        "status": "accepted",
        "requestId": request_id
    }