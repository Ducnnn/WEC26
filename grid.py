grid_failure_event = "grid_failure"
battery_failure_event = "battery_failure"
generator_cost_per_unit = 1.00


def is_grid_available(received):
    return received["random_event"] != grid_failure_event


# Above $1 the battery (charged by the $1 generator) is the cheaper source
def is_grid_more_expensive(received):
    return received["grid_price"] > generator_cost_per_unit


# grid goes before battery when it's cheap or the battery
# has failed. Otherwise the battery goes first and the grid takes leftovers.
def use_grid_before_battery(received):
    if not is_grid_available(received):
        return False
    if received["random_event"] == battery_failure_event:
        return True
    return not is_grid_more_expensive(received)


# Grid has no limit, so it covers whatever is left. gives nothing during a grid failure.
def allocate_grid(leftover_demands, received):
    if not is_grid_available(received):
        return [0] * len(leftover_demands)
    return list(leftover_demands)
