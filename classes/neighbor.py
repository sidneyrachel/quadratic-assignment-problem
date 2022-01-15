import numpy as np
from utils import cost


class Neighbor:
    def __init__(self, number_of_facilities, flows, distances):
        self.members = np.zeros(number_of_facilities + 2, dtype=int).tolist()
        self.flows = flows
        self.distances = distances
        self.objective_value = 0

    def get_assignments(self):
        return self.members[:-2]

    def get_tabu_identifiers(self):
        return self.members[-2:]

    def set_assignments(self, assignments):
        self.members[:-2] = assignments

    def set_tabu_identifiers(self, tabu_identifiers):
        self.members[-2:] = tabu_identifiers

    def calculate_objective_value(self):
        self.objective_value = cost.calculate_objective_value(
            flows=self.flows,
            distances=self.distances,
            assignments=self.get_assignments()
        )
