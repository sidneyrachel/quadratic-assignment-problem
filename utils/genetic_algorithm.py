# Reference:
# https://github.com/cssartori/ga-qap
# https://github.com/BlackMooth/Quadratic-Assignment-Problem/blob/master/Genetic_Algorithm.cpp
# https://github.com/100/Solid/blob/master/Solid/GeneticAlgorithm.py

import numpy as np
from utils import iterated_local_search, assignment
from random import shuffle, random, randint, randrange, uniform, choice
from copy import deepcopy
from classes import Individual


def roulette_wheel_selection(number_of_selections, population):
    shuffle(population)
    total_fitness = sum(individual.objective_value for individual in population)

    if total_fitness > 0:
        probabilities = [individual.objective_value / total_fitness for individual in population]
    else:
        return population[:number_of_selections]

    selections = []
    for idx in range(number_of_selections):
        random_number = random()
        probability_sum = 0

        for i, probability in enumerate(probabilities):
            probability_sum += probability

            if random_number <= probability_sum:
                selections.append(deepcopy(population[i]))
                break

    return selections


def tournament_selection(number_of_selections, population, number_of_individuals, tournament_size):
    chosen_population_idx_set = set()
    chosen_individuals = []
    member_set = set(range(number_of_individuals))

    for idx in range(number_of_selections):
        random_idx = assignment.choose_random_element(
            member_set=member_set,
            excluded_member_set=chosen_population_idx_set
        )

        selected_individual = population[random_idx]
        chosen_population_idx = random_idx

        for i in range(1, tournament_size):
            random_idx = assignment.choose_random_element(
                member_set=member_set,
                excluded_member_set=chosen_population_idx_set.union({chosen_population_idx})
            )

            if population[random_idx].objective_value < selected_individual.objective_value:
                selected_individual = population[random_idx]
                chosen_population_idx = random_idx

        chosen_individuals.append(deepcopy(selected_individual))
        chosen_population_idx_set.add(chosen_population_idx)

    return chosen_individuals


def crossover(
    parent1,
    parent2,
    number_of_facilities,
    flows,
    distances,
    crossover_rate
):
    can_crossover = uniform(0, 1) <= crossover_rate

    if not can_crossover:
        if parent1.objective_value < parent2.objective_value:
            return parent1
        else:
            return parent2

    child_assignments = [-1] * number_of_facilities
    placed_locations = [False] * number_of_facilities

    for i in range(number_of_facilities):
        if parent1.assignments[i] == parent2.assignments[i]:
            child_assignments[i] = parent1.assignments[i]
            placed_locations[parent1.assignments[i]] = True

    number_of_trials = max(int(number_of_facilities * 0.2), 1)

    best_child_individual = None

    for idx in range(number_of_trials):
        current_child_assignments = deepcopy(child_assignments)
        current_placed_locations = deepcopy(placed_locations)

        for i in range(number_of_facilities):
            if current_child_assignments[i] == -1:
                if not current_placed_locations[parent1.assignments[i]] and \
                        not current_placed_locations[parent2.assignments[i]]:
                    random_number = uniform(0, 1)
                    if random_number < 0.5:
                        current_child_assignments[i] = parent1.assignments[i]
                    else:
                        current_child_assignments[i] = parent2.assignments[i]
                elif not current_placed_locations[parent1.assignments[i]]:
                    current_child_assignments[i] = parent1.assignments[i]
                elif not current_placed_locations[parent2.assignments[i]]:
                    current_child_assignments[i] = parent2.assignments[i]
                else:
                    location = choice(
                        [i for i in range(len(current_placed_locations)) if not current_placed_locations[i]]
                    )
                    current_child_assignments[i] = location

                current_placed_locations[current_child_assignments[i]] = True

        current_child_individual = Individual(assignments=current_child_assignments, flows=flows, distances=distances)

        if best_child_individual is None or \
                current_child_individual.objective_value < best_child_individual.objective_value:
            best_child_individual = current_child_individual

    return best_child_individual


def perturbation(individual, number_of_perturbations, number_of_facilities):
    for idx in range(max(number_of_perturbations, 1)):
        indices = np.random.permutation(np.arange(number_of_facilities))
        individual.exchange(facility1=indices[0], facility2=indices[1])


def limited_iterated_search(
    child_individual,
    number_of_facilities,
    worst_acceptance_probability
):
    best_individual = deepcopy(child_individual)

    iterated_local_search.two_opt_improvement(
        individual=child_individual,
        worst_acceptance_probability=worst_acceptance_probability
    )

    if child_individual.objective_value < best_individual.objective_value:
        best_individual = deepcopy(child_individual)

    number_of_perturbations = 2

    max_iterations = max(int(number_of_facilities * 0.1), 1)

    for idx in range(max_iterations):
        perturbation(
            individual=child_individual,
            number_of_perturbations=number_of_perturbations,
            number_of_facilities=number_of_facilities
        )

        number_of_perturbations += 1
        if number_of_perturbations > number_of_facilities:
            number_of_perturbations = 2

        iterated_local_search.two_opt_improvement(
            individual=child_individual,
            worst_acceptance_probability=worst_acceptance_probability
        )

        if child_individual.objective_value < best_individual.objective_value:
            best_individual = deepcopy(child_individual)
        else:
            child_individual = deepcopy(best_individual)

    return best_individual


def shift_mutation(individual, number_of_shifts, number_of_facilities):
    p1 = [-1] * number_of_shifts
    p2 = [-1] * (number_of_facilities - number_of_shifts)

    for i in range(number_of_facilities):
        if i < number_of_shifts:
            p1[i] = individual.assignments[i]
        else:
            p2[i - number_of_shifts] = individual.assignments[i]

    for i in range(number_of_facilities):
        if i < number_of_facilities - number_of_shifts:
            individual.assignments[i] = p2[i]
        else:
            individual.assignments[i] = p1[i - (number_of_facilities - number_of_shifts)]

    individual.calculate_objective_value()


def run_genetic_algorithm(
    flows,
    distances,
    number_of_individuals,
    crossover_rate,
    number_of_iterations,
    worst_acceptance_probability,
    tournament_size,
    selection_algorithm
):
    number_of_facilities = len(flows)
    population = iterated_local_search.generate_initial_population(
        flows=flows,
        distances=distances,
        number_of_individuals=number_of_individuals
    )

    for individual in population:
        iterated_local_search.two_opt_improvement(
            individual=individual,
            worst_acceptance_probability=worst_acceptance_probability
        )

    population = iterated_local_search.sort_population(population=population)
    best_individual = deepcopy(population[0])
    number_of_shifts = 1
    last_mutated_generation = 0
    mutation_type = 1
    best_iteration = 0

    for generation in range(1, number_of_iterations + 1):
        offspring = []

        while len(offspring) < int(number_of_individuals * 0.5):
            if selection_algorithm == 'roulette_wheel':
                [parent1_individual, parent2_individual] = roulette_wheel_selection(
                    number_of_selections=2,
                    population=population
                )
            elif selection_algorithm == 'tournament':
                [parent1_individual, parent2_individual] = tournament_selection(
                    number_of_selections=2,
                    population=population,
                    number_of_individuals=number_of_individuals,
                    tournament_size=tournament_size
                )
            else:
                raise Exception(f'Unknown selection algorithm. Selection algorithm: {selection_algorithm}.')

            child_individual = crossover(
                parent1=parent1_individual,
                parent2=parent2_individual,
                number_of_facilities=number_of_facilities,
                flows=flows,
                distances=distances,
                crossover_rate=crossover_rate
            )

            improved_child_individual = limited_iterated_search(
                child_individual=child_individual,
                number_of_facilities=number_of_facilities,
                worst_acceptance_probability=worst_acceptance_probability
            )

            offspring.append(improved_child_individual)

        offspring = iterated_local_search.sort_population(population=offspring)

        for idx in range(len(offspring)):
            offspring_mapped_idx = number_of_individuals - 1 - idx
            if offspring[idx].objective_value < population[offspring_mapped_idx].objective_value:
                population[offspring_mapped_idx] = offspring[idx]

        population = iterated_local_search.sort_population(population=population)

        if population[0].objective_value >= best_individual.objective_value \
                and (generation - last_mutated_generation) > 100 \
                and (generation - best_iteration) > 200:
            if mutation_type == 1:
                for i in range(number_of_individuals):
                    shift_mutation(
                        individual=population[i],
                        number_of_shifts=number_of_shifts,
                        number_of_facilities=number_of_facilities
                    )

                number_of_shifts += 1
                if number_of_shifts > number_of_facilities:
                    number_of_shifts = 1
                    mutation_type = 2

                population = iterated_local_search.sort_population(population=population)
                last_mutated_generation = generation
            elif mutation_type == 2:
                for i in range(number_of_individuals):
                    perturbation(
                        individual=population[i],
                        number_of_perturbations=int(number_of_facilities * 0.2),
                        number_of_facilities=number_of_facilities
                    )

                    iterated_local_search.two_opt_improvement(
                        individual=population[i],
                        worst_acceptance_probability=worst_acceptance_probability
                    )

                population = iterated_local_search.sort_population(population=population)
                last_mutated_generation = generation
                mutation_type = 1

        if population[0].objective_value < best_individual.objective_value:
            best_individual = deepcopy(population[0])
            best_iteration = generation
            number_of_shifts = 1

        print(f'[GA] Iteration: {generation}. '
              f'Objective value: {best_individual.objective_value}.')

    print(f'[GA] Best individual found on iteration: {best_iteration}.')
    best_individual.normalize_final_assignments()

    return best_individual.assignments, best_individual.objective_value
