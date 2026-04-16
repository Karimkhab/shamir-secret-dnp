import logging

from sympy import Dict

from shamir.core import calculate_polynomial, generate, hash_data
from shamir.share import Share



logger = logging.getLogger(__name__)

def check_input_data(secret: str, threshold: int, total_shares: int) -> None:
    """
    Validate input data before splitting a secret.
    :param secret: Non-empty text secret.
    :param threshold: Required number of shares for recovery.
    :param total_shares: Total number of shares to generate.
    """
    if not isinstance(secret, str):
        raise ValueError("secret must be a string")
    if secret == "":
        raise ValueError("secret must not be empty")
    if not isinstance(threshold, int) or not isinstance(total_shares, int):
        raise ValueError("threshold and total_shares must be integers")
    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    if total_shares < 2:
        raise ValueError("total_shares must be at least 2")
    if threshold > total_shares:
        raise ValueError("threshold must not exceed total_shares")


def split_secret(secret: str, threshold: int, total_shares: int) -> Dict[str]:
    """
    Split a secret into a list of shares.
    :param secret: Non-empty text secret to split.
    :param threshold: Minimum number of shares required to recover the secret.
    :param total_shares: Total number of shares to generate.
    :return: List of serialized Shamir shares.
    """
    # validate input data
    check_input_data(secret, threshold, total_shares)


    secret_bytes = secret.encode("utf-8")
    secret_int = int.from_bytes(secret_bytes, "big")
    secret_hash = hash_data(secret_bytes)

    # generate prime number and polynomial coefficients
    prime, coefficients = generate(secret_int, threshold)

    shares = []
    for x in range(1, total_shares + 1):
        # calculate the value of the polynomial at the point x
        y = calculate_polynomial(coefficients, x, prime)

        # create share and then we add it to the list
        share = Share(
            threshold = threshold,
            prime = prime,
            byte_length = len(secret_bytes),
            x = x, y = y
        )
        shares.append(share.serialize())

    # write logs of execution
    logger.info("Splitting secret", extra={
        "threshold": threshold,
        "total_shares": total_shares
    })
    return {
        "shares": shares,
        "hash": secret_hash
    }


