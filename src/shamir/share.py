from dataclasses import dataclass

@dataclass(frozen=True)
class Share:
    threshold: int
    prime: int
    byte_length: int
    x: int
    y: int

    def serialize(self) -> str:
        """serialize share to string"""
        return f"{self.threshold}:{self.prime:x}:{self.byte_length:x}:{self.x:x}:{self.y:x}"

    @classmethod
    def parse(cls, raw: str) -> "Share":
        """parse share from string"""
        try:
            t, p, bl, x, y = raw.strip().split(":")
            return cls(
                threshold = int(t),
                prime = int(p, 16),
                byte_length = int(bl, 16),
                x = int(x, 16), y = int(y, 16),
            )

        except Exception:
            raise ValueError("malformed share")