import matplotlib.pyplot as plt
from MasterPyraminxModel.Pyraminx import Pyraminx
from AStarAlgorithm import AStarAlgorithm


def generate_instances(k):
    puzzles = []
    for n in range(5):
        instance = Pyraminx()
        instance.randomize(k)
        puzzles.append(instance)
    return puzzles


# x: actual distance to solution, y: nodes expanded on last iteration of A*
def plot_outcomes(x, y):
    plt.plot(x, y)
    plt.title("A* Node Expansion")
    plt.xlabel("k")
    plt.ylabel("average nodes expanded")
    plt.axis([3, 10, 0, max(y)])
    plt.show()


# ----- MAIN -----
parameters = [3, 4, 5, 6, 7, 8, 9, 10]
graph_data = []  # average number of nodes expanded for each k
for k in parameters:
    # generate 5 k-randomized puzzles
    puzzles = generate_instances(k)

    # hold number of nodes expanded for all instances of this k value
    expanded_nodes = []

    # run A* to solve each puzzle
    for p in puzzles:
        a_star = AStarAlgorithm(p)
        a_star.run()
        print(a_star.expanded_nodes)
        expanded_nodes.append(a_star.expanded_nodes)

    # average expanded nodes for this k and add to graph_data
    nodes_sum = 0
    for num in expanded_nodes:
        nodes_sum += num
    average = nodes_sum / len(expanded_nodes)
    print(average)
    graph_data.append(average)

print(graph_data)
# plot expanded nodes data
plot_outcomes(parameters, graph_data)
