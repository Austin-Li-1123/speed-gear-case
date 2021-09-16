# Define machine IDs
'''
Chucker 1   -  0
Chucker 2   -  1
Chucker 3   -  2
Chucker A   -  3
Chucker B   -  4
Chucker C   -  5
Chucker D   -  6
Mill 1      -  7
Mill 2      -  8
Natco Drill -  9
'''

all_jobs = ["C17", "E26", "D20", "B15", "D25", "F35"]
# Definitions of all types of jobs in the speedgear case
# individual task format: (machine ID, process time).
C17 = [(0, 3), (3, 8), (7, 4), (9, 1.5)]
E26 = [(1, 6), (5, 9), (8, 4.5), (9, 2)]
D20 = [(2, 4.5), (5, 8), (8, 3), (9, 2)]
B15 = [(2, 6), (6, 8), (8, 2), (9, 1.5)]
D25 = [(2, 4.5), (6, 8), (8, 3), (9, 2)]
F35 = [(9, 3)]


# Function that return the job description given the name
def get_job_def(job_name):
    return globals()[job_name]

# print(get_job_def("C17")) #test


# Past order amounts
# ["C17", "E26", "D20", "B15", "D25", "F35"]
past_orders = [
    [12, 4,	2, 5, 11, 2],
    [14, 3, 3, 10, 2, 1],
    [2,	5, 4, 8, 3, 3],
]