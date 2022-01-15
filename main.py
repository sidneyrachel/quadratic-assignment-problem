from utils import file, iterated_local_search, tabu_search, constraint_solving


config = {
    'iterated_local_search': {
        'worst_acceptance_probability': 0.0,
        'number_of_iterations': 1000,  # 10000
        'number_of_individuals': 5,
        'shuffle_tolerance': 10,
        'number_of_shuffles': 15,
        'local_improvement_iterations': 1000,
        'local_improvement_mode': 'two_opt'
    },
    'tabu_search': {
        'tabu_size': 20,
        'number_of_iterations': 100
    }
}

if __name__ == '__main__':
    flows, distances = file.read_external_file('had12.dat')

    algorithm = 'iterated_local_search'

    if algorithm == 'iterated_local_search':
        algorithm_config = config['iterated_local_search']

        assignments, objective_value = iterated_local_search.run_iterated_local_search(
            flows,
            distances,
            number_of_individuals=algorithm_config['number_of_individuals'],
            number_of_iterations=algorithm_config['number_of_iterations'],
            shuffle_tolerance=algorithm_config['shuffle_tolerance'],
            number_of_shuffles=algorithm_config['number_of_shuffles'],
            local_improvement_iterations=algorithm_config['local_improvement_iterations'],
            worst_acceptance_probability=algorithm_config['worst_acceptance_probability'],
            local_improvement_mode=algorithm_config['local_improvement_mode']
        )
    elif algorithm == 'tabu_search':
        algorithm_config = config['tabu_search']

        assignments, objective_value = tabu_search.run_tabu_search(
            flows,
            distances,
            tabu_size=algorithm_config['tabu_size'],
            number_of_iterations=algorithm_config['number_of_iterations']
        )
    elif algorithm == 'constraint_solving':
        assignments, objective_value = constraint_solving.run_minizinc(flows=flows, distances=distances)
    else:
        raise Exception(f'Algorithm is unknown. Algorithm: {algorithm}.')

    print(f'Best assignments: {assignments}. Objective value: {objective_value}.')
