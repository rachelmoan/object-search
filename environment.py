# Class representing the environment in which we are searching
# This includes the locations of obstacles and probability  map
import pygame
import sys
import math
import cv2
import numpy as np

class Environment:
    def __init__(self, 
                 display_environment, 
                 screen_height, 
                 fov=math.pi / 3, 
                 casted_rays=120, 
                 map_length=10, 
                 map_height=10,
                 player_angle=math.pi
                 ):

        self.screen_height = 480
        self.display_environment = display_environment
        self.screen_width = screen_height * 2
        self.map_size = 10
        self.tile_size = ((self.screen_width / 2) / self.map_size)
        self.max_depth = int(self.map_size * self.tile_size)
        self.fov = fov
        self.half_fov = fov / 2
        self.casted_rays = casted_rays # no. of rays that we will cast
        self.step_angle = fov / casted_rays
        self.scale = (self.screen_width / 2) / casted_rays
        self.map_length = 10
        self.map_height = 10

        # The current location of the person controlling the point robot
        # is denoted as (player_x, player_y, player_angle)
        self.player_x = self.tile_size*2
        self.player_y = self.tile_size*2
        self.player_angle = player_angle

        self.obstacle_map = self.get_obstacle_map()
        self.probability_matrix = self.get_prob_map()

        self.true_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.confusion = [
            [.9, .1],
            [.1, .9] 
        ]

        if self.display_environment:
            pygame.init()
            self.win = pygame.display.set_mode((self.screen_width,self.screen_height))
            pygame.display.set_caption("Visibility!")
            self.clock = pygame.time.Clock()


    def get_obstacle_map(self):
        map = [[True, True, True, True, True, True, True, True, True, True], 
       [True, False, False, False, True, True, False, False, False,True], 
       [True, False, False, False, False, False, False, False, False,True],
       [True, False, False, False, False, True, True, False, False,True],
       [True, False, False, False, False, False, False, False, False,True],
       [True, False, False, False, False, True, True, False, False,True],
       [True, True, False, False, False, False, False, False, False,True],
       [True, False, False, False, True, False, False, False, False,True],
       [True, False, False, False, True, False, False, False, False,True],
       [True, True, True, True, True, True, True, True, True, True]]

        return map

    # read in the color values from heatmap
    def read_as_digital(self, image, cell_size, offset_x, offset_y):
        # grab the image dimensions
        h = image.shape[0]
        w = image.shape[1]
        results = []
        # loop over the image, cell by cell 
        for y in range(offset_y[0], h-offset_y[1]-cell_size + 1, cell_size):
            row = []
            for x in range(offset_x[0], w-offset_x[0]-cell_size + 1, cell_size):
                # append heatmap cell color to row
                row.append(image[y+int(cell_size/2),x+int(cell_size/2)])
            results.append(row)

        return results


    def get_prob_map(self):
        image = cv2.imread("grid1.png",1)

        results = self.read_as_digital(image, int(self.tile_size),[0,0],[0,0])
        clean_results = []

        # clean up the result to be able to convert to heatmap
        rows = len(results)
        cols = len(results[0])

        for i in range(len(results)):
            clean_results.append([])
            for j in range(len(results[i])):
                clean_results[i].append(float(results[i][j][0]/255))

        return np.asarray(clean_results)

    def draw_map(self):
        self.win.fill((0,0,0))

        font = pygame.font.SysFont('Monospace Regular', 30)
        for row in range(self.map_length):
            for col in range(self.map_height):
                #square = row * MAP_SIZE + col
                
                pygame.draw.rect(self.win,
                                 (200,200,200) if self.obstacle_map[row][col]  else (100,100,100),
                                 (col * self.tile_size, row * self.tile_size, self.tile_size - 2, self.tile_size - 2)
                    
                                )  

    
        pygame.draw.circle(self.win, 
                           (255, 0, 0), 
                           (int(self.player_x),
                           int(self.player_y)), 
                           8)

        pygame.draw.line(self.win, 
                         (0,255,0),
                         (self.player_x,self.player_y),
                         (self.player_x - math.sin(self.player_angle) * 50,self.player_y + math.cos(self.player_angle) * 50),
                         3)

        pygame.draw.line(self.win, 
                         (0,255,0),
                         (self.player_x,self.player_y),
                         (self.player_x - math.sin(self.player_angle - self.half_fov) * 50,self.player_y + math.cos(self.player_angle - self.half_fov) * 50),
                         3)

        pygame.draw.line(self.win, 
                         (0,255,0),
                         (self.player_x,self.player_y),
                         (self.player_x - math.sin(self.player_angle + self.half_fov) * 50,self.player_y + math.cos(self.player_angle + self.half_fov) * 50),
                         3)

    def colfunc(self, val, minval, maxval, startcolor, stopcolor):
        f = float(val-minval) / (maxval-minval)
        return tuple(100*(f*(b-a)+a) for (a, b) in zip(startcolor, stopcolor))
        
    def draw_prob_map(self, probability_matrix):
    
        # get the current probability map

        RED, YELLOW, GREEN  = (1, 0, 0), (1, 1, 0), (0, 1, 0)
        CYAN, BLUE, MAGENTA = (0, 1, 1), (0, 0, 1), (1, 0, 1)

        font = pygame.font.SysFont('Monospace Regular', 30)
        for row in range(self.map_length):
            for col in range(self.map_height):

                prob = self.probability_matrix[row][col]
                color = self.colfunc(prob, 0, 1, BLUE, GREEN)
                #print("color = ", color)
                
                pygame.draw.rect(
                    self.win,
                    color,
                    (self.screen_height + col * self.tile_size, row * self.tile_size, self.tile_size - 2, self.tile_size - 2)
                    )  

                pr = str(math.floor(self.probability_matrix[row][col] * 100000)/100000.0)

                

                self.win.blit(font.render(pr, True, (255,255,255)), ( self.screen_height  + col * self.tile_size + 20, row * self.tile_size + 20))        
        
        return

    def get_cells_in_viewpoint(self, viewpoint, num_casted_rays, max_depth):
        visible_cells = []
        x = viewpoint[0]
        y = viewpoint[1]
        angle = viewpoint[2]
        start_angle = angle - self.half_fov
        
        for ray in range(self.casted_rays):
            for depth in range(self.max_depth):
                target_x = x - math.sin(start_angle) * depth
                target_y = y + math.cos(start_angle) * depth
                col = int(target_x / self.tile_size)
                row = int(target_y / self.tile_size)


                # uncomment this block to draw visible cells in red
                '''
                if self.display_environment: 
                    
                    pygame.draw.rect(self.win,
                                    (200,0,0) ,
                                    (col * self.tile_size, row * self.tile_size, self.tile_size - 2, self.tile_size - 2)
                                    ) 
                '''

                if ([row,col] not in visible_cells):
                    visible_cells.append([row,col])
    
                if self.obstacle_map[row][col]:

                    if self.display_environment: pygame.draw.line(self.win, (255,255,0),(x,y),(target_x,target_y))
                    color = 50 / (1 + depth * depth * 0.0001)
                    
                    depth *= math.cos(angle - start_angle)
                        
                    wall_height = 21000 / (depth + 0.0001)
                    
                    if wall_height > self.screen_height: wall_height == self.screen_height

                    
                    break
        
            start_angle += self.step_angle


        #print(f"visible cells are {visible_cells}")
        return visible_cells

    def make_observation(self, viewpoint):
        # get the cells in the viewpoint

        cells_in_viewpoint = self.get_cells_in_viewpoint(viewpoint, 800, 480)
        
        total = 0
        for cell in cells_in_viewpoint:
            total += self.true_map[cell[0]][cell[1]]

        if total == 1:
            bias_to_see = self.confusion[0][0] # true positive
        else: bias_to_see = self.confusion[1][0] # false positive

        # Sample a random observation
        # Bias this choice using the probability that is currently in the cell
        obs = np.random.choice([0,1], p=[1-bias_to_see, bias_to_see])

        return obs

    def update_map(self, viewpoint):

        cells_in_viewpoint = self.get_cells_in_viewpoint(viewpoint, 800, 480)
        total_num_cells = len(cells_in_viewpoint)

        obs = self.make_observation(viewpoint)

        # now update the probability for each cell that is visible from this viewpoint
        for cell in cells_in_viewpoint:
            x = cell[0]
            y = cell[1]

            # Account for the probability that the object is not in this 
            # cell, but rather in one of the other cells that are within
            # the visibility of the viewpoint

            pr_not_cell_given_obs_n1 = (1 -self.probability_matrix[x][y])*self.confusion[1][0]*((total_num_cells-1)/total_num_cells)
            pr_not_cell_given_obs_n0 = (1 -self.probability_matrix[x][y])*self.confusion[1][1]*((total_num_cells-1)/total_num_cells)
            pr_cell_given_obs_n1 = (self.probability_matrix[x][y]*self.confusion[0][0])*(1/total_num_cells)
            pr_cell_given_obs_n0 = (self.probability_matrix[x][y]*self.confusion[0][1])*(1/total_num_cells)
            
            if(obs == 1):
                prob = pr_cell_given_obs_n1 / (pr_cell_given_obs_n1 + pr_not_cell_given_obs_n1)
            else:
                prob = pr_cell_given_obs_n0 / (pr_cell_given_obs_n0 + pr_not_cell_given_obs_n0)
       
            self.probability_matrix[x][y] = prob

        return 

    def sort(self, sub_li):
        l = len(sub_li)
        for i in range(0, l):
            for j in range(0, l-i-1):
                if (sub_li[j][1] < sub_li[j + 1][1]):
                    tempo = sub_li[j]
                    sub_li[j]= sub_li[j + 1]
                    sub_li[j + 1]= tempo
        return sub_li

    def get_best_viewpoints(self, candidate_viewpoints):
        cand_view_probs = [] 

        #print(f'total num cands = {len(candidate_viewpoints)}')

        for i in range(len(candidate_viewpoints)):
            candidate = candidate_viewpoints[i]

            # calculate the probability that we detect the object from this vantage point
            total = 0

            cells_in_viewpoint = self.get_cells_in_viewpoint(candidate, 800, 480)

            for cell in cells_in_viewpoint:
                total += self.probability_matrix[cell[0]][cell[1]]
            
            cand_view_probs.append([i,total ])

        sorted_cands = self.sort(cand_view_probs)

        best_five = sorted_cands[0:5]

        #print(f'the best 5 are {best_five}')

        return best_five

            
