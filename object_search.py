import environment 
from AStar import AStar
from graph import Graph
from node import Node
import math


def run():
    # Create graph
    g = Graph()
    # Add vertices
    g.add_node(Node('S', (1,1)))
    g.add_node(Node('B', (1,2)))
    g.add_node(Node('C', (1,4)))
    g.add_node(Node('D', (2,1)))
    g.add_node(Node('E', (2,2)))
    g.add_node(Node('F', (2,3)))
    g.add_node(Node('G', (2,4)))
    g.add_node(Node('H', (3,1)))
    g.add_node(Node('I', (3,4)))
    g.add_node(Node('J', (4,1)))
    g.add_node(Node('K', (4,2)))
    g.add_node(Node('T', (4,3)))
    g.add_node(Node('L', (4,4)))
    
    # Add edges
    g.add_edge('S', 'B', 4)
    g.add_edge('S', 'D', 5)
    g.add_edge('B', 'E', 1)
    g.add_edge('C', 'G', 1)
    g.add_edge('D', 'E', 2)
    g.add_edge('D', 'H', 3)
    g.add_edge('E', 'F', 6)
    g.add_edge('F', 'G', 4)
    g.add_edge('G', 'I', 3)
    g.add_edge('H', 'J', 1)
    g.add_edge('I', 'L', 4)
    g.add_edge('J', 'K', 6)
    g.add_edge('K', 'T', 2)
    g.add_edge('T', 'L', 3)

    # Execute the algorithm
    alg = AStar(g, "S", "T")
    path, path_length = alg.search()
    print(" -> ".join(path))
    print(f"Length of the path: {path_length}")

if __name__ == '__main__':

    env = environment.Environment(display_environment=True, 
                 screen_height =480, 
                 fov=math.pi / 3, 
                 casted_rays=120, 
                 map_length=8, 
                 map_height=8,
                 player_angle=math.pi
                 )

    g = Graph()

    obstacle_map = env.obstacle_map

    length = env.map_length
    height = env.map_height

    candidate_points = []

    for i in range(height-1):
        print(i)
        for j in range(length-1):
            if not obstacle_map[i][j]:
                # this is not an obstacle, so we can add the 4 corners as nodes, all connected to each other
                x1 = i*env.tile_size
                y1 = j*env.tile_size
                x2 = (i+1)*env.tile_size
                y2 = (j+1)*env.tile_size

                print(x1)

                g.add_node(Node(f'{str(x1)}, {str(y1)}', (x1,y1)))
                g.add_node(Node(f'{str(x1)}, {str(y2)}', (x1,y2)))
                g.add_node(Node(f'{str(x2)}, {str(y1)}', (x2,y1)))
                g.add_node(Node(f'{str(x2)}, {str(y2)}', (x2,y2)))

                g.add_edge(f'{str(x1)}, {str(y1)}', f'{str(x1)}, {str(y2)}', 1)
                g.add_edge(f'{str(x1)}, {str(y1)}', f'{str(x2)}, {str(y1)}', 1)
                g.add_edge(f'{str(x2)}, {str(y2)}', f'{str(x1)}, {str(y2)}', 1)
                g.add_edge(f'{str(x2)}, {str(y2)}', f'{str(x2)}, {str(y1)}', 1)



    #for i in range(len(g.nodes)):
    #    print(f'x = {g.nodes[i].x}, y = {g.nodes[i].y}, value = {g.nodes[i].value}')



    # Execute the algorithm
    alg = AStar(g, '60.0, 60.0', '300.0, 300.0')

    print(alg.start)

    path, path_length = alg.search()
    print(" -> ".join(path))
    print(f"Length of the path: {path_length}")