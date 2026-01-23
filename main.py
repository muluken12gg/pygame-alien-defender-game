import pygame
import math
import random

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

aliens=[]
alien_speed = 1.5
alien_radius = 12
alien_spawn_delay = 120
spawn_time = 0

mountains = [
    (planet_center[0]-200, planet_center[1]+40 , 35),
    (planet_center[0]+120, planet_center[1]-20, 40),
    (planet_center[0]+190, planet_center[1]+80, 50)
]

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

        if math.hypot(bullet[0] - planet_center[0], bullet[1] - planet_center[1]) > planet_radius:
            bullets.remove(bullet)
            continue

        for mx, my, mr in mountains:
            if math.hypot(bullet[0] - mx, bullet[1] - my) < mr:
                bullets.remove(bullet)
                break

    spawn_time += 1
    if spawn_time >= alien_spawn_delay:
        spawn_time = 0
        angle = random.uniform(0, 2 * math.pi)
        ax = planet_center[0] + math.cos(angle) * planet_radius
        ay = planet_center[1] + math.sin(angle) * planet_radius
        aliens.append([ax, ay])

    for alien in aliens:
        dx = planet_center[0] - alien[0]
        dy = planet_center[1] - alien[1]
        length = math.hypot(dx, dy)
        if length != 0:
            alien[0] += dx/length * alien_speed
            alien[1] += dy/length * alien_speed

    screen.fill(black)
    pygame.draw.circle(screen, green, planet_center, planet_radius)
    pygame.draw.circle(screen, gray, planet_center, base_radius)
    draw_player(screen, player_x, player_y, player_angle)

    for alien in aliens:
        pygame.draw.circle(screen, red, (int(alien[0]), int(alien[1])), alien_radius)

    for mx, my, mr in mountains:
        pygame.draw.circle(screen, gray, (mx, my), mr)
    for bullet in bullets:
        pygame.draw.circle(
            screen, yellow, (int(bullet[0]), int(bullet[1])), bullet_radius
        )
    pygame.display.flip()
pygame.quit()