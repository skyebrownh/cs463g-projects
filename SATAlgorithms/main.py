import matplotlib.pyplot as plt
import os
from SATAlgorithms import Resolution, LocalSearch, GSAT
from CNFParser import CNFParser


# def plot_outcomes(title, x_label, x, y_label, y):
#     plt.plot(x, y)
#     plt.title(title)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.savefig(f'{"-".join(title.split(" "))}.png')


directories = ['CNF Formulas', 'HARD CNF Formulas']

# resolution graph data is list of tuples (x, y): (True/False, time)
resolution_data = []
# graph data is list of tuples (x, y): (c-value, time)
local_search_data = []
gsat_data = []

# Load files and run LocalSearch and GSAT
for directory in directories:
    print(f'Local Search & GSAT on {directory}:')
    for filename in os.listdir(directory):
        if not filename.endswith('.cnf') and not filename.endswith('.rncf'):
            continue

        curr_file = os.path.join(directory, filename)
        print(f'Running {filename}...')

        # parse
        curr_data = CNFParser.read_cnf(curr_file)

        # pass parsed data to each algorithm, collect data on each
        l = LocalSearch(curr_data)
        l.run()
        local_search_data.append((l.c, l.time_taken))
        # print(f'Local Search: {l.c} / {len(l.phi)}')

        g = GSAT(curr_data)
        g.run()
        gsat_data.append((g.c, g.time_taken))
        # print(f'GSAT: {g.c} / {len(g.phi)}')

# graph data from this set of formulas
ls_x = [p[0] for p in local_search_data]
ls_y = [p[1] for p in local_search_data]
plt.subplot(211)
plt.scatter(ls_x, ls_y)
plt.title('Local Search')
plt.xlabel('c-value')
plt.ylabel('time (s)')

gsat_x = [p[0] for p in gsat_data]
gsat_y = [p[1] for p in gsat_data]
plt.subplot(212)
plt.scatter(gsat_x, gsat_y)
plt.title('GSAT')
plt.xlabel('c-value')
plt.ylabel('time (s)')

plt.savefig('ls-gsat-outcomes.png')

# Load files and run Resolution
for directory in directories:
    print(f'Resolution on {directory}:')
    for filename in os.listdir(directory):
        if not filename.endswith('.cnf') and not filename.endswith('.rncf'):
            continue

        curr_file = os.path.join(directory, filename)
        print(f'Running {filename}...')

        # parse
        curr_data = CNFParser.read_cnf(curr_file)

        r = Resolution(curr_data)
        result = r.run()
        resolution_data.append((result, r.time_taken))
        # print(f'Resolution: {result}')

# Print Resoultion outcomes
sat_times = 0
sat_count = 0
unsat_times = 0
unsat_count = 0

for p in resolution_data:
    if p[0]:
        sat_count += 1
        sat_times += p[1]
    else:
        unsat_count += 1
        unsat_times += p[1]

print(f'*****\nAverage time (satisfiable): {sat_times / sat_count}\n')
print(f'*****\nAverage time (unsatisfiable): {unsat_times / unsat_count}\n')
