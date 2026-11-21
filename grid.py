grid_failure_event = "grid_failure"
generator_cost_per_unit = 1.00


def is_grid_available(received):
    return received["random_event"] != grid_failure_event


# Above $1 the battery (charged by the $1 generator) is the cheaper source
def is_grid_more_expensive(received):
    return received["grid_price"] > generator_cost_per_unit
