from minizinc import Instance, Model, Solver


def run_minizinc(flows, distances):
    qap = Model('../qap.mzn')
    geocode = Solver.lookup('gecode')
    instance = Instance(geocode, qap)
    instance['n'] = len(flows)
    instance['flows'] = flows
    instance['distances'] = distances

    result = instance.solve(intermediate_solutions=True)
    result_len = len(result)

    for idx in range(result_len):
        print(f'Solution: {idx}. '
              f'Assignments: {result[idx].assigned_facilities}. '
              f'Objective: {result[idx].objective}.')

        if idx == result_len - 1:
            return result[idx].assigned_facilities, result[idx].objective
