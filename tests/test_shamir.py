from __future__ import annotations

import pytest

from shamir_secret import hash_secret, recover_secret, split_secret


def test_roundtrip_reconstruction() -> None:
    secret = "Shamir test secret"
    shares = split_secret(secret=secret, threshold=3, total_shares=5)

    recovered = recover_secret(shares[:3])

    assert recovered == secret


def test_insufficient_shares_fails() -> None:
    shares = split_secret(secret="secret", threshold=3, total_shares=5)

    with pytest.raises(ValueError, match="Insufficient shares"):
        recover_secret(shares[:2])


def test_integrity_hash_matches() -> None:
    secret = "integrity check"
    shares = split_secret(secret=secret, threshold=2, total_shares=3)

    recovered = recover_secret(shares[:2])

    assert hash_secret(recovered) == hash_secret(secret)


def test_invalid_share_parsing_fails() -> None:
    with pytest.raises(ValueError, match="Invalid share format"):
        recover_secret(["bad-share-value"])

