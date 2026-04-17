import sys
from itertools import combinations
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shamir.decoder import recover_secret
from shamir.encoder import split_secret
from shamir.share import Share


def test_any_threshold_shares_recover_secret() -> None:
    secret = "hello Привет 123"
    result = split_secret(secret, threshold=3, total_shares=5)
    shares = result["shares"]

    assert len(shares) == 5
    assert all(len(Share.parse(share).secret_hash) == 64 for share in shares)
    assert all(
        recover_secret(list(combo)) == secret
        for combo in combinations(shares, 3)
    )


def test_insufficient_shares_fail() -> None:
    result = split_secret("secret", threshold=3, total_shares=5)

    with pytest.raises(ValueError, match="insufficient shares"):
        recover_secret(result["shares"][:2])


def test_wrong_hash_fails() -> None:
    result = split_secret("secret", threshold=3, total_shares=5)
    shares = result["shares"][:3]
    tampered = [share.rsplit(":", 1)[0] + ":" + "0" * 64 for share in shares]

    with pytest.raises(ValueError, match="invalid shares"):
        recover_secret(tampered)


def test_duplicate_shares_fail() -> None:
    result = split_secret("secret", threshold=3, total_shares=5)
    shares = result["shares"]

    with pytest.raises(ValueError, match="duplicate x values"):
        recover_secret([shares[0], shares[0], shares[1]])


def test_malformed_share_fails() -> None:
    with pytest.raises(ValueError, match="malformed share"):
        Share.parse("not-a-share")


def test_mixed_sessions_fail() -> None:
    first = split_secret("alpha secret", threshold=3, total_shares=5)
    second = split_secret("omega secret", threshold=3, total_shares=5)

    with pytest.raises(ValueError, match="inconsistent shares"):
        recover_secret(
            [first["shares"][0], first["shares"][1], second["shares"][2]],
        )
