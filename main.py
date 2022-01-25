from utils import file, \
    iterated_local_search, \
    tabu_search, \
    constraint_solving, \
    genetic_algorithm
from datetime import datetime
import argparse

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
    parser = argparse.ArgumentParser(description='Algorithms for solving quadratic assignment problem.')
    parser.add_argument(
        '-a',
        '--algorithm',
        help='Choose one of the algorithms: ils (iterative local search), '
             'ts (tabu search), '
             'cs (constraint solving with Minizinc). Example: ils.',
        required=True
    )
    parser.add_argument(
        '-f',
        '--filename',
        help='Choose filename of the problem from qapdata folder. Example: had12.dat.',
        required=True
    )
    # iterative local search
    parser.add_argument(
        '-iwap',
        '--iterative_worst_acceptance_probability',
        help='Worst acceptance probability in iterative local search.',
        type=float,
        default=config['iterated_local_search']['worst_acceptance_probability']
    )
    parser.add_argument(
        '-inoit',
        '--iterative_number_of_iterations',
        help='Number of iterations in iterative local search.',
        type=int,
        default=config['iterated_local_search']['number_of_iterations']
    )
    parser.add_argument(
        '-inoin',
        '--iterative_number_of_individuals',
        help='Number of individuals in iterative local search.',
        type=int,
        default=config['iterated_local_search']['number_of_individuals']
    )
    parser.add_argument(
        '-ist',
        '--iterative_shuffle_tolerance',
        help='Shuffle tolerance in iterative local search.',
        type=int,
        default=config['iterated_local_search']['shuffle_tolerance']
    )
    parser.add_argument(
        '-inos',
        '--iterative_number_of_shuffles',
        help='Number of shuffles in iterative local search.',
        type=int,
        default=config['iterated_local_search']['number_of_shuffles']
    )
    parser.add_argument(
        '-ilii',
        '--iterative_local_improvement_iterations',
        help='Local improvement iterations in iterative local search.',
        type=int,
        default=config['iterated_local_search']['local_improvement_iterations']
    )
    parser.add_argument(
        '-ilim',
        '--iterative_local_improvement_mode',
        help='Local improvement mode in iterative local search. Example: two_opt, three_opt, four_opt.',
        default=config['iterated_local_search']['local_improvement_mode']
    )
    # tabu search
    parser.add_argument(
        '-ts',
        '--tabu_size',
        help='Tabu size in tabu search.',
        type=int,
        default=config['tabu_search']['tabu_size']
    )
    parser.add_argument(
        '-tnoit',
        '--tabu_number_of_iterations',
        help='Number of iterations in tabu search.',
        type=int,
        default=config['tabu_search']['number_of_iterations']
    )
    args = vars(parser.parse_args())

    flows, distances = file.read_external_file(args['filename'])

    start_time = datetime.now()

    if args['algorithm'] == 'ils':
        assignments, objective_value = iterated_local_search.run_iterated_local_search(
            flows=flows,
            distances=distances,
            number_of_individuals=args['iterative_number_of_individuals'],
            number_of_iterations=args['iterative_number_of_iterations'],
            shuffle_tolerance=args['iterative_shuffle_tolerance'],
            number_of_shuffles=args['iterative_number_of_shuffles'],
            local_improvement_iterations=args['iterative_local_improvement_iterations'],
            worst_acceptance_probability=args['iterative_worst_acceptance_probability'],
            local_improvement_mode=args['iterative_local_improvement_mode']
        )
    elif args['algorithm'] == 'ts':
        algorithm_config = config['tabu_search']

        assignments, objective_value = tabu_search.run_tabu_search(
            flows=flows,
            distances=distances,
            tabu_size=args['tabu_size'],
            number_of_iterations=args['tabu_number_of_iterations']
        )
    elif args['algorithm'] == 'cs':
        assignments, objective_value = constraint_solving.run_minizinc(flows=flows, distances=distances)
    elif args['algorithm'] == 'ga':
        assignments, objective_value = genetic_algorithm.run_genetic_algorithm(
            flows=flows,
            distances=distances,
            number_of_individuals=3,
            crossover_rate=0.7,
            number_of_iterations=1000,
            worst_acceptance_probability=0.1,
            tournament_size=4,
            selection_algorithm='tournament'
        )
    else:
        raise Exception(f"Algorithm is unknown. Algorithm: {args['algorithm']}.")

    end_time = datetime.now()

    print(f'Best assignments: {assignments}. Objective value: {objective_value}.')
    print(f'Duration: {end_time - start_time}')
