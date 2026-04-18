export type SplitRequest = {
    secret: string
    threshold: number
    totalShares: number
}

export type SplitResponse = {
    shares: string[]
    share_count: number
    request_id: string
}

export type RecoverRequest = {
    shares: string[]
}

export type RecoverResponse = {
    secret: string
    request_id: string
}

export type ApiError = {
    code: string
    message: string
    request_id: string
}