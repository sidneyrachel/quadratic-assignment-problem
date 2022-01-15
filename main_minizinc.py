import time
from minizinc import Instance, Model, Solver
from utils import file


def solve():
    qap = Model('../qap.mzn')
    geocode = Solver.lookup('gecode')
    instance = Instance(geocode, qap)
    instance['n'] = len(flows)
    instance['flows'] = flows
    instance['distances'] = distances

    start_time = time.time()

    print("Start solving...")

    result = instance.solve(intermediate_solutions=True)

    execution_time = time.time() - start_time

    print(f"Execution time: {execution_time} s")

    for i in range(len(result)):
        print(result[i])


if __name__ == '__main__':
    flows, distances = file.read_external_file('test.dat')
    solve()
