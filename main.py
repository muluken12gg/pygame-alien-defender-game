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
sky_blue = (135, 206, 235)
orange = (255, 165, 0)
purple = (128, 0, 128)
lava_red = (207, 16, 32)
brown = (139, 69, 19)
pink = (255, 105, 180)
yellow_2 = (255, 255, 0)
cyan = (0, 255,255)
magenta = (255, 0, 255)

clock = pygame.time.Clock()
FPS = 60

planet_center = (WIDTH//2, HEIGHT//2)
planet_radius = 300

player_x = planet_center[0]
player_y = planet_center[1]
player_radius = 8
player_speed = 4
player_angle = 0
player_max_health = 100
player_health = player_max_health
player_alive = True
player_fire_rate = 10
player_fire_cooldown = 0

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
player_bullet_damage = 10

alien_bullets = []
alien_bullet_radius = 4
alien_bullet_speed = 6
alien_shoot_delay = 90
alien_bullet_damage = 10

def draw_player(surface, x, y, angle):
    size = 16
    tip = (x + math.cos(angle) * size, y + math.sin(angle) * size)
    left = (x + math.cos(angle + 2.5) * size, y + math.sin(angle + 2.5) * size)
    right = (x + math.cos(angle - 2.5) * size, y + math.sin(angle - 2.5) * size)
    pygame.draw.polygon(surface, red, [tip, left, right])

def draw_player_health(surface, health, max_health):
    bar_width = 200
    bar_height = 12
    x=20
    y=20

    health_ratio = health/max_health

    pygame.draw.rect(surface, (60,60,60), (x, y, bar_width, bar_height))

    pygame.draw.rect(surface, (50,200,50), (x, y, bar_width * health_ratio, bar_height))

    pygame.draw.rect(surface, (255,255,255), (x, y, bar_width, bar_height), 2)

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

    if player_alive:
        if distance_to_center <=  planet_radius :
            player_x = new_x
            player_y = new_y
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if player_alive:
        player_angle = math.atan2(
            mouse_y - player_y,
            mouse_x - player_x
        )

    mouse_buttons = pygame.mouse.get_pressed()

    if player_fire_cooldown > 0:
        player_fire_cooldown -= 1

    if player_alive and mouse_buttons[0]:
        if player_fire_cooldown <= 0:
            bullets.append([
                player_x,
                player_y,
                math.cos(player_angle) * bullet_speed,
                math.sin(player_angle) * bullet_speed
            ])
            player_fire_cooldown = player_fire_rate

    spawn_time += 1
    if spawn_time >= alien_spawn_delay:
        spawn_time = 0
        angle = random.uniform(0, 2 * math.pi)
        ax = planet_center[0] + math.cos(angle) * planet_radius
        ay = planet_center[1] + math.sin(angle) * planet_radius
        aliens.append({
            "x" : ax,
            "y" : ay,
            "cooldown" : random.randint(30, alien_shoot_delay),
            "health" : 30
        })

    for alien in aliens:
        dx = planet_center[0] - alien["x"]
        dy = planet_center[1] - alien["y"]
        length = math.hypot(dx, dy)
        if length != 0:
            alien["x"] += dx/length * alien_speed
            alien["y"] += dy/length * alien_speed

        alien["cooldown"] -= 1
        if alien["cooldown"] <= 0:
            alien["cooldown"] = alien_shoot_delay

            shoot_dx = player_x - alien["x"]
            shoot_dy = player_y - alien["y"]
            shoot_len = math.hypot(shoot_dx, shoot_dy)

            if shoot_len != 0:
                vx = shoot_dx/shoot_len * alien_bullet_speed
                vy = shoot_dy/shoot_len * alien_bullet_speed

            alien_bullets.append([
                alien["x"],
                alien["y"],
                vx,
                vy
            ])

    for bullet in bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

        if math.hypot(bullet[0] - planet_center[0], bullet[1] - planet_center[1]) > planet_radius:
            bullets.remove(bullet)
            continue

        bullet_destroyed = False
        for mx, my, mr in mountains:
            if math.hypot(bullet[0] - mx, bullet[1] - my) < mr:
                bullets.remove(bullet)
                bullet_destroyed = True
                break
        
        if bullet_destroyed:
            continue
        
        for alien in aliens[:]:
            if math.hypot(bullet[0] - alien["x"], bullet[1] - alien["y"]) < alien_radius:
                alien["health"] -= player_bullet_damage
                bullets.remove(bullet)

                if alien["health"] <= 0:
                    aliens.remove(alien)
                break

    for bullet in alien_bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

        if math.hypot(bullet[0] - planet_center[0], bullet[1] - planet_center[1]) > planet_radius:
            alien_bullets.remove(bullet)
            continue

        for mx, my, mr in mountains:
            if math.hypot(bullet[0] - mx, bullet[1] - my) < mr:
                alien_bullets.remove(bullet)
                break

        if math.hypot(bullet[0] - player_x, bullet[1] - player_y) < player_radius:
            player_health -= alien_bullet_damage
            alien_bullets.remove(bullet)

            if player_health <= 0:
                player_health = 0
                player_alive = False
            break

    screen.fill(black)
    pygame.draw.circle(screen, green, planet_center, planet_radius)
    pygame.draw.circle(screen, gray, planet_center, base_radius)
    draw_player(screen, player_x, player_y, player_angle)
    draw_player_health(screen, player_health, player_max_health)

    for alien in aliens:
        pygame.draw.circle(screen, red, (int(alien["x"]), int(alien["y"])), alien_radius)

        bar_width = 20
        bar_height =4
        health_ratio = alien["health"]/30

        pygame.draw.rect(screen,
                         magenta,
                         (
                            alien["x"] - bar_width//2,
                            alien["y"] - alien_radius - 5,
                            bar_width * health_ratio,
                            bar_height
                            )
                        )
                                           
    for mx, my, mr in mountains:
        pygame.draw.circle(screen, brown, (mx, my), mr)
    for bullet in alien_bullets:
        pygame.draw.circle(screen, pink, (int(bullet[0]), int(bullet[1])), alien_bullet_radius)
    for bullet in bullets:
        pygame.draw.circle(
            screen, yellow, (int(bullet[0]), int(bullet[1])), bullet_radius
        )

    if not player_alive:
        font = pygame.font.SysFont(None, 64)
        text = font.render("YOU DIED", True, (255,80,80))
        rect = text.get_rect(center = (WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)

    pygame.display.flip()
pygame.quit()