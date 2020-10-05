import pygame
import random
import os
import sys

sys.path.append(os.getcwd())

from structs import sprites
from structs import elements


def main():
    run = True
    FPS = 60
    wave, lives = 0, 5
    main_font = pygame.font.Font(r"fonts\Starjedi.ttf", 30)
    deaths_font = pygame.font.Font(r"fonts\Starjedi.ttf", 30)

    enemies = []
    wave_length = 5
    enemy_velocity, player_velocity = 2, 5
    laser_velocity = 8

    player = elements.Player(300, 630)

    clock = pygame.time.Clock()

    deaths = False
    deaths_count = 0

    def redraw():
        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 0))
        wave_label = main_font.render(f"wave: {wave}", 1, (255, 255, 0))

        sprites.WINDOW.blit(lives_label, (10, 10))
        sprites.WINDOW.blit(
            wave_label, (sprites.WIDTH - wave_label.get_width() - 10, 10)
        )

        for enemy in enemies:
            enemy.draw(sprites.WINDOW)

        player.draw(sprites.WINDOW)

        if deaths:
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

        if deaths:
            if deaths_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
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
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            main()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.fire_lasers(laser_velocity, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if elements.object_collision(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.posy + enemy.get_height() > sprites.HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.fire_lasers(-laser_velocity, enemies)