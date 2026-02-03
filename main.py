import pygame
import math
import random

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("my game")

planet_center = (WIDTH//2, HEIGHT//2)
planet_radius = 300

mars_img = pygame.image.load("assets/planet/mars.png").convert_alpha()
mars_img = pygame.transform.smoothscale(mars_img, (planet_radius * 2, planet_radius * 2))

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

player_x = planet_center[0]
player_y = planet_center[1] - 250
player_radius = 8
player_speed = 4
player_angle = 0
player_max_health = 100
player_health = player_max_health
player_alive = True
game_over = False
player_fire_rate = 20
player_fire_cooldown = 0
player_flash = 0

base_radius = 38

aliens=[]
alien_speed = 1.5
alien_radius = 12
alien_spawn_delay = 120
spawn_time = 0

alien_laser_shot = pygame.mixer.Sound("sounds/laser_weapon_shot.wav")
player_laser_shot = pygame.mixer.Sound("sounds/player_laser_gun.wav")
game_over_sound = pygame.mixer.Sound("sounds/game_over_sound.wav")
alien_die_sound = pygame.mixer.Sound("sounds/alien_dieing_sound.wav")

alien_laser_shot.set_volume(0.1)
player_laser_shot.set_volume(0.2)
game_over_sound.set_volume(0.7)
alien_die_sound.set_volume(0.15)

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
alien_bullet_speed = 15
alien_shoot_delay = 90
alien_bullet_damage = 10

shake_intensity = 0
shake_duration = 0

base_img = pygame.image.load("assets/base/base.png").convert_alpha()
base_img = pygame.transform.smoothscale(base_img, (base_radius * 2, base_radius * 2))

def make_circle_surface(image, radius):
    size = radius * 2
    circle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    pygame.draw.circle(circle_surface, (255, 255, 255, 255), (radius, radius), radius)

    circle_surface.blit(image, (0, 0), special_flags = pygame.BLEND_RGB_MULT)

    return circle_surface

def draw_player(surface, x, y, angle):
    size = 16
    tip = (x + math.cos(angle) * size, y + math.sin(angle) * size)
    left = (x + math.cos(angle + 2.5) * size, y + math.sin(angle + 2.5) * size)
    right = (x + math.cos(angle - 2.5) * size, y + math.sin(angle - 2.5) * size)
    pygame.draw.polygon(surface, blue, [tip, left, right])

def draw_player_health(surface, health, max_health):
    bar_width = 200
    bar_height = 12
    x=20
    y=20

    health_ratio = health/max_health

    pygame.draw.rect(surface, (60,60,60), (x, y, bar_width, bar_height))

    pygame.draw.rect(surface, (50,200,50), (x, y, bar_width * health_ratio, bar_height))

    pygame.draw.rect(surface, (255,255,255), (x, y, bar_width, bar_height), 2)

def reset_game():
    global player_x, player_y, player_health, player_alive
    global bullets, alien_bullets, aliens
    global game_over, spawn_time

    player_x = planet_center[0]
    player_y = planet_center[1] - 249
    player_health = player_max_health
    player_alive = True

    aliens.clear()
    bullets.clear()
    alien_bullets.clear()

    spawn_time = 0
    game_over = False

mars_img = make_circle_surface(mars_img, planet_radius)
base_img = make_circle_surface(base_img, base_radius)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reset_game()
    
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

            player_laser_shot.play()
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
            "health" : 30,
            "flash" : 0
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

            alien_laser_shot.play()

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
                alien["flash"] = 4
                bullets.remove(bullet)

                if alien["health"] <= 0:
                    aliens.remove(alien)
                    alien_die_sound.play()
                    shake_intensity = 3
                    shake_duration = 5
                break
    

    for bullet in alien_bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

        if math.hypot(bullet[0] - planet_center[0], bullet[1] - planet_center[1]) > planet_radius:
            alien_bullets.remove(bullet)
            continue

        hit_mountain = False
        for mx, my, mr in mountains:
            if math.hypot(bullet[0] - mx, bullet[1] - my) < mr:
                alien_bullets.remove(bullet)
                hit_mountain = True
                break
        if hit_mountain:
            continue

        if math.hypot(bullet[0] - player_x, bullet[1] - player_y) < player_radius:
            player_health -= alien_bullet_damage
            player_flash = 6
            alien_bullets.remove(bullet)

            if player_health <= 0 and not game_over:
                player_health = 0
                player_alive = False
                game_over = True
                game_over_sound.play()
                shake_intensity = 8
                shake_duration = 10
            break
    if player_flash > 0:
        player_flash -= 1

    shake_x = shake_y = 0
    if shake_duration > 0:
        shake_x = random.randint(-shake_intensity, shake_intensity)
        shake_y = random.randint(-shake_intensity, shake_intensity)
        shake_duration -= 1
    
    offset_surface = pygame.Surface((WIDTH, HEIGHT))
    offset_surface.fill(black)

    mars_rect = mars_img.get_rect(center = planet_center)
    offset_surface.blit(mars_img, mars_rect)

    base_rect = base_img.get_rect(center = planet_center)
    offset_surface.blit(base_img, base_rect)

    draw_player(offset_surface, player_x, player_y, player_angle)
    if player_flash > 0:
        flash_x = player_x + math.cos(player_angle) * player_radius
        flash_y = player_y + math.sin(player_angle) * player_radius

        pygame.draw.circle(
            offset_surface,
            red,
            (int(flash_x), int(flash_y)),
            6
        )
    draw_player_health(offset_surface, player_health, player_max_health)

    for alien in aliens:
        pygame.draw.circle(offset_surface, red, (int(alien["x"]), int(alien["y"])), alien_radius)

        bar_width = 20
        bar_height =4
        health_ratio = alien["health"]/30

        pygame.draw.rect(offset_surface,
                         magenta,
                         (
                            alien["x"] - bar_width//2,
                            alien["y"] - alien_radius - 5,
                            bar_width * health_ratio,
                            bar_height
                            )
                        )
        

                                           
    for mx, my, mr in mountains:
        pygame.draw.circle(offset_surface, brown, (mx, my), mr)
    for bullet in alien_bullets:
        pygame.draw.circle(offset_surface, yellow_2, (int(bullet[0]), int(bullet[1])), alien_bullet_radius)
    for bullet in bullets:
        pygame.draw.circle(
            offset_surface, yellow, (int(bullet[0]), int(bullet[1])), bullet_radius
        )
        
    if not player_alive:
        font = pygame.font.SysFont(None, 64)
        text = font.render("YOU DIED", True, (255,80,80))
        rect = text.get_rect(center = (WIDTH//2, HEIGHT//2))
        offset_surface.blit(text, rect)

        small_font = pygame.font.SysFont(None, 32)
        game_over_text = small_font.render('Click "space" to restart', True, black)
        rect_2 = game_over_text.get_rect(center = (WIDTH//2, HEIGHT//2 + 26))
        offset_surface.blit(game_over_text, rect_2)
    screen.blit(offset_surface, (shake_x, shake_y))

    pygame.display.flip()
pygame.quit()