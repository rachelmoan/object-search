import environment
import pygame
import math

#######################################
################ Main #################
#######################################
if __name__ == "__main__": 

    env = environment.Environment(display_environment=True, 
                 screen_height =480, 
                 fov=math.pi / 3, 
                 casted_rays=120, 
                 map_length=8, 
                 map_height=8,
                 player_angle=math.pi
                 )


    last = pygame.time.get_ticks()
    cooldown = 300  

    forward = True

    prob_map = env.get_prob_map()

    while True:
        for event in pygame.event.get():
            now = pygame.time.get_ticks()
            if now - last >= cooldown:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                col = int(env.player_x / env.tile_size) # get the number of columns
                row = int(env.player_y / env.tile_size) # get the number of rows

                pygame.draw.rect(env.win,(0,0,0),(0,0,env.screen_height,env.screen_height))
                
                pygame.draw.rect(env.win,(100,0,0),(600,env.screen_height / 2,env.screen_height,env.screen_height))
                pygame.draw.rect(env.win,(200,0,0),(600,-env.screen_height / 2,env.screen_height,env.screen_height))      
                
                
                env.draw_map()
                env.draw_prob_map(prob_map)
                #env.cast_rays()
                keys = pygame.key.get_pressed()

                if env.obstacle_map[row][col]:
                    if forward == True:
                        env.player_x -= -math.sin(env.player_angle) * env.tile_size
                        env.player_y -= math.cos(env.player_angle) * env.tile_size
                    else:
                        env.player_x += -math.sin(env.player_angle) * env.tile_size
                        env.player_y += math.cos(env.player_angle) * env.tile_size

                else:
                    if keys[pygame.K_LEFT]: 
                        env.player_angle -= (1/2)*math.pi
                    if keys[pygame.K_RIGHT]: 
                        env.player_angle += (1/2)*math.pi
                    if keys[pygame.K_UP]:
                        forward = True
                        env.player_x += -math.sin(env.player_angle) * env.tile_size
                        env.player_y += math.cos(env.player_angle) * env.tile_size
                    if keys[pygame.K_DOWN]:
                        forward = False
                        env.player_x -= -math.sin(env.player_angle) * env.tile_size
                        env.player_y -= math.cos(env.player_angle) * env.tile_size
                

                # For each movement, make an observation and update the map
                prob_map = env.update_map([env.player_x, env.player_y, env.player_angle])
            
        env.clock.tick(60)    
        
        fps = str(int(env.clock.get_fps()))
        font = pygame.font.SysFont('Monospace Regular', 30)
        textsurface = font.render(fps, False, (255,255,255))
        env.win.blit(textsurface,(0,0))
        pygame.display.flip()
        