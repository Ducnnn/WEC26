grid_failure_event = "grid_failure"
generator_cost_per_unit = 1.00


def is_grid_available(message):
    """Return True if the grid can be used this hour.

    The grid is down only when the server's random event is "grid_failure".
    A missing or empty event counts as "none", so the grid is available.
    """
    random_event = message.get("random_event") or "none"
    return random_event.strip().lower() != grid_failure_event


def get_grid_price(message):
    """Return this hour's grid price per unit from the server message.

    Raises ValueError if the price is missing, not a number, or negative,
    so a bad message is caught right away instead of costing us silently.
    """
    raw_price = message.get("grid_price")
    if raw_price is None:
        raise ValueError("server message has no grid_price")

    try:
        grid_price = float(raw_price)
    except (TypeError, ValueError):
        raise ValueError(f"grid_price is not a number: {raw_price!r}")

    if grid_price < 0:
        raise ValueError(f"grid_price is negative: {grid_price}")
    return grid_price


if __name__ == "__main__":
    example_message = {"random_event": "none", "grid_price": 1.2}
    failure_message = {"random_event": "grid_failure", "grid_price": 1.2}

    print("available (none):", is_grid_available(example_message))
    print("available (grid_failure):", is_grid_available(failure_message))
    print("price:", get_grid_price(example_message))
