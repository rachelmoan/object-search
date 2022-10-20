import math

class Node:
    def __init__(self, value, coordinates, neighbors=None):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.theta = coordinates[2]
        self.value = value
        self.heuristic_value = None
        self.distance_from_start = math.inf
        if neighbors is None: self.neighbors = []
        else: self.neighbors = neighbors
        self.parent = None

    def has_neighbors(self):
        if len(self.neighbors) == 0:
            return False
        return True

    def number_of_neighbors(self):
        return len(self.neighbors)

    def add_neighboor(self, neighboor):
        self.neighbors.append(neighboor)

    def extend_node(self):
        children = []
        for child in self.neighbors:
            children.append(child[0])
        return children
    
    def isGreaterThan(self, other):
        if isinstance(other, Node):
            if self.heuristic_value > other.heuristic_value:
                return True
            if self.heuristic_value < other.heuristic_value:
                return False
            return False
            
    def isEqual(self, other):
        if isinstance(other, Node):
            if self.x == other.x and self.y == other.y: return True
        return False

    def string(self):
        return str(self.x) + " , " + str(self.y)
        

class Graph:

    def __init__(self, nodes=None):
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes


    def add_node(self, node):
        self.nodes.append(node)


    def find_node(self, x, y):
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node 
        return None


    def add_edge(self, x1, y1, x2, y2, weight=1):
        node1 = self.find_node(x1, y1)        
        node2 = self.find_node(x2, y2)

        if (node1 is not None) and (node2 is not None):
            node1.add_neighboor((node2, weight))
            node2.add_neighboor((node1, weight))
        else:
            print("Error: One or more nodes were not found")


    def number_of_nodes(self):
        return f"The graph has {len(self.nodes)} nodes"


    def are_connected(self, x1, y1, x2, y2, node_two):
        node_one = self.find_node(x1, y1)
        node_two = self.find_node(x2, y2)

        for neighbor in node_one.neighbors:
            if neighbor[0].x == node_two.x and neighbor[0].y == node_two.y:
                return True
        return False

    def __str__(self):
        graph = ""
        for node in self.nodes:
            graph += f"{node.__str__()}\n" 
        return graph