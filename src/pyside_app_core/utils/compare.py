__abs_tolerance = 1e-6


def float_approx(a: float, b: float) -> bool:
    if a == b:
        return True

    return abs(a - b) <= __abs_tolerance
