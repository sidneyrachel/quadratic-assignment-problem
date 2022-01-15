# from ortools.linear_solver import pywraplp
# from ortools.sat.python import cp_model
# from ortools.init import pywrapinit
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     flows = [
#         [0, 79, 32, 57, 68, 99, 97, 80, 90, 10, 11, 49],
#         [79, 0, 96, 62, 55, 11, 79, 17, 28, 88, 62, 32],
#         [32, 96, 0, 89, 21, 33, 4, 26, 75, 78, 22, 45],
#         [57, 62, 89, 0, 23, 57, 68, 66, 32, 15, 12, 69],
#         [68, 55, 21, 23, 0, 33, 84, 54, 95, 5, 15, 10],
#         [99, 11, 33, 57, 33, 0, 14, 86, 29, 53, 97, 75],
#         [97, 79, 4, 68, 84, 14, 0, 95, 74, 15, 85, 56],
#         [80, 17, 26, 66, 54, 86, 95, 0, 34, 38, 79, 27],
#         [90, 28, 75, 32, 95, 29, 74, 34, 0, 22, 80, 43],
#         [10, 88, 78, 15, 5, 53, 15, 38, 22, 0, 41, 20],
#         [11, 62, 22, 12, 15, 97, 85, 79, 80, 41, 0, 55],
#         [49, 32, 45, 69, 10, 75, 56, 27, 43, 20, 55, 0]
#     ]
#
#     distances = [
#         [0, 78, 22, 43, 86, 8, 99, 5, 32, 89, 19, 69],
#         [78, 0, 2, 81, 24, 83, 92, 36, 31, 73, 96, 5],
#         [22, 2, 0, 38, 50, 32, 66, 73, 6, 8, 68, 16],
#         [43, 81, 38, 0, 53, 75, 40, 8, 63, 30, 30, 10],
#         [86, 24, 50, 53, 0, 41, 29, 68, 52, 83, 51, 52],
#         [8, 83, 32, 75, 41, 0, 68, 44, 0, 56, 82, 23],
#         [99, 92, 66, 40, 29, 68, 0, 46, 64, 79, 4, 64],
#         [5, 36, 73, 8, 68, 44, 46, 0, 74, 19, 56, 34],
#         [32, 31, 6, 63, 52, 0, 64, 74, 0, 2, 14, 95],
#         [89, 73, 8, 30, 83, 56, 79, 19, 2, 0, 43, 49],
#         [19, 96, 68, 30, 51, 82, 4, 56, 14, 43, 0, 8],
#         [69, 5, 16, 10, 52, 23, 64, 34, 95, 49, 8, 0]
#     ]
#
#     n = len(flows)
#
#     # row: facility, column: location
#     # x = {}
#
#     model = cp_model.CpModel()
#
#     # for i in range(n):
#     #     for j in range(n):
#     #         x[i, j] = solver.IntVar(0, 1, '')
#     #
#     # # each facility is assigned to exactly 1 location.
#     # for i in range(n):
#     #     solver.Add(solver.Sum([x[i, j] for j in range(n)]) == 1)
#     #
#     # # each location has exactly 1 facility.
#     # for j in range(n):
#     #     solver.Add(solver.Sum([x[i, j] for i in range(n)]) == 1)
#
#     assigned_facilities = []
#     for i in range(n):
#         assigned_facilities.append(model.NewIntVar(0, n - 1, ''))
#
#     model.AddAllDifferent(assigned_facilities)
#
#     # model_distances = []
#     # for i in range(n):
#     #     distance_row = []
#     #
#     #     for j in range(n):
#     #         distance_row.append(model.NewIntVar(distances[i][j], distances[i][j], ''))
#     #
#     #     model_distances.append(distance_row)
#
#     objective_terms = []
#     for i in range(n):
#         for j in range(n):
#             objective_terms.append(flows[i][j] * distances[assigned_facilities[i]][assigned_facilities[j]])
#
#     model.Minimize(sum(objective_terms))
#
#     solver = cp_model.CpSolver()
#     status = solver.Solve(model)
#
#     if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#         print(f'Total cost = {solver.ObjectiveValue()}\n')
#         for i in range(n):
#             print('Facility %d is assigned to location %d.' % (i + 1, solver.Value(assigned_facilities[i]) + 1))
