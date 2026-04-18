import type {
    SplitRequest,
    SplitResponse,
    RecoverRequest,
    RecoverResponse,
    ApiError,
} from "../types/api"

const BASE_URL = "http://127.0.0.1:8000"

async function parseResponse<T>(response: Response): Promise<T> {
    const data = await response.json()

    if (!response.ok) {
        throw data as ApiError
    }

    return data as T
}

export async function splitSecret(payload: SplitRequest): Promise<SplitResponse> {
    const response = await fetch(`${BASE_URL}/api/v1/secrets/split`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            secret: payload.secret,
            threshold: payload.threshold,
            total_shares: payload.totalShares,
        }),
    })

    return parseResponse<SplitResponse>(response)
}

export async function recoverSecret(payload: RecoverRequest): Promise<RecoverResponse> {
    const response = await fetch(`${BASE_URL}/api/v1/secrets/recover`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            shares: payload.shares,
        }),
    })

    return parseResponse<RecoverResponse>(response)
}