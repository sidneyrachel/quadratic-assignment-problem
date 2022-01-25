def read_matrix(lines, current_idx, n):
    matrix = []

    for i in range(current_idx, current_idx + n):
        raw_row = lines[i].split(' ')
        row = []

        for element in raw_row:
            if element != '':
                row.append(int(element))

        matrix.append(row)

    return matrix


def read_external_file(filename):
    filepath = 'qapdata/' + filename
    file = open(filepath, 'r')
    lines = [line.strip() for line in file.readlines()]

    current_idx = 0

    n = int(lines[current_idx])

    current_idx = current_idx + 2
    read_flows = read_matrix(lines=lines, current_idx=current_idx, n=n)

    current_idx = current_idx + n + 1
    read_distances = read_matrix(lines=lines, current_idx=current_idx, n=n)

    if len(read_flows) != n:
        raise Exception(f'Flows length is not equal to {n}. Flows length: {len(read_flows)}.')

    for row in read_flows:
        if len(row) != n:
            raise Exception(f'Flows row length is not equal to {n}. Flows row length: {len(row)}.')

    if len(read_distances) != n:
        raise Exception(f'Distances length is not equal to {n}. Distances length: {len(read_distances)}.')

    for row in read_distances:
        if len(row) != n:
            raise Exception(f'Distances row length is not equal to {n}. Distances row length: {len(row)}.')

    return read_flows, read_distances
