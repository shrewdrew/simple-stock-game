import pygame
import brownian_bridge
import stock_game_player_state as PSM
import numpy as np
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
bridge_length=10001
bridge=brownian_bridge.brownian_bridge(bridge_length,1)
yscale=200.
xscale=7
xlength=int(size[0]/xscale)

ycoords=np.ones(xlength)*size[1]/2
xcoords=np.linspace(0,size[0],xlength)

xfade=int(xlength*0.8)
state=PSM.state()
font = pygame.font.SysFont('Calibri', 25, True, False)
history_point=int(3/4*size[0])
bridge_counter=bridge_buy_offset=0
buy_point=-1

#calculate display/buy offset
for i, val in enumerate(xcoords):
    if val > history_point:
        bridge_counter=bridge_buy_offset=i
        break
        

def draw_buysell(state, bridge, bridge_counter, screen):
    if state.get_state()==1:
        #left, top, width, height
        rect=(
        0, 
        -1*max(state.get_buy_price(),bridge.Y[bridge_counter-xlength +bridge_buy_offset])*yscale+size[1]/2,
        xcoords[bridge_buy_offset],
        abs(bridge.Y[bridge_counter-xlength +bridge_buy_offset]-state.get_buy_price())*yscale
        )
        pygame.draw.rect(screen, GREEN if state.get_buy_price()<bridge.Y[bridge_counter-xlength +bridge_buy_offset] else RED, (rect))

def draw_score(screen, state):
    pygame.draw.line(screen, BLACK, [0, size[1]*6/7], [size[0]/2, size[1]*6/7], 5)
    pygame.draw.line(screen, BLACK, [size[0]/2, size[1]*6/7], [size[0]/2, size[1]], 5)
    text = font.render("Score:\t{:1.6f}".format(state.get_score()), True, BLACK)
    screen.blit(text, [25, size[1]-50])

def draw_BB_and_update(screen, ycoords, xcoords, bridge, bridge_counter, done):
    ycoords[-1]=-1*bridge.Y[bridge_counter]*yscale+size[1]/2
    bridge_counter+=1

    if bridge_counter==bridge_length:
        done = True
 
    factor=-9999
    for i in range(xlength-1):
        if xcoords[i]>history_point:
            factor=(size[0]-xcoords[i])/(size[0]-history_point)
            colour=[min(int(BLACK[i]*(factor) + BLUE[i]*(1-factor)), 255) for i in range(len(BLUE))]
            colour.append(int(255*factor))
            pygame.draw.line(screen, colour,[xcoords[i], (factor)*ycoords[i]+(1-factor)*size[1]/2],[xcoords[i+1], (factor)*ycoords[i+1]+(1-factor)*size[1]/2],2)
        else:
            pygame.draw.line(screen, BLACK,[xcoords[i], ycoords[i]],[xcoords[i+1], ycoords[i+1]],2)
    
    ycoords=np.roll(ycoords,-1)
    return done, ycoords, bridge_counter

def convert_bb_to_ycoord(value):
    return -1*value*yscale+size[1]/2


# -------- Main Program Loop -----------
while not done:
    screen.fill(WHITE)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        if state.get_state()==0:
            state.buy(bridge.Y[bridge_counter-xlength +bridge_buy_offset])
            buy_point=bridge_buy_offset+1
        if buy_point>0:
            buy_point-=1
        pygame.draw.circle(screen, BLUE, [xcoords[buy_point], -1*state.get_buy_price()*yscale+size[1]/2], 10, 2)

    else:
        if state.get_state()==1:
            state.sell(bridge.Y[bridge_counter-xlength +bridge_buy_offset])
 

    draw_buysell(state, bridge, bridge_counter, screen)
    done, ycoords, bridge_counter = draw_BB_and_update(screen, ycoords, xcoords, bridge, bridge_counter, done)
    draw_score(screen, state)

    #draw line to indicate buy point
    pygame.draw.line(screen, BLACK,[xcoords[bridge_buy_offset], 0],[xcoords[bridge_buy_offset], size[1]],2)

    pygame.display.flip()
    clock.tick(20)
 
pygame.quit()