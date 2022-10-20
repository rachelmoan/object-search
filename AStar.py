'''
Given an environment, get the best viewpoints, and then plan a path using a*
'''

from environment import Environment
import math
from graph import Graph

class AStar:
    def __init__(self, graph, start_position, target):
        self.graph = graph
        self.start = graph.find_node(start_position)
        self.target = graph.find_node(target)
        self.opened = []
        self.closed = []
        self.number_of_steps = 0

    def manhattan_distance(self, node1, node2):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)


    def calculate_distance(self, parent, child):
        for neighbor in parent.neighbors:
            if neighbor[0] == child:
                distance = parent.distance_from_start + neighbor[1]
                if distance < child.distance_from_start:
                    child.parent = parent
                    return distance
            
                return child.distance_from_start


    def calculate_heuristic_value(self, parent, child, target):
        return self.calculate_distance(parent, child) + self.manhattan_distance(child, target)


    def insert_to_list(self, list_category, node):
        if list_category == "open":
            self.opened.append(node)
        else:
            self.closed.append(node)


    def remove_from_opened(self):
        

        node = self.opened.pop(0)
        self.closed.append(node)
        return node


    def opened_is_empty(self):
        return len(self.opened) == 0


    def get_old_node(self, node_value):

        for node in self.opened:
            if node.value == node_value:
                return node
        return None 
            

    def calculate_path(self, target_node):

        path = [target_node.value]
        node = target_node.parent
        while True:
            path.append(node.value)
            if node.parent is None:
                break
            node = node.parent
        return path


    def calculate_cost(self, path):

        total_cost = 0
        for i in range(len(path) - 1):
            child = self.graph.find_node(path[i])
            parent = self.graph.find_node(path[i+1])
            
            for neighbor in child.neighbors:
                # Structure of neighbor(Node, weight)
                if neighbor[0] == parent:
                    total_cost += neighbor[1]

        return total_cost
            

    def search(self):

        # Calculate the heuristic value of the starting node
        # The distance from the starting node is 0 so only manhattan_distance is calculated
        self.start.distance_from_start = 0
        self.start.heuristic_value = self.manhattan_distance(self.start, self.target)
        # Add the starting point to opened list
        self.opened.append(self.start)

        while True:
            self.number_of_steps += 1

            if self.opened_is_empty():
                print(f"No Solution Found after {self.number_of_steps} steps!!!")
                break
            
            selected_node = self.remove_from_opened()
            # print(f"Selected Node {selected_node} has parent {selected_node.parent}")
            # check if the selected_node is the solution
            if selected_node == self.target:
                path = self.calculate_path(selected_node)
                total_cost = self.calculate_cost(path)
                path.reverse()
                return path, total_cost

            # extend the node
            new_nodes = selected_node.extend_node()

            # add the extended nodes in the list opened
            if len(new_nodes) > 0:
                for new_node in new_nodes:
                    
                    new_node.heuristic_value = self.calculate_heuristic_value(selected_node, new_node, self.target)
                    if new_node not in self.closed and new_node not in self.opened:
                        new_node.parent = selected_node
                        self.insert_to_list("open", new_node)
                    elif new_node in self.opened and new_node.parent != selected_node:
                        old_node = self.get_old_node(new_node.value)
                        if new_node.heuristic_value < old_node.heuristic_value:
                            new_node.parent = selected_node
                            self.insert_to_opened(new_node)



