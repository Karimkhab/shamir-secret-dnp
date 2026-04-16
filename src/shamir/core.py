import secrets
from sympy import nextprime


def generate(secret_int: int, threshold: int, byte_length: int, total_shares: int) -> list[int]:
    """
    Generate coefficients for a polynomial with f(0) equal to secret.
    :param secret: Secret value as an integer.
    :param threshold: Number of shares required for reconstruction.
    :param prime: Prime modulus used for finite field operations.
    :return: List of polynomial coefficients.
    """
    offset = secrets.randbits(128)
    prime = int(nextprime(secret_int + offset))

    coefficients = [secret_int]
    for _ in range(threshold - 2):
        coefficients.append(secrets.randbelow(prime))

    coefficients.append(1 + secrets.randbelow(prime - 1))
    return prime, coefficients


def calculate_polynomial(coefficients: list[int], x: int, prime: int) -> int:
    """
    Calculate a polynomial at x
    :param coefficients: List of polynomial coefficients.
    :param x: value in x axes.
    :param prime: Prime modulus used for finite field operations.
    :return:
    """
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * x + coefficient) % prime
    return result


def lagrange_interpolate_at_zero(points: list[tuple[int, int]], prime: int) -> int:
    """
    Recover f(0) from polynomial points using modular Lagrange interpolation.
    :param points:
    :param prime:
    :return:
    """
    secret = 0
    for i, (x_i, y_i) in enumerate(points):
        numerator = 1
        denominator = 1
        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue
            numerator = (numerator * (-x_j)) % prime
            denominator = (denominator * (x_i - x_j)) % prime

        # Division in GF(p) is multiplication by the modular inverse.
        basis = numerator * pow(denominator, -1, prime)
        secret = (secret + y_i * basis) % prime

    return secret
