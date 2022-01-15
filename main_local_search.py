# reference:
# https://github.com/shah314/cilsassignment/blob/master/cILSAssignment.cpp
# https://github.com/BlackMooth/Quadratic-Assignment-Problem
# https://github.com/Lolik-Bolik/Quadratic_Assign_Problem/blob/master/algorithms/iterated_local_search.py

from utils import file, iterated_local_search

config = {
    'iterated_local_search': {
        'worst_acceptance_probability': 0.0,
        'number_of_iterations': 1000,  # 10000
        'number_of_individuals': 5,
        'shuffle_tolerance': 10,
        'number_of_shuffles': 15,
        'local_improvement_iterations': 1000,
        'local_improvement_mode': 'two_opt'
    }
}

if __name__ == '__main__':
    flows, distances = file.read_external_file(filename='had12.dat')
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

    print(f'Best assignments: {assignments}. Objective value: {objective_value}.')
