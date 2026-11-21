import grid, connections, charge, battery

MAX_SOLAR_POWER = 200


def main():
    sckt = connections.connect_to_server()
    battery_power = 0
    for i in range(24):
        data = connections.get_json_from_server(sckt=sckt)
        random_event = data["random_event"]
        forecast = data["forecast"]
        loads = data["loads"]
        grid_price = data["grid_price"]
        solar_power_left = MAX_SOLAR_POWER
        

        answer = {
            "buildings" : [],
            "generator" : 100
        }

        match random_event:
            case "cloudy":
                for building in loads:
                    load = building["load"]
                    build_answer = {"solar": 0, "battery": 0, "grid": 0}
                    if grid_price > 1 and battery_power >= load:
                        build_answer = {"solar": 0, "battery": load, "grid": 0}
                        battery_power -= load
                    else:
                        build_answer = {"solar": 0, "battery": 0, "grid": load}
                    answer["buildings"].append(build_answer)
            case "battery_failure":
                for building in loads:
                    load = building["load"]
                    build_answer = {"solar": 0, "battery": 0, "grid": 0}
                    if building["type"] != "lecture_hall":
                        if solar_power_left >= load:
                            solar_power_left -= load
                            build_answer = {"solar": load, "battery": 0, "grid": 0}
                        else:
                            build_answer = {"solar": 0, "battery": 0, "grid": load}
                    else:
                        build_answer = {"solar": 0, "battery": 0, "grid": load}
                    answer["buildings"].append(build_answer)
            case "grid_failure":
                for building in loads:
                    load = building["load"]
                    build_answer = {"solar": 0, "battery": 0, "grid": 0}
                    if building["type"] != "lecture_hall":
                        if solar_power_left >= load:
                            solar_power_left -= load
                            build_answer = {"solar": load, "battery": 0, "grid": 0}
                        else:
                            build_answer = {"solar": 0, "battery": load, "grid": 0}
                            battery_power -= load
                    else:
                        build_answer = {"solar": 0, "battery": load, "grid": 0}
                        battery_power -= load
                    answer["buildings"].append(build_answer)
            case _:
                for building in loads:
                    load = building["load"]
                    build_answer = {"solar": 0, "battery": 0, "grid": 0}
                    if building["type"] != "lecture_hall":
                        if solar_power_left >= load:
                            solar_power_left -= load
                            build_answer = {"solar": load, "battery": 0, "grid": 0}
                        elif grid_price > 1 and battery_power >= load:
                            build_answer = {"solar": 0, "battery": load, "grid": 0}
                            battery_power -= load
                        else:
                            build_answer = {"solar": 0, "battery": 0, "grid": load}
                    else:
                        if grid_price > 1 and battery_power >= load:
                            build_answer = {"solar": 0, "battery": load, "grid": 0}
                            battery_power -= load
                        else:
                            build_answer = {"solar": 0, "battery": 0, "grid": load}
                    answer["buildings"].append(build_answer)

        amount_to_charge = charge.charge(battery_power, 100)
        battery_power += amount_to_charge
        answer["charge"] = amount_to_charge
        connections.send_json_to_server(sckt=sckt, dict_output=answer)


if __name__ == "__main__":
    main()