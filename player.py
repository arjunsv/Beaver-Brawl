import pygame
import math
import constants

from threading import Timer
from constants import BLACK
from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    direction = "R"
    level = None

    def __init__(self, health, player):
        pygame.sprite.Sprite.__init__(self)
        self.heart_img = pygame.image.load("heart.png").convert_alpha()
        self.image = pygame.image.load("beaver.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70,70))
        self.image_original = self.image
        self.image_flipped = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.health = health
        self.attack = Stick
        self.last_shot = 0
        self.last_portal = 0
        self.last_spec = 0
        self.lives = 3
        self.is_knocked_back = False
        self.knockback_ticks = 15
        self.can_portal = False
        self.portal_up = False

    def update(self):
        self.calc_grav()

        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "L":
            self.image = self.image_flipped
        else:
            self.image = self.image_original

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .75

        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -15

    def go_left(self):
        self.change_x = -8
        self.direction = "L"

    def go_right(self):
        self.change_x = 8
        self.direction = "R"

    def stop(self):
        self.change_x = 0

    def update_health(self, screen, color):
        pygame.draw.rect(screen, color, (self.rect.x - 15, self.rect.y - 20, self.health, 5), 4)

    def update_heart(self, screen, player):
        offset = 0
        heart = pygame.transform.scale(self.heart_img, (40, 40))
        if player == 2:
            start = 40
            for i in range(self.lives):
                screen.blit(heart, (40 + offset, 40))
                offset += 55
        if player == 1:
            for i in range(self.lives):
                screen.blit(heart, (constants.SCREEN_WIDTH - 80 + offset, 40))
                offset -= 55

    def update_portal(self, screen, player):
        offset = 0
        if self.portal_up:
            portal = pygame.transform.scale(pygame.image.load("portal0.png").convert_alpha(), (40, 40))
        else:
            portal = pygame.transform.scale(pygame.image.load("portal_gray.png").convert_alpha(), (40, 40))

        if player == 2:
            start = 40
            screen.blit(portal, (40 + offset, 90))
            offset += 55
        if player == 1:
            screen.blit(portal, (constants.SCREEN_WIDTH - 80 + offset, 90))
            offset -= 55

class Projectile(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
 
        self.image = pygame.Surface([10, 4])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
        self.direction = direction
 
    def update(self):
        self.rect.x += 25 * self.direction

        #check if we are outside the screen
        if self.rect.x > constants.SCREEN_WIDTH or self.rect.x < 0:
            self.kill()

        if self.rect.y > constants.SCREEN_HEIGHT or self.rect.y < 0:
            self.kill()

class Stick(Projectile):
    def __init__(self, direction):
        super().__init__(direction)
        self.index = 0
        self.image = pygame.transform.scale(pygame.image.load("stick.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.height = self.rect.height*0.3
        self.rect.width = self.rect.width*0.5
        self.rect.y += self.rect.height
        self.rect.x += self.rect.width

    def update(self):

        self.rect.x += 15 * self.direction

        if self.rect.x > constants.SCREEN_WIDTH or self.rect.x < 0:
            self.kill()

        if self.rect.y > constants.SCREEN_HEIGHT or self.rect.y < 0:
            self.kill()

class MegaStick(Projectile):
    def __init__(self, direction):
        super().__init__(direction)
        self.index = 0
        self.image = pygame.transform.scale(pygame.image.load("log.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect()
        self.rect.y += self.rect.height + 300
        self.rect.x += self.rect.width

    def update(self):
        self.rect.y += 12

        if self.rect.x > constants.SCREEN_WIDTH or self.rect.x < 0:
            self.kill()

        if self.rect.y > constants.SCREEN_HEIGHT or self.rect.y < 0:
            self.kill()

class Shuriken(Projectile):
    image_list = []
    for i in range(3):
        scaled_image = pygame.transform.scale(pygame.image.load("shuriken" + str(i) + ".png"), (75, 75)) 
        image_list.append(scaled_image)
    def __init__(self, direction, player):
        super().__init__(direction)
        self.index = 0
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.player = player
        self.target_x = player.rect.x + 500*direction
        self.reached_target = False

    def update(self):
        if abs(self.rect.x - self.target_x) < 10:
            self.reached_target = True
        if self.reached_target:
            self.rect.x += 15*self.direction*-1
        else:
            if self.target_x > self.rect.x:
                self.rect.x += 15
            else:
                self.rect.x -= 15
        self.index += 1
        if self.index >= len(self.image_list):
            self.index = 0
        if self.direction == 1:
            self.image = self.image_list[self.index]
        else:
            self.image = pygame.transform.flip(self.image_list[self.index],True ,False)

class Item(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 50))
        self.rect = self.image.get_rect()

class Portal(pygame.sprite.Sprite):
    image_list = []
    wide_image_list = []
    for i in range(8):
        scaled_image = pygame.transform.scale(pygame.image.load("portal" + str(i) + ".png"), (100, 200)) 
        image_list.append(scaled_image)
    for i in range(8):
        scaled_image = pygame.transform.scale(pygame.image.load("portal" + str(i) + ".png"), (200, 100)) 
        wide_image_list.append(scaled_image)
    def __init__(self, player, other_player, direction, is_start, duration=5):
        super().__init__()
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        if not is_start:
            self.rect = pygame.Rect((0,0), (0,0))
            self.image_list = self.wide_image_list
        self.active = True
        self.direction = direction
        self.index = 0
        self.player = player
        if is_start:
            if player.direction == "R":
                self.rect.x = player.rect.x + 100
            else:
                self.rect.x = player.rect.x - 150
            self.rect.y = player.rect.y - 50
        else:
            self.rect.x = other_player.rect.x - 60
            self.rect.y = other_player.rect.y - 300

        Timer(3, self.reset).start()

    def reset(self):
        self.active = False        
    def update(self):
        if self.active:
            if self.index >= len(self.image_list):
                self.index = 0
            if self.direction == 1:
                self.image = self.image_list[self.index]
            else:
                self.image = pygame.transform.flip(self.image_list[self.index],True ,False)
            self.index += 1