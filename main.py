import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("my game")

black = (0,0,0)
green = (50,180,50)
blue = (80,120,255)
red = (200,60,60)
yellow = (255,220,100)
gray = (120,120,120)

clock = pygame.time.Clock()
FPS = 60

planet_center = (WIDTH//2, HEIGHT//2)
planet_radius = 300

player_x = planet_center[0]
player_y = planet_center[1]
player_radius = 8
player_speed = 4
player_angle = 0

base_radius = 36

bullets = []
bullet_speed = 8
bullet_radius = 3

def draw_player(surface, x, y, angle):
    size = 16
    tip = (x + math.cos(angle) * size, y + math.sin(angle) * size)
    left = (x + math.cos(angle + 2.5) * size, y + math.sin(angle + 2.5) * size)
    right = (x + math.cos(angle - 2.5) * size, y + math.sin(angle - 2.5) * size)
    pygame.draw.polygon(surface, red, [tip, left, right])

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullets.append([
                    player_x,
                    player_y,
                    math.cos(player_angle) * bullet_speed,
                    math.sin(player_angle) * bullet_speed
                ])
    
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
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_angle = math.atan2(
        mouse_y - player_y,
        mouse_x - player_x
    )

    for bullet in bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    screen.fill(black)
    pygame.draw.circle(screen, green, planet_center, planet_radius)
    pygame.draw.circle(screen, gray, planet_center, base_radius)
    draw_player(screen, player_x, player_y, player_angle)
    for bullet in bullets:
        pygame.draw.circle(
            screen, yellow, (int(bullet[0]), int(bullet[1])), bullet_radius
        )
    pygame.display.flip()
pygame.quit()