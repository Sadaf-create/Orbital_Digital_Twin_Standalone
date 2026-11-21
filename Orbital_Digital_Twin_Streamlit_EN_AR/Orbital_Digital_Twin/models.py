from math import cos, pi, sin

NODES = ("SAT-A", "SAT-B", "SAT-C")

def orbit_trace(revolution: float) -> list[tuple[float, float]]:
    """Conceptual drawing in canvas coordinates, with no real orbital elements."""
    phase = 2 * pi * revolution
    return [
        (round(250 + 166 * cos(phase + i * 2 * pi / 3), 1),
         round(110 + 66 * sin(phase + i * 2 * pi / 3), 1))
        for i in range(len(NODES))
    ]


def service_coverage(offline: str | None) -> dict[str, int]:
    """Count fictional relays available to each demonstration service."""
    dependencies = {"Mapping": ("SAT-A", "SAT-B"), "Weather reports": ("SAT-B", "SAT-C"),
                    "Service notices": NODES}
    return {service: sum(node != offline for node in relays) for service, relays in dependencies.items()}
