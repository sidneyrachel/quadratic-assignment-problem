# Reference:
# https://arxiv.org/pdf/1405.5050.pdf
# https://github.com/100/Solid/blob/master/Solid/GeneticAlgorithm.py
# https://github.com/remiomosowon/pyeasyga/blob/develop/pyeasyga/pyeasyga.py

import numpy as np
from utils import iterated_local_search
from random import shuffle, random, randint
from copy import deepcopy
from classes import Individual


def select(n, population):
    shuffle(population)
    total_fitness = sum(individual.objective_value for individual in population)

    if total_fitness != 0:
        probabilities = list([individual.objective_value / total_fitness for individual in population])
    else:
        return population[0:n]

    res = []
    for _ in range(n):
        r = random()
        sum_ = 0
        for i, x in enumerate(probabilities):
            sum_ += probabilities[i]
            if r <= sum_:
                res.append(deepcopy(population[i]))
                break

    return res


def crossover(
    parent1,
    parent2,
    number_of_facilities,
    flows,
    distances
):
    indices = np.random.permutation(np.arange(number_of_facilities))
    chosen_indices = indices[:2]
    exchanged_indices = indices[2:]
    exchanged_indices.sort()
    chosen_parent1 = [parent1.assignments[idx] for idx in chosen_indices]
    chosen_parent2 = [parent2.assignments[idx] for idx in chosen_indices]
    exchanged_parent1 = [location for location in parent1.assignments if location not in chosen_parent2]
    exchanged_parent2 = [location for location in parent2.assignments if location not in chosen_parent1]

    child1 = deepcopy(parent1.assignments)
    child2 = deepcopy(parent2.assignments)

    for idx, exchanged_idx in enumerate(exchanged_indices):
        child1[exchanged_idx] = exchanged_parent2[idx]
        child2[exchanged_idx] = exchanged_parent1[idx]

    return Individual(
        assignments=child1,
        flows=flows,
        distances=distances
    ), Individual(
        assignments=child2,
        flows=flows,
        distances=distances
    )


def mutate(number_of_facilities, individual):
    indices = np.random.permutation(np.arange(number_of_facilities))
    individual.exchange(facility1=indices[0], facility2=indices[1])


def run_genetic_algorithm(
    flows,
    distances,
    number_of_individuals,
    crossover_rate,
    mutation_rate,
    number_of_iterations
):
    number_of_facilities = len(flows)
    population = iterated_local_search.generate_initial_population(
        flows=flows,
        distances=distances,
        number_of_individuals=number_of_individuals
    )

    # TODO: MAKE THIS MORE EFFICIENT
    sorted_population = iterated_local_search.sort_population(population=population)
    best_individual = deepcopy(sorted_population[0])

    for idx in range(number_of_iterations):
        new_population = []

        while len(new_population) < number_of_individuals:
            [parent1, parent2] = select(n=2, population=population)

            can_crossover = random() < crossover_rate
            can_mutate = random() < mutation_rate

            if can_crossover:
                child1, child2 = crossover(
                    parent1=parent1,
                    parent2=parent2,
                    number_of_facilities=number_of_facilities,
                    flows=flows,
                    distances=distances
                )
            else:
                child1 = parent1
                child2 = parent2

            if can_mutate:
                mutate(
                    number_of_facilities=number_of_facilities,
                    individual=child1
                )
                mutate(
                    number_of_facilities=number_of_facilities,
                    individual=child2
                )

            new_population.append(child1)
            if len(new_population) < number_of_individuals:
                new_population.append(child2)

        new_population[0] = best_individual
        population = new_population
        sorted_population = iterated_local_search.sort_population(population=population)
        best_individual = deepcopy(sorted_population[0])

        print(f'[GA] Iteration: {(idx + 1)}. '
              f'Objective value: {best_individual.objective_value}.')

    best_individual.normalize_final_assignments()

    return best_individual.assignments, best_individual.objective_value
