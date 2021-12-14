import pygame, sys
from pygame import mixer
import os
import main
from structs import root


sys.path.append(os.getcwd())
from structs import sprites


class Shuttle:
    REST_TIME = 30

    def __init__(self, posx, posy, health=100):
        self.shuttle_image = None
        self.laser_image = None
        self.lasers = []
        self.rest_timer = 0
        self.posx = posx
        self.posy = posy
        self.health = health

    def draw(self, window):
        window.blit(self.shuttle_image, (self.posx, self.posy))
        for laser in self.lasers:
            laser.draw(window)

    def fire_lasers(self, velocity, obj):
        self.rest_time()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.screen_bound(sprites.HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def rest_time(self):
        if self.rest_timer >= self.REST_TIME:
            self.rest_timer = 0
        elif self.rest_timer > 0:
            self.rest_timer += 1

    def shoot(self):
        if self.rest_timer == 0:
            laser = Laser(self.posx, self.posy, self.laser_image)
            self.lasers.append(laser)
            self.rest_timer = 1

    def get_width(self):
        return self.shuttle_image.get_width()

    def get_height(self):
        return self.shuttle_image.get_height()


class Laser:
    def __init__(self, posx, posy, image):
        self.posx = posx
        self.posy = posy
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.posx, self.posy))

    def move(self, velocity):
        self.posy += velocity

    def screen_bound(self, height):
        return not (self.posy <= height and self.posy >= 0)

    def collision(self, obj):
        return object_collision(self, obj)


class Player(Shuttle):
    def __init__(self, posx, posy, health=100):
        super().__init__(posx, posy, health)
        self.shuttle_image = sprites.PLAYER
        self.laser_image = sprites.LASER_YELLOW
        self.mask = pygame.mask.from_surface(self.shuttle_image)
        self.max_health = health

    def fire_lasers(self, velocity, objs, score):
        self.rest_time()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.screen_bound(sprites.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        collision_sound = mixer.Sound(r"Star Wars Lite/sounds/explosion.wav")
                        collision_sound.play()
                        objs.remove(obj)
                        score.update()
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.posx,
                self.posy + self.shuttle_image.get_height() + 10,
                self.shuttle_image.get_width(),
                10,
            ),
        )
        pygame.draw.rect(
            window,
            (255, 255, 0),
            (
                self.posx,
                self.posy + self.shuttle_image.get_height() + 10,
                self.shuttle_image.get_width() * (self.health / self.max_health),
                10,
            ),
        )


class Enemy(Shuttle):
    # using rgbs as placeholders
    COLOR_PLACEHOLDER = {
        "red": (sprites.ENEMY0, sprites.LASER_RED),
        "green": (sprites.ENEMY1, sprites.LASER_GREEN),
        "blue": (sprites.ENEMY3, sprites.LASER_BLUE),
    }

    def __init__(self, posx, posy, color, health=100):
        super().__init__(posx, posy, health)
        self.shuttle_image, self.laser_image = self.COLOR_PLACEHOLDER[color]
        self.mask = pygame.mask.from_surface(self.shuttle_image)

    def move(self, velocity):
        self.posy += velocity

    def shoot(self):
        if self.rest_timer == 0:
            laser = Laser(self.posx - 20, self.posy, self.laser_image)
            self.lasers.append(laser)
            self.rest_timer = 1

class Score():
    def __init__(self):
        self.score = 0
        self.high_scores = [int(line.rstrip("\n")) for line in open("Star Wars Lite/leaderboard.txt")]

    def update(self): #Ten points per ship destroyed 
        self.score += 10

    def wave_score_update(self): #One hundred points per wave cleared
        self.score += 100

    def top_3_high_score(self): #Still needs to be added
        return self.high_scores.sort(reverse=True)

    def update_high_scores(self): #Still needs to be added
        self.high_scores.sort()
        if self.score > self.high_scores[0]:
            del self.high_scores[0]
            self.high_scores.append(self.score)
        with open("leaderboard.txt", "w") as leaderboard:
            leaderboard.writelines("%s\n" % high_score for high_score in self.high_scores)
        return self.high_scores

def object_collision(obj1, obj2):
    offset_x = obj2.posx - obj1.posx
    offset_y = obj2.posy - obj1.posy
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def button(active,inactive,get_top,action=None):
    
    click = pygame.mouse.get_pressed()
    music_paused = False

    mx, my = pygame.mouse.get_pos()
    display = pygame.image.load(inactive).convert_alpha()
    display_rect = display.get_rect(center=sprites.WINDOW.get_rect().center, top=get_top)

    if display_rect.collidepoint((mx, my)):
        display = pygame.image.load(active).convert_alpha()
        if click[0] == 1 and action != None:
            if action == 'play':
                root.game()
            elif action == 'options':
                root.options()
            elif action == 'exit':
                pygame.quit()
                quit()
            elif action == 'back':
                main.game_menu()
            elif action == 'soundon':
                if mixer.music.play(-1) == False:
                    mixer.music.play(-1)
            elif action == 'soundoff':
                if not music_paused:
                    pygame.mixer.music.pause()
                    music_paused = True
                else:
                    pygame.mixer.music.unpause()
    else:
        display = pygame.image.load(inactive).convert_alpha()

    sprites.WINDOW.blit(display, display_rect)