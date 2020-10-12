import pygame, sys
from pygame import mixer
import os
import time
import random
import warnings
from structs import elements, root, sprites

warnings.filterwarnings("ignore")

pygame.font.init()
pygame.init()
mixer.init()
pygame.display.set_caption("Star Wars Lite")

mainClock = pygame.time.Clock()



def main():
    title_font = pygame.font.Font(r"fonts\Starjedi.ttf", 40)
    run = True
    while run:
        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        title_text = title_font.render("Click LMB to start $", 1, (255, 255, 0))
        sprites.WINDOW.blit(
            title_text, (sprites.WIDTH / 2 - title_text.get_width() / 2, 350)
        )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                root.main()

    pygame.quit()
click = False


def game_menu():
    title_font = pygame.font.Font(r"fonts\Starjedi.ttf", 40)
    menu_font = pygame.font.Font(r"fonts\Starjedi.ttf", 40)
    run = True

    play_button = pygame.image.load('assets\menu\play.png').convert()
    play_button_rect = play_button.get_rect(center = sprites.WINDOW.get_rect().center, top=325)

    while run:

        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        # draw text on a new surface, 'text', antialias, color, background
        title_text = title_font.render("Star Wars Lite", 1, (255, 255, 0))
        play_text = menu_font.render("play_image", 1, (255, 255, 0))
        options_text = menu_font.render("Play", 1, (255, 255, 0))
        quit_text = menu_font.render("Play", 1, (255, 255, 0))


        mx, my = pygame.mouse.get_pos()

        if play_button_rect.collidepoint((mx,my)):
            if click:
                root.main()


        sprites.WINDOW.blit(title_text, (sprites.WIDTH / 2 - title_text.get_width() / 2, 30))
        sprites.WINDOW.blit(play_button, play_button_rect)
        pygame.display.update()

        # quits on escape
        click = False
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

        pygame.display.update()
        mainClock.tick(60)

if __name__ == "__main__":
    game_menu()
    