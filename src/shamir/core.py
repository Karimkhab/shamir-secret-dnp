import secrets
from sympy import nextprime
import hashlib



def hash_data(data: bytes) -> str:
    """Return SHA-256 hex digest of input bytes."""
    return hashlib.sha256(data).hexdigest()


def generate(secret_int: int, threshold: int, total_shares: int) -> tuple[int, list[int]]:
    """
    Generate coefficients for a polynomial with f(0) equal to secret.
    :param secret_int: secret value.
    :param threshold: threshold value.
    :param total_shares: total number of shares.
    :return: prime and coefficients
    """
    # choose prime that more secret and total shares
    offset = secrets.randbits(128)
    prime = int(nextprime(max(secret_int + offset, total_shares)))

    # first coefficients = secret
    coefficients = [secret_int]
    for _ in range(threshold - 2):
        # random coefficients
        coefficients.append(secrets.randbelow(prime))

    # highest degree coefficient must be non-zero
    coefficients.append(1 + secrets.randbelow(prime - 1))
    return prime, coefficients


def calculate_polynomial(coefficients: list[int], x: int, prime: int) -> int:
    """
    Calculate a polynomial at x
    :param coefficients: List of polynomial coefficients.
    :param x: value in x axes.
    :param prime: Prime modulus used for finite field operations.
    :return: result of the polynomial.
    """
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * x + coefficient) % prime
    return result


def lagrange_interpolate_at_zero(points: list[tuple[int, int]], prime: int) -> int:
    """
    Recover f(0) from polynomial points using modular Lagrange interpolation.
    :param points: list of (x, y) points.
    :param prime: prime modulus used for finite field operations.
    :return: result of the polynomial.
    """
    if not points:
        raise ValueError("no points provided")

    # x must be unique
    x_vals = [x for x, _ in points]
    if len(set(x_vals)) != len(x_vals):
        raise ValueError("duplicate x values")

    # x = 0 would leak secret directly
    if any(x == 0 for x in x_vals):
        raise ValueError("x=0 is not allowed")

    secret = 0
    for i, (x_i, y_i) in enumerate(points):
        numerator = 1
        denominator = 1
        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue
            numerator = (numerator * (-x_j)) % prime
            denominator = (denominator * (x_i - x_j)) % prime

        # modular inverse instead of division
        basis = numerator * pow(denominator, -1, prime)
        secret = (secret + y_i * basis) % prime

    return secret
