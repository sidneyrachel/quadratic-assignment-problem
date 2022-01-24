# TODO: REPLACE THIS WITH GENETIC ALGORITHM?
# Reference:
# https://github.com/Giant316/quadraticAssignment/blob/main/QAP.ipynb
# https://github.com/100/Solid/blob/master/Solid/SimulatedAnnealing.py

import numpy as np
from copy import deepcopy
from utils import cost
from math import exp, log
from random import random, randint
from classes import Neighbor


def generate_neighbor(assignments):
    indices = np.random.permutation(np.arange(len(assignments)))
    neighbor = deepcopy(assignments)
    neighbor[indices[1]], neighbor[indices[0]] = neighbor[indices[0]], neighbor[indices[1]]

    return neighbor


# def generate_neighbor(assignments, number_of_facilities, flows, distances):
#     neighbors = []
#
#     for i in range(number_of_facilities - 1):
#         for j in range(i + 1, number_of_facilities):
#             neighbor = Neighbor(number_of_facilities=number_of_facilities, flows=flows, distances=distances)
#             assignments[j], assignments[i] = assignments[i], assignments[j]
#             neighbor.set_assignments(assignments=assignments)
#             neighbor.set_tabu_identifiers(tabu_identifiers=[assignments[i], assignments[j]])
#             neighbor.calculate_objective_value()
#             neighbors.append(neighbor)
#             assignments[i], assignments[j] = assignments[j], assignments[i]
#
#     neighbors = sorted(neighbors, key=lambda iterated_neighbor: iterated_neighbor.objective_value)
#
#     k = randint(0, len(neighbors) - 1)
#
#     return neighbors[k].get_assignments()


def is_neighbor_accepted(
    current_energy,
    neighbor_energy,
    current_temperature
):
    try:
        p = exp(-(neighbor_energy - current_energy) / current_temperature)
    except OverflowError:
        return True

    return True if p >= 1 else p >= random()


def run_simulated_annealing(
    flows,
    distances,
    number_of_iterations,
    start_temperature,
    schedule_constant,
    schedule
):
    number_of_facilities = len(flows)
    current_assignments = np.random.permutation(np.arange(number_of_facilities))
    current_energy = cost.calculate_objective_value(
        flows=flows,
        distances=distances,
        assignments=current_assignments
    )
    best_assignments = deepcopy(current_assignments)
    best_energy = current_energy
    current_temperature = start_temperature

    for idx in range(number_of_iterations):
        neighbor = generate_neighbor(
            assignments=current_assignments,
            # number_of_facilities=number_of_facilities,
            # flows=flows,
            # distances=distances
        )
        neighbor_energy = cost.calculate_objective_value(
            flows=flows,
            distances=distances,
            assignments=neighbor
        )

        # TODO: CHECK IF THIS IS TRUE
        if neighbor_energy < best_energy or is_neighbor_accepted(
            current_energy=current_energy,
            neighbor_energy=neighbor_energy,
            current_temperature=current_temperature
        ):
            current_assignments = neighbor
            current_energy = neighbor_energy

        if current_energy < best_energy:
            best_energy = current_energy
            best_assignments = deepcopy(current_assignments)

        print(f'[SA] Iteration: {(idx + 1)}. '
              f'Objective value: {best_energy}.')

        if schedule == 'geometric':
            current_temperature *= schedule_constant
        elif schedule == 'linear':
            current_temperature -= schedule_constant
        else:
            raise Exception(f"Schedule is unknown. Schedule: {schedule}.")

        if current_temperature < 0.000001:
            print("Temperature reaches 0. Terminating...")
            return best_assignments, best_energy

    return best_assignments, best_energy

