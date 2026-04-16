import logging

from shamir.core import lagrange_interpolate_at_zero
from shamir.share import Share, validate_consistent_shares


logger = logging.getLogger(__name__)

def check_input_data(shares: list[str]) -> None:
    """
    Validate input data before recovering a secret.
    :param shares: list of shares
    """
    if not isinstance(shares, list):
        raise ValueError("malformed share")
    if not shares:
        raise ValueError("insufficient shares")



def recover_secret(shares: list[str]) -> str:
    """
    Recover the original UTF-8 text secret from at least threshold shares.
    :param shares:
    :return:
    """
    check_input_data(shares)

    parsed_shares = [Share.parse(share) for share in shares]

    first = parsed_shares[0]
    selected_shares = parsed_shares[: first.threshold]
    points = [(share.x, share.y) for share in selected_shares]

    secret_int = lagrange_interpolate_at_zero(points, first.prime)
    try:
        secret_bytes = secret_int.to_bytes(first.byte_length, "big")
    except OverflowError as error:
        raise ValueError("inconsistent shares") from error

    try:
        secret = secret_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("inconsistent shares") from error

    # Hash logging confirms integrity without exposing the reconstructed secret.
    logger.info(
        "Recovered Shamir secret",
        extra={
            "threshold": first.threshold,
            "provided_shares": len(parsed_shares),
        },
    )
    return secret
