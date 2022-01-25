from utils import cost
from utils import assignment


class Individual:
    def __init__(self, assignments, flows, distances):
        self.assignments = assignments
        self.number_of_facilities = len(assignments)
        self.objective_value = 0
        self.flows = flows
        self.distances = distances
        self.calculate_objective_value()

    def calculate_value_swap(self, facility1, facility2):
        self.objective_value += cost.calculate_value_swap(
            assignments=self.assignments,
            facility1=facility1,
            facility2=facility2,
            flows=self.flows,
            distances=self.distances
        )

    def exchange(self, facility1, facility2):
        self.calculate_value_swap(facility1=facility1, facility2=facility2)
        temp = self.assignments[facility1]
        self.assignments[facility1] = self.assignments[facility2]
        self.assignments[facility2] = temp

    def calculate_objective_value(self):
        self.objective_value = cost.calculate_objective_value(
            flows=self.flows,
            distances=self.distances,
            assignments=self.assignments
        )

    def normalize_final_assignments(self):
        assignment.normalize_final_assignments(assignments=self.assignments)

    def __str__(self):
        return f'{self.assignments} {self.objective_value}'
