def calculate_objective_value(flows, distances, assignments):
    value = 0
    number_of_facilities = len(flows)

    for i in range(number_of_facilities):
        for j in range(number_of_facilities):
            value += flows[i][j] * distances[assignments[i]][assignments[j]]

    return value


def calculate_value_swap(assignments, facility1, facility2, flows, distances):
    number_of_facilities = len(flows)
    location1 = assignments[facility1]
    location2 = assignments[facility2]

    delta = flows[facility1][facility1] * (distances[location2][location2] - distances[location1][location1]) + \
        flows[facility1][facility2] * (distances[location2][location1] - distances[location1][location2]) + \
        flows[facility2][facility1] * (distances[location1][location2] - distances[location2][location1]) + \
        flows[facility2][facility2] * (distances[location1][location1] - distances[location2][location2])

    for facility in range(number_of_facilities):
        if facility != facility1 and facility != facility2:
            location = assignments[facility]
            delta += flows[facility][facility1] * (distances[location][location2] - distances[location][location1]) + \
                flows[facility][facility2] * (distances[location][location1] - distances[location][location2]) + \
                flows[facility1][facility] * (distances[location2][location] - distances[location1][location]) + \
                flows[facility2][facility] * (distances[location1][location] - distances[location2][location])

    return delta


def compute_delta_part(
        assignments,
        deltas,
        facility1,
        facility2,
        facility_retained1,
        facility_retained2,
        flows,
        distances
):
    location1 = assignments[facility1]
    location2 = assignments[facility2]
    location_retained1 = assignments[facility_retained1]
    location_retained2 = assignments[facility_retained2]

    return (deltas[facility1][facility2] + (distances[location_retained1][location1] - distances[location_retained1][location2] + distances[location_retained2][location2] - distances[location_retained2][location1]) *
        (flows[facility_retained2][facility1] - flows[facility_retained2][facility2] + flows[facility_retained1][facility2] - flows[facility_retained1][facility1]) +
        (distances[location1][location_retained1] - distances[location2][location_retained1] + distances[location2][location_retained2] - distances[location1][location_retained2]) *
        (flows[facility1][facility_retained2] - flows[facility2][facility_retained2] + flows[facility2][facility_retained1] - flows[facility1][facility_retained1]))
