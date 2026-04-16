from dataclasses import dataclass

SHARE_VERSION = "sss1"


@dataclass(frozen=True)
class Share:
    threshold: int
    prime: int
    byte_length: int
    x: int
    y: int

    def serialize(self) -> str:
        return f"{SHARE_VERSION}:{self.threshold}:{self.prime:x}:{self.byte_length:x}:{self.x:x}:{self.y:x}"

    @classmethod
    def parse(cls, raw: str) -> "Share":
        """Parse share from string format."""
        try:
            version, t, p, bl, x, y = raw.strip().split(":")
            if version != SHARE_VERSION:
                raise ValueError

            return cls(
                threshold = int(t),
                prime = int(p, 16),
                byte_length = int(bl, 16),
                x = int(x, 16), y = int(y, 16),
            )

        except Exception:
            raise ValueError("malformed share")