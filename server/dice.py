"""Server-side dice streams. The GM never invents numbers; it consumes these in order."""
import secrets


def stream(sides: int, n: int):
    return [secrets.randbelow(sides) + 1 for _ in range(n)]


def make_dice(n_d6=60, n_d10=30, n_d20=30):
    return {"d6": stream(6, n_d6), "d10": stream(10, n_d10), "d20": stream(20, n_d20)}
