from copy import deepcopy
from MasterPyraminxModel.Pyraminx import Pyraminx


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g = 0  # distance to start node
        self.h = 0  # distance to goal node
        self.f = 0  # total cost

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state


class AStarAlgorithm:
    center = (0, 1.5)
    corners = [(0, 3.5), (-1.5, 0.5), (1.5, 0.5)]
    edges = [(-0.5, 2.5), (-1, 1.5), (-0.5, 0.5), (0.5, 0.5), (0.5, 2.5), (1, 1.5)]
    interiors = [(0, 2.5), (-0.5, 1.5), (0.5, 1.5), (-1, 0.5), (0, 0.5), (1, 0.5)]

    def __init__(self, pyraminx):
        self.start_node = Node(pyraminx, None)
        self.goal_node = Node(Pyraminx(), None)  # un-randomized / solved Pyraminx
        self.expanded_nodes = 0
        self.open = []
        self.closed = []

    @staticmethod
    def heuristic(node):
        pyraminx = node.state

        corner_h, edge_h, interior_h = 0, 0, 0
        corner_oop, edge_oop, interior_oop = 0, 0, 0

        for f in pyraminx.faces:
            center_color = f.get_piece(AStarAlgorithm.center).color
            for c in AStarAlgorithm.corners:
                if f.get_piece(c).color != center_color:
                    corner_oop += 1
            for e in AStarAlgorithm.edges:
                if f.get_piece(e).color != center_color:
                    edge_oop += 1
            for i in AStarAlgorithm.interiors:
                if f.get_piece(i).color != center_color:
                    interior_oop += 1

        corner_h = corner_oop / 3
        edge_h = edge_oop / 6
        interior_h = interior_oop / 9

        return max(corner_h, edge_h, interior_h)

    # NOTE: clockwise is used to randomize, so counterclockwise will be used to solve
    def run(self):
        self.open.append(self.start_node)

        while len(self.open) > 0:
            print(self.expanded_nodes)
            # sort the open list to get the Node with lowest f
            self.open.sort()
            current_node = self.open.pop(0)

            # add current_node to closed list
            self.closed.append(current_node)

            # check if we have reached the goal node and return path
            if current_node == self.goal_node:
                print('DONE')
                break
                # # calculate path from start to end
                # path = []
                # while current_node != self.start_node:
                #     path.append(current_node.state)
                #     current_node = current_node.parent
                # # return the reversed path
                # return path[::-1]

            # increment expanded_nodes
            self.expanded_nodes += 1

            # get neighbors to this current_node.state: loop through the 3 orientations and make move on each level
            neighbors = []
            for o in range(1, 4):
                for level in [0.5, 1.5, 2.5, 3.5]:
                    new_neighbor = Pyraminx(data=deepcopy(current_node.state.faces))
                    new_neighbor.single_move(100, level, 'counterclockwise')
                    neighbors.append(new_neighbor)
                current_node.state.rotate()

            # loop over neighbor states
            for n in neighbors:
                # create Node from this neighbor state
                neighbor_node = Node(n, current_node)

                # if neighbor node is in closed list, skip to next iteration
                if neighbor_node in self.closed:
                    continue

                # else, generate neighbor node g, h, and f values
                if current_node == self.start_node:
                    neighbor_node.g = 1
                else:
                    neighbor_node.g = neighbor_node.parent.g + 1
                neighbor_node.h = AStarAlgorithm.heuristic(neighbor_node)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                # add neighbor to open if it passes add_to_open check
                if self.add_to_open(neighbor_node):
                    self.open.append(neighbor_node)

        # return None if no path is found
        return None

    # check if a neighbor should be added to the open list
    def add_to_open(self, neighbor):
        if len(self.open) == 0:
            return True

        for node in self.open:
            if neighbor == node and neighbor.f >= node.f:
                return False

        return True
