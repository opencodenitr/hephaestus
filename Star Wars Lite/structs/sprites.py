import pygame

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# images of enemy ships
ENEMY0 = pygame.image.load(r"Star Wars Lite/assets\enemy1.png")
ENEMY1 = pygame.image.load(r"Star Wars Lite/assets\enemy2.png")
ENEMY3 = pygame.image.load(r"Star Wars Lite/assets\enemy3.png")

# image of player ship
PLAYER = pygame.image.load(r"Star Wars Lite\assets\promlf.png")

# images of laser shots
LASER_RED = pygame.image.load(r"Star Wars Lite\assets\laser_red.png")
LASER_GREEN = pygame.image.load(r"Star Wars Lite\assets\laser_green.png")
LASER_BLUE = pygame.image.load(r"Star Wars Lite\assets\laser_blue.png")
LASER_YELLOW = pygame.image.load(r"Star Wars Lite\assets\laser_yellow.png")

# image of background
BACKGROUND = pygame.transform.scale(
    pygame.image.load(r"Star Wars Lite\assets\game_background.jpg"), (WIDTH, HEIGHT)
)
