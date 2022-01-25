from random import choice


def normalize_final_assignments(assignments):
    for i in range(len(assignments)):
        assignments[i] += 1


def choose_random_element(member_set, excluded_member_set):
    return choice(list(member_set - excluded_member_set))
