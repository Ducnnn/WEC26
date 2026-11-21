import charge
import connections
import grid

MAX_SOLAR_POWER = 200
BATTERY_CAPACITY = 100
HOURS_PER_DAY = 24


def main():
    sckt = connections.connect_to_server()
    battery_power = 0

    for hour in range(HOURS_PER_DAY):
        data = connections.get_json_from_server(sckt=sckt)
        random_events = data["random_event"]
        last_hour = hour == HOURS_PER_DAY - 1
        battery_works = "battery_failure" not in random_events
        generator_works = "generator_failure" not in random_events
        grid_up = grid.is_grid_available(data)

        # Charge left after the last hour is wasted, so spend it then
        use_battery = battery_works and (
            not grid_up or last_hour or (generator_works and grid.is_grid_more_expensive(data))
        )

        solar_left = 0 if "cloudy_weather" in random_events else MAX_SOLAR_POWER
        battery_left = battery_power if use_battery else 0
        buildings = []

        for building in data["loads"]:
            load = building["load"]
            solar = 0 if building["type"] == "lecture_hall" else min(load, solar_left)
            from_battery = min(load - solar, battery_left)
            from_grid = load - solar - from_battery if grid_up else 0

            solar_left -= solar
            battery_left -= from_battery
            battery_power -= from_battery
            buildings.append({"solar": solar, "battery": from_battery, "grid": from_grid})

        can_charge = battery_works and generator_works and not last_hour
        target = BATTERY_CAPACITY if can_charge else battery_power
        charged_level, _ = charge.charge(battery_power, target)
        generator = charged_level - battery_power
        battery_power = charged_level

        connections.send_json_to_server(
            sckt=sckt, dict_output={"buildings": buildings, "generator": generator}
        )


if __name__ == "__main__":
    main()
