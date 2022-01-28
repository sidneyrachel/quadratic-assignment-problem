# Quadratic Assignment Problem
This repository contains implementations of iterated local search (ILS), improved hybrid genetic algorithm (IHGA), tabu search (TS), and constraint solving (CS) to solve quadratic assignment problem (QAP) in Python programming language.

## Prerequisite
To be able to run the program, you need to:
1. Install [MiniZinc](https://www.minizinc.org/) 2.5.0+.
2. Install [Python](https://www.python.org/) 3.6.0+.
3. Install [MiniZinc Python library](https://pypi.org/project/minizinc/): `pip install minizinc`.
4. Install [NumPy Python library](https://pypi.org/project/numpy/): `pip install numpy`.
5. Download `qapdata.tar.gz` from [QAPLIB](https://www.opt.math.tugraz.at/qaplib/inst.html).
6. Unzip `qapdata.tar.gz` to `qapdata` and place the folder inside the root folder.

## Run the Program
### Iterated Local Search
Run the following command in the terminal:
`python main.py -a ils -f <instance-filename>`
The available options for the parameters are:
| Command | Default Value | Description |
|--|--|--|
| `-iwap` | `0.0` | Worst acceptance probability used for local improvement.  |
| `-inoit` | `1000` | Number of iterations. |
| `-inoin` | `max(5, int(0.1 * number of facilities))` | Number of individuals in the population. |
| `-ist` | `10` | Shuffle tolerance. If after `ist` number of iterations there is no improvement in the objective score, we will run perturbation. |
| `-inos` | `15` | Number of perturbations performed for each individual. |
| `-ilim` | `two_opt` | Type of local improvement: `two_opt`, `three_opt`, `four_opt`. |
| `-ilii` | `1000` | Number of local improvement iterations. It is only used in `three_opt` and `four_opt`. |

### Improved Hybrid Genetic Algorithm
Run the following command in the terminal:
`python main.py -a ga -f <instance-filename>`
The available options for the parameters are:
| Command | Default Value | Description |
|--|--|--|
| `-gnoin` | `max(5, int(0.1 * number of facilities))` | Number of individuals in the population. |
| `-gcr` | `0.8` | Crossover rate. |
| `-gnoit` | `1000` | Number of iterations. |
| `-gwap` | `0.0` | Worst acceptance probability used for local improvement.  |
| `-gts` | `5` | Tournament size used in tournament selection algorithm.  |
| `-gsa` | `tournament` | Selection algorithm: `roulette_wheel`, `tournament`. |

### Tabu Search
Run the following command in the terminal:
`python main.py -a ts -f <instance-filename>`
The available options for the parameters are:
| Command | Default Value | Description |
|--|--|--|
| `-ts` | `20` | Tabu size. |
| `-tnoit` | `100` | Number of iterations. |

### Constraint Solving
Run the following command in the terminal:
`python main.py -a cs -f <instance-filename>`