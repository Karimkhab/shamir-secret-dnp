from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass


SHARE_PREFIX = "sss1"


@dataclass(frozen=True)
class ParsedShare:
    threshold: int
    prime: int
    byte_length: int
    x: int
    y: int


def split_secret(secret: str, threshold: int, total_shares: int) -> list[str]:
    if not (2 <= threshold <= total_shares):
        raise ValueError("Invalid threshold/total_shares: expected 2 <= threshold <= total_shares.")

    secret_bytes = secret.encode("utf-8")
    secret_int = int.from_bytes(secret_bytes, byteorder="big", signed=False)
    byte_length = len(secret_bytes)

    prime = _next_prime(max(secret_int, total_shares) + 1)
    coefficients = [secret_int] + [secrets.randbelow(prime) for _ in range(threshold - 1)]

    shares: list[str] = []
    for x in range(1, total_shares + 1):
        y = _evaluate_polynomial(coefficients, x, prime)
        shares.append(_encode_share(threshold, prime, byte_length, x, y))
    return shares


def recover_secret(encoded_shares: list[str]) -> str:
    if not encoded_shares:
        raise ValueError("No shares provided.")

    parsed = [_decode_share(item) for item in encoded_shares]
    first = parsed[0]

    for share in parsed[1:]:
        if (
            share.threshold != first.threshold
            or share.prime != first.prime
            or share.byte_length != first.byte_length
        ):
            raise ValueError("Shares have inconsistent metadata.")

    unique_points: dict[int, int] = {}
    for share in parsed:
        unique_points.setdefault(share.x, share.y)

    if len(unique_points) < first.threshold:
        raise ValueError(
            f"Insufficient shares: got {len(unique_points)}, need at least {first.threshold}."
        )

    selected_points = list(unique_points.items())[: first.threshold]
    secret_int = _lagrange_at_zero(selected_points, first.prime)
    secret_bytes = _int_to_bytes(secret_int, first.byte_length)

    try:
        return secret_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Recovered secret is not valid UTF-8 text.") from exc


def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def _encode_share(threshold: int, prime: int, byte_length: int, x: int, y: int) -> str:
    return f"{SHARE_PREFIX}:{threshold}:{prime:x}:{byte_length:x}:{x:x}:{y:x}"


def _decode_share(raw_share: str) -> ParsedShare:
    parts = raw_share.split(":")
    if len(parts) != 6:
        raise ValueError("Invalid share format: expected 6 ':'-separated parts.")
    if parts[0] != SHARE_PREFIX:
        raise ValueError("Invalid share format: unsupported prefix.")

    try:
        threshold = int(parts[1], 10)
        prime = int(parts[2], 16)
        byte_length = int(parts[3], 16)
        x = int(parts[4], 16)
        y = int(parts[5], 16)
    except ValueError as exc:
        raise ValueError("Invalid share format: expected integer fields.") from exc

    if threshold < 2:
        raise ValueError("Invalid share format: threshold must be >= 2.")
    if prime <= 2:
        raise ValueError("Invalid share format: prime must be > 2.")
    if byte_length < 0:
        raise ValueError("Invalid share format: byte length must be >= 0.")
    if x <= 0:
        raise ValueError("Invalid share format: x must be > 0.")
    if y < 0:
        raise ValueError("Invalid share format: y must be >= 0.")

    return ParsedShare(
        threshold=threshold,
        prime=prime,
        byte_length=byte_length,
        x=x,
        y=y,
    )


def _int_to_bytes(value: int, expected_length: int) -> bytes:
    if expected_length == 0:
        if value != 0:
            raise ValueError("Invalid secret payload for empty secret.")
        return b""
    return value.to_bytes(expected_length, byteorder="big", signed=False)


def _evaluate_polynomial(coefficients: list[int], x: int, modulus: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * x + coefficient) % modulus
    return result


def _lagrange_at_zero(points: list[tuple[int, int]], modulus: int) -> int:
    secret = 0

    for j, (xj, yj) in enumerate(points):
        numerator = 1
        denominator = 1
        for m, (xm, _) in enumerate(points):
            if j == m:
                continue
            numerator = (numerator * (-xm)) % modulus
            denominator = (denominator * (xj - xm)) % modulus

        inv_denominator = pow(denominator, -1, modulus)
        lagrange_basis = (numerator * inv_denominator) % modulus
        secret = (secret + yj * lagrange_basis) % modulus

    return secret


def _next_prime(start: int) -> int:
    candidate = max(3, start)
    if candidate % 2 == 0:
        candidate += 1

    while not _is_probable_prime(candidate):
        candidate += 2
    return candidate


def _is_probable_prime(n: int) -> bool:
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    if n >= (1 << 64):
        bases = [secrets.randbelow(n - 3) + 2 for _ in range(16)]

    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

