import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("my game")

black = (0,0,0)
green = (50,180,50)
blue = (80,120,255)

clock = pygame.time.Clock()
FPS = 60

planet_center = (WIDTH//2, HEIGHT//2)
planet_radius = 300

player_x = planet_center[0]
player_y = planet_center[1]
player_radius = 8
player_speed = 4

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    
    keys= pygame.key.get_pressed()
    dx = dy = 0

    if keys[pygame.K_w]:
        dy-=1
    if keys[pygame.K_d]:
        dx+=1
    if keys[pygame.K_s]:
        dy+=1
    if keys[pygame.K_a]:
        dx-=1

    if dx != 0 or dy != 0:
        length = math.hypot(dx, dy)
        dx = dx/length*player_speed
        dy = dy/length*player_speed

    new_x = dx + player_x
    new_y = dy + player_y

    distance_to_center = math.hypot(
        new_x - planet_center[0],
        new_y - planet_center[1]
    )

    if distance_to_center <=  planet_radius :
        player_x = new_x
        player_y = new_y

    screen.fill(black)
    pygame.draw.circle(screen, green, planet_center, planet_radius)
    pygame.draw.circle(screen, blue, (int(player_x), int(player_y)), player_radius)
    pygame.display.flip()
pygame.quit()