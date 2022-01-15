from utils import file, constraint_solving


if __name__ == '__main__':
    flows, distances = file.read_external_file('test.dat')
    constraint_solving.run_minizinc(flows=flows, distances=distances)
