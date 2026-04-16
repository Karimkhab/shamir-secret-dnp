import logging

from shamir.core import lagrange_interpolate_at_zero, hash_data
from shamir.share import Share


logger = logging.getLogger(__name__)

def check_input_data(shares: list[str], expected_hash: str) -> None:
    """
    Validate input data before recovering a secret.
    :param shares: list of shares
    """
    if not isinstance(shares, list):
        raise ValueError("malformed share")
    if not shares:
        raise ValueError("insufficient shares")
    if not isinstance(expected_hash, str) or not expected_hash:
        raise ValueError("invalid hash")


def recover_secret(shares: list[str], expected_hash: str) -> str:
    """
    Recover the original UTF-8 text secret from at least threshold shares.
    :param shares: list of shares
    :return: secret UTF-8 text
    """
    check_input_data(shares, expected_hash)

    parsed_shares = [Share.parse(s) for s in shares]
    first = parsed_shares[0]

    # check enough shares
    if len(parsed_shares) < first.threshold:
        raise ValueError("insufficient shares")

    # check consistency
    for s in parsed_shares:
        if s.prime != first.prime or s.threshold != first.threshold or s.byte_length != first.byte_length:
            raise ValueError("inconsistent shares")

    # take only threshold shares
    selected = parsed_shares[:first.threshold]
    points = [(s.x, s.y) for s in selected]

    # recover secret
    secret_int = lagrange_interpolate_at_zero(points, first.prime)

    try:
        secret_bytes = secret_int.to_bytes(first.byte_length, "big")
        secret = secret_bytes.decode("utf-8")
    except Exception:
        raise ValueError("inconsistent shares")

    # hash check (CRITICAL)
    if hash_data(secret_bytes) != expected_hash:
        raise ValueError("invalid shares")

    # write logs of execution
    logger.info("Recovered Shamir secret", extra={
        "threshold": first.threshold,
        "provided_shares": len(parsed_shares),
    },)

    return secret