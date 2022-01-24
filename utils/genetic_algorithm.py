# Reference:
# https://arxiv.org/pdf/1405.5050.pdf
# https://github.com/100/Solid/blob/master/Solid/GeneticAlgorithm.py

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


def mutate(mutation_rate, number_of_facilities, individual):
    if mutation_rate >= random():
        indices = np.random.permutation(np.arange(number_of_facilities))
        individual.exchange(facility1=indices[0], facility2=indices[1])

    return individual


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
    num_copy = max(int((1 - crossover_rate) * len(population)), 2)
    num_crossover = len(population) - num_copy

    for idx in range(number_of_iterations):
        population = select(n=num_copy, population=population)
        parents = select(n=2, population=population)

        crossover_idx = 0
        while crossover_idx < num_crossover:
            new_individual1, new_individual2 = crossover(
                parent1=parents[0],
                parent2=parents[1],
                number_of_facilities=number_of_facilities,
                flows=flows,
                distances=distances
            )

            population.append(new_individual1)
            crossover_idx += 1

            if crossover_idx + 1 < num_crossover:
                population.append(new_individual2)
                crossover_idx += 1

        population = list([
            mutate(
                mutation_rate=mutation_rate,
                number_of_facilities=number_of_facilities,
                individual=individual
            ) for individual in population
        ])

        # TODO: MAKE THIS MORE EFFICIENT
        sorted_population = iterated_local_search.sort_population(population=population)
        candidate_best_individual = sorted_population[0]

        if candidate_best_individual.objective_value < best_individual.objective_value:
            best_individual = deepcopy(candidate_best_individual)

        print(f'[GA] Iteration: {(idx + 1)}. '
              f'Objective value: {best_individual.objective_value}.')

    return best_individual.assignments, best_individual.objective_value
