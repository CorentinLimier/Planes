import pygame


pygame.init()

display_width = 800
display_height = 400

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Planes')
clock = pygame.time.Clock()

planeImg = pygame.image.load('plane.png')

def plane(x,y):
    gameDisplay.blit(planeImg, (x,y))

x = (display_width * 0.45)
y = (display_height * 0.8)

crashed = False
y_change = 0

while not crashed:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                y_change = -5
            elif event.key == pygame.K_RIGHT:
                y_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                y_change = 0


    y += y_change

    gameDisplay.fill(white) # fill background with white
    plane(x,y) # display plane
    pygame.display.update() # update the screen
    clock.tick(60) #frames per seconds

pygame.quit()
quit()
