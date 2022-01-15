import numpy as np
from collections import deque
from copy import deepcopy
from utils import cost, assignment
from classes import Neighbor


def generate_neighbors(assignments, number_of_facilities, flows, distances):
    neighbors = []

    for i in range(number_of_facilities - 1):
        for j in range(i + 1, number_of_facilities):
            neighbor = Neighbor(number_of_facilities=number_of_facilities, flows=flows, distances=distances)
            assignments[j], assignments[i] = assignments[i], assignments[j]
            neighbor.set_assignments(assignments=assignments)
            neighbor.set_tabu_identifiers(tabu_identifiers=[assignments[i], assignments[j]])
            neighbor.calculate_objective_value()
            neighbors.append(neighbor)
            assignments[i], assignments[j] = assignments[j], assignments[i]

    return neighbors


def is_in_tabu_list(tabu_identifiers, tabu_list):
    if tabu_identifiers in tabu_list:
        return True

    tabu_identifiers[0], tabu_identifiers[1] = tabu_identifiers[1], tabu_identifiers[0]

    if tabu_identifiers in tabu_list:
        return True

    return False


def run_tabu_search(
    flows,
    distances,
    tabu_size,
    number_of_iterations
):
    number_of_facilities = len(flows)
    tabu_list = deque(maxlen=tabu_size)
    current_assignments = np.random.permutation(np.arange(number_of_facilities))
    best_assignments = deepcopy(current_assignments)
    best_objective_value = cost.calculate_objective_value(
        flows=flows,
        distances=distances,
        assignments=best_assignments
    )

    for idx in range(number_of_iterations):
        neighbors = generate_neighbors(
            assignments=current_assignments,
            number_of_facilities=number_of_facilities,
            flows=flows,
            distances=distances
        )
        neighbors = sorted(neighbors, key=lambda neighbor: neighbor.objective_value)
        best_neighbor = neighbors[0]

        while True:
            is_all_in_tabu_list = all([
                is_in_tabu_list(
                    tabu_identifiers=neighbor.get_tabu_identifiers(),
                    tabu_list=tabu_list
                ) for neighbor in neighbors
            ])

            if is_all_in_tabu_list:
                print('All neighbors are in tabu list. Terminating...')
                return best_assignments, best_objective_value

            neighbor_tabu_identifiers = best_neighbor.get_tabu_identifiers()

            if is_in_tabu_list(tabu_identifiers=neighbor_tabu_identifiers, tabu_list=tabu_list):
                if best_neighbor.objective_value < best_objective_value:
                    tabu_list.append(neighbor_tabu_identifiers)  # TODO: REMOVE THIS OR NOT?
                    best_assignments = deepcopy(best_neighbor.get_assignments())
                    best_objective_value = best_neighbor.objective_value
                    break
                else:
                    neighbors = neighbors[1:]
                    best_neighbor = neighbors[0]
            else:
                tabu_list.append(neighbor_tabu_identifiers)
                current_assignments = best_neighbor.get_assignments()
                current_objective_value = best_neighbor.objective_value

                if current_objective_value < best_objective_value:
                    best_assignments = deepcopy(current_assignments)
                    best_objective_value = current_objective_value

                break

        print(f'[TS] Iteration: {(idx + 1)}. '
              f'Objective value: {best_objective_value}.')

    assignment.normalize_final_assignments(assignments=best_assignments)

    return best_assignments, best_objective_value
