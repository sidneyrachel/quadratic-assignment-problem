# Reference:
# https://github.com/Giant316/quadraticAssignment/blob/main/QAP.ipynb
# https://github.com/100/Solid/blob/master/Solid/TabuSearch.py

from utils import file, cost as cost_util
import numpy as np
from collections import deque
from copy import deepcopy

TABU_SIZE = 20
MAX_STEPS = 500
NUMBER_OF_ITERATIONS = 200


def n_size(number_of_facilities):
    n = 0

    for i in range(number_of_facilities):
        n = i + n

    return n


def generate_neighborhood(assignments, number_of_neighbors):
    idx = -1
    number_of_facilities = len(assignments)
    neighborhood = np.zeros((number_of_neighbors, number_of_facilities + 2), dtype=int)

    for i in range(number_of_facilities - 1):
        for j in range(i + 1, number_of_facilities):
            idx += 1
            assignments[j], assignments[i] = assignments[i], assignments[j]
            neighborhood[idx, :-2] = assignments
            neighborhood[idx, -2:] = [assignments[i], assignments[j]]
            assignments[i], assignments[j] = assignments[j], assignments[i]

    return neighborhood


def in_tabu_list(assignments, tabu_list):
    if assignments.tolist() in tabu_list:
        return True

    assignments[0], assignments[1] = assignments[1], assignments[0]

    if assignments.tolist() in tabu_list:
        return True

    return False


def run_tabu_search(assignments):
    """
    Conducts tabu search
    :param verbose: indicates whether or not to print progress regularly
    :return: best state and objective function value of best state
    """
    cur_steps = 0
    tabu_list = deque(maxlen=TABU_SIZE)
    current = assignments
    best = assignments
    number_of_facilities = len(assignments)
    number_of_neighbors = n_size(number_of_facilities)
    max_score = None

    for i in range(MAX_STEPS):
        print(f"Step: {i}")
        cur_steps += 1

        neighborhood = generate_neighborhood(assignments=current, number_of_neighbors=number_of_neighbors)
        cost = np.zeros(number_of_neighbors)  # holds the cost of the neighbors
        for index in range(number_of_neighbors):
            cost[index] = cost_util.calculate_objective_value(flows=flows, distances=distances, assignments=neighborhood[index, :-2])  # evaluate the cost of the candidate neighbors
        rank = np.argsort(cost)  # sorted index based on cost
        neighborhood_best = neighborhood[rank[0]]
        neighborhood_best_index = rank[0]

        while True:
            if all([in_tabu_list(assignments=x[-2:], tabu_list=tabu_list) for x in neighborhood]):
                print("TERMINATING - NO SUITABLE NEIGHBORS")
                return best, cost_util.calculate_objective_value(flows, distances, best)
            if in_tabu_list(neighborhood_best[-2:], tabu_list):
                if cost_util.calculate_objective_value(flows, distances, neighborhood_best[:-2].tolist()) < cost_util.calculate_objective_value(flows, distances, best):
                    # tabu_list.append(neighborhood_best[-2:].tolist())
                    best = deepcopy(neighborhood_best[:-2].tolist())
                    break
                else:
                    neighborhood = np.delete(neighborhood, neighborhood_best_index, axis=0)
                    cost = np.zeros(len(neighborhood))  # holds the cost of the neighbors
                    for index in range(len(neighborhood)):
                        cost[index] = cost_util.calculate_objective_value(
                            flows=flows, distances=distances,
                            assignments=neighborhood[index, :-2]
                        )  # evaluate the cost of the candidate neighbors
                    rank = np.argsort(cost)  # sorted index based on cost
                    neighborhood_best = neighborhood[rank[0]]
                    neighborhood_best_index = rank[0]
            else:
                tabu_list.append(neighborhood_best[-2:].tolist())
                current = neighborhood_best[:-2].tolist()
                if cost_util.calculate_objective_value(flows, distances, current) < cost_util.calculate_objective_value(flows, distances, best):
                    best = deepcopy(current)
                break

        if max_score is not None and cost_util.calculate_objective_value(flows, distances, best) < max_score:
            print("TERMINATING - REACHED MAXIMUM SCORE")
            return best, cost_util.calculate_objective_value(flows, distances, best)
    print("TERMINATING - REACHED MAXIMUM STEPS")
    return best, cost_util.calculate_objective_value(flows, distances, best)


if __name__ == '__main__':
    flows, distances = file.read_external_file(filename='had12.dat')
    number_of_facilities = len(flows)
    curr_assignments = np.random.permutation(np.arange(number_of_facilities))
    assignments, objective_value = run_tabu_search(curr_assignments)
    print(assignments)
    print(objective_value)
