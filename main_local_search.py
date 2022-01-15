# reference:
# https://github.com/shah314/cilsassignment/blob/master/cILSAssignment.cpp
# https://github.com/BlackMooth/Quadratic-Assignment-Problem
# https://github.com/Lolik-Bolik/Quadratic_Assign_Problem/blob/master/algorithms/iterated_local_search.py

import copy
import numpy as np
from utils import file
from classes import Individual
import random

WORST_ACCEPTANCE_PROBABILITY = 0.0
NUMBER_OF_GENERATIONS = 1000  # 10000
NUMBER_OF_INDIVIDUALS = 5
SHUFFLE_TOLERANCE = 10
NUMBER_OF_SHUFFLES = 15
LOCAL_IMPROVEMENT_ITERATIONS = 1000


def generate_initial_population(flows, distances):
    initial_population = []
    number_of_facilities = len(flows)
    available_permutation = set()

    for i in range(NUMBER_OF_INDIVIDUALS):
        assignments = np.random.permutation(np.arange(number_of_facilities))
        assignment_str = "".join(str(location) for location in assignments)

        while assignment_str in available_permutation:
            assignments = np.random.permutation(np.arange(number_of_facilities))
            assignment_str = "".join(str(location) for location in assignments)

        available_permutation.add(assignment_str)

        initial_population.append(Individual(assignments=assignments, flows=flows, distances=distances))

    return initial_population


def sort_population(pop):
    return sorted(pop, key=lambda individual: individual.objective_value)


def shuffle_population(pop):
    for individual in pop:
        for i in range(NUMBER_OF_SHUFFLES):
            indices = np.random.permutation(np.arange(individual.number_of_facilities))
            individual.exchange(facility1=indices[0], facility2=indices[1])

        # TODO: THIS IS REDUNDANT?
        # individual.calculate_objective_value()


def two_opt_improvement(individual):
    for i in range(individual.number_of_facilities - 1):
        for j in range(i + 1, individual.number_of_facilities):
            objective_value = individual.objective_value
            individual.exchange(facility1=i, facility2=j)
            new_objective_value = individual.objective_value

            if new_objective_value > objective_value:
                probability = random.random()

                if probability > WORST_ACCEPTANCE_PROBABILITY:
                    individual.exchange(facility1=i, facility2=j)  # abort exchange procedure


def three_opt_improvement(individual):
    for i in range(LOCAL_IMPROVEMENT_ITERATIONS):
        objective_value = individual.objective_value
        indices = np.random.permutation(np.arange(individual.n))
        individual.exchange(facility1=indices[0], facility2=indices[1])
        individual.exchange(facility1=indices[1], facility2=indices[2])

        new_objective_value = individual.objective_value

        if new_objective_value > objective_value:
            probability = random.random()

            if probability > WORST_ACCEPTANCE_PROBABILITY:
                individual.exchange(facility1=indices[1], facility2=indices[2])
                individual.exchange(facility1=indices[0], facility2=indices[1])


def four_opt_improvement(individual):
    for i in range(LOCAL_IMPROVEMENT_ITERATIONS):
        objective_value = individual.objective_value
        indices = np.random.permutation(np.arange(individual.number_of_facilities))
        individual.exchange(facility1=indices[0], facility2=indices[1])
        individual.exchange(facility1=indices[1], facility2=indices[2])
        individual.exchange(facility1=indices[2], facility2=indices[3])

        new_objective_value = individual.objective_value

        if new_objective_value > objective_value:
            probability = random.random()

            if probability > WORST_ACCEPTANCE_PROBABILITY:
                individual.exchange(facility1=indices[2], facility2=indices[3])
                individual.exchange(facility1=indices[1], facility2=indices[2])
                individual.exchange(facility1=indices[0], facility2=indices[1])


def local_improvement(individual):
    two_opt_improvement(individual=individual)
    # three_opt_improvement(individual=individual)
    # four_opt_improvement(individual=individual)


if __name__ == '__main__':
    flows, distances = file.read_external_file(filename='had12.dat')
    population = generate_initial_population(
        flows=flows,
        distances=distances
    )

    best_individual = None
    count = 0

    for idx in range(NUMBER_OF_GENERATIONS):
        population = sort_population(pop=population)
        new_best_individual = population[0]

        if idx == 0 or new_best_individual.objective_value < best_individual.objective_value:
            best_individual = copy.deepcopy(new_best_individual)
            count = 0
        else:
            count += 1

            if count > SHUFFLE_TOLERANCE:
                shuffle_population(pop=population)
                count = 0

        print(f"Current objective value: {best_individual.objective_value}")

        for current_individual in population:
            local_improvement(individual=current_individual)

    print(best_individual)
    best_individual.normalize_final_assignments()
    print(best_individual)

    # assignments = [ 9, 2, 10,  1, 11,  4,  5,  6,  7, 0,  3,  8]
    #
    # value = 0
    #
    # for i in range(len(flows)):
    #     for j in range(len(flows)):
    #         value += flows[i][j] * distances[assignments[i]][assignments[j]]
    #
    # print(value)
