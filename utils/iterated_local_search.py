# reference:
# https://github.com/shah314/cilsassignment/blob/master/cILSAssignment.cpp
# https://github.com/BlackMooth/Quadratic-Assignment-Problem
# https://github.com/Lolik-Bolik/Quadratic_Assign_Problem/blob/master/algorithms/iterated_local_search.py

import numpy as np
from classes import Individual
import random
from copy import deepcopy


def generate_initial_population(flows, distances, number_of_individuals):
    initial_population = []
    number_of_facilities = len(flows)
    available_permutation = set()

    for i in range(number_of_individuals):
        assignments = np.random.permutation(np.arange(number_of_facilities))
        assignment_str = ''.join(str(location) for location in assignments)

        while assignment_str in available_permutation:
            assignments = np.random.permutation(np.arange(number_of_facilities))
            assignment_str = ''.join(str(location) for location in assignments)

        available_permutation.add(assignment_str)

        initial_population.append(Individual(assignments=assignments, flows=flows, distances=distances))

    return initial_population


def sort_population(population):
    return sorted(population, key=lambda individual: individual.objective_value)


def shuffle_population(population, number_of_shuffles):
    for individual in population:
        for i in range(number_of_shuffles):
            indices = np.random.permutation(np.arange(individual.number_of_facilities))
            individual.exchange(facility1=indices[0], facility2=indices[1])

        # TODO: THIS IS REDUNDANT?
        # individual.calculate_objective_value()


def two_opt_improvement(individual, worst_acceptance_probability):
    for i in range(individual.number_of_facilities - 1):
        for j in range(i + 1, individual.number_of_facilities):
            objective_value = individual.objective_value
            individual.exchange(facility1=i, facility2=j)
            new_objective_value = individual.objective_value

            if new_objective_value > objective_value:
                probability = random.uniform(0, 1)

                if probability > worst_acceptance_probability:
                    individual.exchange(facility1=i, facility2=j)  # abort exchange procedure


def three_opt_improvement(individual, local_improvement_iterations, worst_acceptance_probability):
    for i in range(local_improvement_iterations):
        objective_value = individual.objective_value
        indices = np.random.permutation(np.arange(individual.number_of_facilities))
        individual.exchange(facility1=indices[0], facility2=indices[1])
        individual.exchange(facility1=indices[1], facility2=indices[2])

        new_objective_value = individual.objective_value

        if new_objective_value > objective_value:
            probability = random.uniform(0, 1)

            if probability > worst_acceptance_probability:
                individual.exchange(facility1=indices[1], facility2=indices[2])
                individual.exchange(facility1=indices[0], facility2=indices[1])


def four_opt_improvement(individual, local_improvement_iterations, worst_acceptance_probability):
    for i in range(local_improvement_iterations):
        objective_value = individual.objective_value
        indices = np.random.permutation(np.arange(individual.number_of_facilities))
        individual.exchange(facility1=indices[0], facility2=indices[1])
        individual.exchange(facility1=indices[1], facility2=indices[2])
        individual.exchange(facility1=indices[2], facility2=indices[3])

        new_objective_value = individual.objective_value

        if new_objective_value > objective_value:
            probability = random.uniform(0, 1)

            if probability > worst_acceptance_probability:
                individual.exchange(facility1=indices[2], facility2=indices[3])
                individual.exchange(facility1=indices[1], facility2=indices[2])
                individual.exchange(facility1=indices[0], facility2=indices[1])


def local_improvement(
        individual,
        local_improvement_iterations,
        worst_acceptance_probability,
        mode='two_opt'
):
    if mode == 'two_opt':
        two_opt_improvement(
            individual=individual,
            worst_acceptance_probability=worst_acceptance_probability
        )
    elif mode == 'three_opt':
        three_opt_improvement(
            individual=individual,
            local_improvement_iterations=local_improvement_iterations,
            worst_acceptance_probability=worst_acceptance_probability
        )
    elif mode == 'four_opt':
        four_opt_improvement(
            individual=individual,
            local_improvement_iterations=local_improvement_iterations,
            worst_acceptance_probability=worst_acceptance_probability
        )
    else:
        raise Exception(f'Local improvement mode is unknown. Mode: {mode}.')


def run_iterated_local_search(
    flows,
    distances,
    number_of_individuals,
    number_of_iterations,
    shuffle_tolerance,
    number_of_shuffles,
    local_improvement_iterations,
    worst_acceptance_probability,
    local_improvement_mode
):
    population = generate_initial_population(
        flows=flows,
        distances=distances,
        number_of_individuals=number_of_individuals
    )

    best_individual = None
    best_iteration = 0
    count = 0

    for idx in range(1, number_of_iterations + 1):
        population = sort_population(population=population)
        new_best_individual = population[0]

        if best_individual is None or new_best_individual.objective_value < best_individual.objective_value:
            best_individual = deepcopy(new_best_individual)
            best_iteration = idx
            count = 0
        else:
            count += 1

            if count > shuffle_tolerance:
                shuffle_population(population=population, number_of_shuffles=number_of_shuffles)
                count = 0

        print(f'[ILS] Iteration: {idx}. '
              f'Objective value: {best_individual.objective_value}.')

        for current_individual in population:
            local_improvement(
                individual=current_individual,
                local_improvement_iterations=local_improvement_iterations,
                worst_acceptance_probability=worst_acceptance_probability,
                mode=local_improvement_mode
            )

    print(f'[ILS] Best individual found on iteration: {best_iteration}.')
    best_individual.normalize_final_assignments()

    return best_individual.assignments, best_individual.objective_value
