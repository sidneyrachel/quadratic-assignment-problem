# Reference:
# https://github.com/Giant316/quadraticAssignment/blob/main/QAP.ipynb
# https://github.com/100/Solid/blob/master/Solid/TabuSearch.py

from utils import file
from utils import tabu_search

config = {
    'tabu_search': {
        'tabu_size': 20,
        'number_of_iterations': 100
    }
}

if __name__ == '__main__':
    flows, distances = file.read_external_file(filename='had12.dat')
    algorithm_config = config['tabu_search']

    assignments, objective_value = tabu_search.run_tabu_search(
        flows,
        distances,
        tabu_size=algorithm_config['tabu_size'],
        number_of_iterations=algorithm_config['number_of_iterations']
    )

    print(f'Best assignments: {assignments}. Objective value: {objective_value}.')
