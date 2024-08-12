import pygame
image_pass = '/data/data/com.alex.nagebator/files/app/'
clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Nagebator")
icon = pygame.image.load(image_pass+'images/nagebator_icon.png').convert_alpha()
pygame.display.set_icon(icon)
bg = pygame.image.load(image_pass+'images/background.jpg').convert_alpha()
walk_left = [
     pygame.image.load(image_pass+'images/left spr/l1.png').convert_alpha(),
     pygame.image.load(image_pass+'images/left spr/l2.png').convert_alpha(),
     pygame.image.load(image_pass+'images/left spr/l3.png').convert_alpha(),
     pygame.image.load(image_pass+'images/left spr/l4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load(image_pass+'images/right spr/r 1.png').convert_alpha(),
    pygame.image.load(image_pass+'images/right spr/r2.png').convert_alpha(),
    pygame.image.load(image_pass+'images/right spr/r3 2.0.png').convert_alpha(),
    pygame.image.load(image_pass+'images/right spr/r4.png').convert_alpha(),
]
ghost = pygame.image.load(image_pass+'images/monster (1).png').convert_alpha()

player_anim_count = 0
bg_x = 0
player_speed = 10
player_x = 120
player_y = 400

is_jump = False
jump_count = 15
ghost_list = []

bg_sound = pygame.mixer.Sound(image_pass+'sound/bgsound.mp3')
bg_sound.play()
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 1000)
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer,4000)
label = pygame.font.Font('images/font/Roboto-Black.ttf', 40)
lose_label = label.render('Game over!', False, (193, 197, 199))
restart_label = label.render('Restart!', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(550, 500))
bullets_left = 10
bullet = pygame.image.load(image_pass+"images/pants_3515820 (1).png").convert_alpha()
bullets = []
gameplay = True
running = True
while running:
    clock.tick(0)

    screen.blit(bg,(bg_x, 0))
    screen.blit(bg,(bg_x+1280, 0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))
        if ghost_list:
            for (i, el) in enumerate( ghost_list):
                screen.blit(ghost, el)
                el.x -= 10
                if el.x < -10:
                    ghost_list.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x,player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        if keys[pygame.K_LEFT] and player_x> 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x<1000:
            player_x += player_speed
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -15:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 15

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1
            bg_x -= 2
        if bg_x == -1280:
            bg_x =0

        if bullets:
            for (i,el) in enumerate( bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 1200:
                    bullets.pop(i)
                if ghost_list:
                    for (index, ghost_el) in enumerate(ghost_list):
                        if el.colliderect(ghost_el):
                            ghost_list.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label,(500,300))
        screen.blit(restart_label, restart_label_rect)
        mouse= pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 120
            ghost_list.clear()
            bullets.clear()
            bullets_left = 10
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(1250,  460)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_a and  bullets_left> 0:

            bullets.append(bullet.get_rect(topleft=(player_x+250, player_y+120)))
            bullets_left -=1
    clock.tick(20)
