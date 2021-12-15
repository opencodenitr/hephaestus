import pygame
from pygame import mixer
import random
import main
import os
import sys

sys.path.append(os.getcwd())

from structs import sprites
from structs import elements

def game():
    run = True
    FPS = 60
    wave, lives = 0, 5
    score = elements.Score()
    if score.score != 0:
        score.score = 0
    main_font = pygame.font.Font(r"Star Wars Lite\fonts\Starjedi.ttf", 30)
    deaths_font = pygame.font.Font(r"Star Wars Lite\fonts\Starjedi.ttf", 30)

    enemies = []
    wave_length = 5
    enemy_velocity, player_velocity = 1, 4
    laser_velocity = 6

    player = elements.Player(300, 630)

    clock = pygame.time.Clock()

    deaths = False
    deaths_count = 0

    def redraw():
        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 0))
        wave_label = main_font.render(f"wave: {wave}", 1, (255, 255, 0))
        score_label = main_font.render(f"Score: {score.score}", 1, (255, 255, 0))
        
        sprites.WINDOW.blit(lives_label, (10, 10))
        sprites.WINDOW.blit(
            wave_label, (sprites.WIDTH - wave_label.get_width() - 10, 10)
        )
        sprites.WINDOW.blit(score_label, (290, 10))

        for enemy in enemies:
            enemy.draw(sprites.WINDOW)

        player.draw(sprites.WINDOW)

        if deaths:
            mixer.music.fadeout(750)
            deaths_label = deaths_font.render(
                "The Imperial Fleet has defeated you!!", 1, (255, 255, 255)
            )
            sprites.WINDOW.blit(
                deaths_label, (sprites.WIDTH / 2 - deaths_label.get_width() / 2, 350)
            )
            

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw()

        if lives <= 0 or player.health <= 0:
            deaths = True
            deaths_count += 1
            score.update_high_scores()


        if deaths:
            if deaths_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            if wave != 0:
                score.wave_score_update()
            wave += 1
            wave_length += 5
            for _ in range(wave_length):
                enemy = elements.Enemy(
                    random.randrange(50, sprites.WIDTH - 100),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"]),
                )
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.posx - player_velocity > 0:  # left
            player.posx -= player_velocity
        if (
            keys[pygame.K_d]
            and player.posx + player_velocity + player.get_width() < sprites.WIDTH
        ):  # right
            player.posx += player_velocity
        if keys[pygame.K_w] and player.posy - player_velocity > 0:  # up
            player.posy -= player_velocity
        if (
            keys[pygame.K_s]
            and player.posy + player_velocity + player.get_height() + 15
            < sprites.HEIGHT
        ):  # down
            player.posy += player_velocity
        if keys[pygame.K_SPACE]:
            player_laser_sound = mixer.Sound(r"Star Wars Lite/sounds/player_laser.wav")
            player_laser_sound.play()
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            main.game_menu()

        collision_sound = mixer.Sound(r"Star Wars Lite/sounds/explosion.wav")

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.fire_lasers(laser_velocity, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if elements.object_collision(enemy, player):
                player.health -= 5
                collision_sound.play()
                enemies.remove(enemy)
            elif enemy.posy + enemy.get_height() > sprites.HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.fire_lasers(-laser_velocity, enemies, score)


def options():
    title_font = pygame.font.Font(r"Star Wars Lite/fonts/Starjedi.ttf", 60)
    menu_font = pygame.font.Font(r"Star Wars Lite/fonts/Starjedi.ttf", 40)
    run = True

    while run:
        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        # draw text on a new surface, 'text', antialias, color, background
        title_text = title_font.render("options", 1, (255, 255, 0))

        menu_text = menu_font.render("toggle sound", 1, (255, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        sprites.WINDOW.blit(title_text, (sprites.WIDTH / 2 - title_text.get_width() / 2, 30))

        sound_on_btn = elements.button('Star Wars Lite/assets\menu\sound-on-active.png', 'Star Wars Lite/assets\menu\sound-on-inactive.png', 250, "soundon")
        sound_off_btn = elements.button('Star Wars Lite/assets\menu\sound-off-active.png', 'Star Wars Lite/assets\menu\sound-off-inactive.png', 310,"soundoff")
        back_btn = elements.button(r'Star Wars Lite/assets\menu\back-active.png', r'Star Wars Lite/assets\menu\back-inactive.png', 485,"back")

        pygame.display.update()
        pygame.time.Clock().tick(60)

    pygame.quit()


def high_score():
    print("not working")
    title_font = pygame.font.Font(r"Star Wars Lite/fonts/Starjedi.ttf", 60)
    menu_font = pygame.font.Font(r"Star Wars Lite/fonts/Starjedi.ttf", 40)
    run = True

    while run:
        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        # draw text on a new surface, 'text', antialias, color, background
        title_text = title_font.render("options", 1, (255, 255, 0))

        menu_text = menu_font.render("toggle sound", 1, (255, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        sprites.WINDOW.blit(title_text, (sprites.WIDTH / 2 - title_text.get_width() / 2, 30))

        sound_on_btn = elements.button('Star Wars Lite/assets\menu\sound-on-active.png', 'Star Wars Lite/assets\menu\sound-on-inactive.png', 250, "soundon")
        sound_off_btn = elements.button('Star Wars Lite/assets\menu\sound-off-active.png', 'Star Wars Lite/assets\menu\sound-off-inactive.png', 310,"soundoff")
        back_btn = elements.button(r'Star Wars Lite/assets\menu\back-active.png', r'Star Wars Lite/assets\menu\back-inactive.png', 485,"back")

        pygame.display.update()
        pygame.time.Clock().tick(60)

    pygame.quit()
