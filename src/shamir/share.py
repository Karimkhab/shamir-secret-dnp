from dataclasses import dataclass

SHARE_VERSION = "sss1"
SHARE_PARTS_COUNT = 6


@dataclass(frozen=True)
class Share:
    threshold: int
    prime: int
    byte_length: int
    x: int
    y: int

    def serialize(self) -> str:
        return f"sss1:{self.threshold}:{self.prime:x}:{self.byte_length:x}:{self.x:x}:{self.y:x}"

    @classmethod
    def parse(cls, raw: str) -> "Share":
        """
        Parse a serialized share string.

        :param raw: Serialized share in sss1 format.
        :return: Parsed Share object.
        :raises ValueError: If the share format is invalid.
        """
        if not isinstance(raw, str):
            raise ValueError("malformed share")

        parts = raw.strip().split(":")
        if len(parts) != SHARE_PARTS_COUNT:
            raise ValueError("malformed share")

        version, threshold_raw, prime_raw, byte_length_raw, x_raw, y_raw = parts
        if version != SHARE_VERSION:
            raise ValueError("malformed share")

        share = cls(
            threshold = int(threshold_raw, 10),
            prime = int(prime_raw, 16),
            byte_length = int(byte_length_raw, 16),
            x=int(x_raw, 16), y=int(y_raw, 16),
        )
        return share




def _parse_hex_int(value: str) -> int:
    if value == "":
        raise ValueError("empty hex value")
    return int(value, 16)


def _validate_share_values(share: Share) -> None:
    if share.threshold < 2:
        raise ValueError("malformed share")
    if share.byte_length <= 0:
        raise ValueError("malformed share")
    if not 0 < share.x < share.prime:
        raise ValueError("malformed share")
    if not 0 <= share.y < share.prime:
        raise ValueError("malformed share")
