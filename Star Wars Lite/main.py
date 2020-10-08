import pygame
from pygame import mixer
import os
import time
import random
import warnings
from structs import elements, root, sprites

warnings.filterwarnings("ignore")

pygame.font.init()
mixer.init()
pygame.display.set_caption("Star Wars Lite")


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
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                root.main()

    pygame.quit()


if __name__ == "__main__":
    main()