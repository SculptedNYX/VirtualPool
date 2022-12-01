import pygame
import pymunk
import pymunk.pygame_util as pmg

#Game Meta Data
DIM_WIDTH = 1200
DIM_HEIGHT = 678
WINDOW_TITLE = "Virtual Pool"
gameOn = True
BALL_MASS = 5
BALL_ELASTICITY = 0.8
CUSHION_ELASTICITY = 0.8

dia = 36

#Initilize the modules
pygame.init()

#Setting up the window
screen = pygame.display.set_mode((DIM_WIDTH,DIM_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

#Setting up the space for pymunk
space = pymunk.Space()
static_body = space.static_body
drawOptions = pmg.DrawOptions(screen)  # to draw on the screen


#clock
clock = pygame.time.Clock()
fps = 120

#colors
bg = (50,50,50)

#load images ps.you need to load the image of the table
#for the table
table_image = pygame.image.load().convert_alpha()

# for the balls
ballImages =[]
for i in range (1,17):
    ballImage = pygame.image.load().convert_alpha()
    ballImages.append(ballImage)

#Create the body and shape of the ball
def createBall(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = BALL_MASS
    shape.elasticity = BALL_ELASTICITY
    #use pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body,(0,0),(0,0))
    pivot.max_bias= 0 #disable joint correction
    pivot.max_force= 1000 #emulate linear friction

    #edit created pivot added to apply friction
    space.add(body, shape, pivot)
    return shape

#setup game balls
balls = []
rows = 5
#potting balls
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * (dia + 1)), 267 + (row  * (dia + 1)) + (col * dia/2))
        new_ball = createBall(dia/2 , pos)
        balls.append(new_ball)
        rows -= 1

#cue "white" ball created
pos = (888 , DIM_HEIGHT/2)
cueBall = createBall(dia / 2, pos)
balls.append(cueBall)

#create pool table cushions
cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
  [(621, 56), (630, 77), (1081, 77), (1102, 56)],
  [(89, 621), (110, 600),(556, 600), (564, 621)],
  [(622, 621), (630, 600), (1081, 600), (1102, 621)],
  [(56, 96), (77, 117), (77, 560), (56, 581)],
  [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]
#function for creating cushions 
#"the walls to stop the balls from moving out of the border"

def crC(poly_dims):
    body = pymunk.Body(body_type = pymunk.Body.STATICS) 
    body.position = ((0,0))
    shape = pymunk.Poly(body,poly_dims)
    shape.elasticity = CUSHION_ELASTICITY

    space.add(body, shape)

for c in cushions:
    crC(c)
#Game loop
while gameOn:

    clock.tick(fps)
    space.step(1/fps)

    #fill background
    screen.fill(bg)

    #draw pool table
    screen.blit(table_image,(0,0))

    #draw pool balls
    for i, ball in enumerate (balls):
        screen.blit(ballImages[i], (ball.body.position[0] - ball.radius , ball.body.position[1]) - ball.radius)

    #Note: for handling
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cueBall.body.apply_impulse_at_local_point((-1500,0),(0,0))
        if event.type == pygame.QUIT:
            gameOn = False
    
    # Display the objects
    space.debug_draw(drawOptions)
    pygame.display.update()

pygame.quit()