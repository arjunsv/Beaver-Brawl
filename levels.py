import pygame

import constants
import platforms
import time

class Level():

    platform_list = None
    enemy_list = None

    background = None

    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.prompt_index = 0
        self.time = time.time()
        self.prompts = [
            "  North American Beavers primarily consume grasses, mushrooms, leaves, and roots!",
            "Beavers build fortified lodges out of mud and branches with underwater entrances.",
            "                              A beaver can stay under water for up to 15 minutes.",
            "                                     Beavers can live up to 24 years in the wild!",
            "                         Beavers are nocturnal animals and like to work at night.",
            "                        Beavers are the second largest rodent after the Capybara.",
            "   Beavers are second to humans in their ability to manipulate their environment.",
            "                                    The largest beaver dam is 850 meters long.   ",
            "      Beavers are a 'Keystone Species' because of their effects on other species.",
            "A hat craze in Europe in 15th-18th centuries created high demand for beaver fur. ",
            "Human factors such as hunting and deforestation have reduced the beaver population.",
            "                                     The Beaver is the national animal of Canada."
        ]

    def update(self):

        self.platform_list.update()
        self.enemy_list.update()

        curr_time = time.time()
        if curr_time - self.time > 10:
            self.time = curr_time
            self.prompt_index += 1

    def update_text(self, screen):
        
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(self.prompts[self.prompt_index % len(self.prompts)], False, (0, 0, 0))
        screen.blit(textsurface,(200,190))

    def draw(self, screen):

        screen.fill(constants.BLUE)
        screen.blit(self.background,(self.world_shift // 3,0))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


class Level_01(Level):

    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.transform.scale(pygame.image.load("images/river.png"),(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert_alpha()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        level = [
                  [platforms.GRASS_LEFT, 800, 680],
                  [platforms.GRASS_MIDDLE, 850, 680],
                  [platforms.GRASS_RIGHT, 900, 680],


                  [platforms.GRASS_LEFT, 470, 580],
                  [platforms.GRASS_MIDDLE, 520, 580],
                  [platforms.GRASS_MIDDLE, 570, 580],
                  [platforms.GRASS_MIDDLE, 620, 580],
                  [platforms.GRASS_RIGHT, 670, 580],


                  [platforms.GRASS_LEFT, 250, 680],
                  [platforms.GRASS_MIDDLE, 300, 680],
                  [platforms.GRASS_RIGHT, 350, 680],

                  [platforms.GRASS_LEFT, 20, 420],
                  [platforms.GRASS_MIDDLE, 70, 420],


                  [platforms.GRASS_LEFT, 100, 550],
                  [platforms.GRASS_MIDDLE, 150, 550],
                  [platforms.GRASS_RIGHT, 200, 550],

                  [platforms.GRASS_LEFT, 600, 250],
                  [platforms.GRASS_MIDDLE, 650, 250],
                  [platforms.GRASS_RIGHT, 700, 250],

                  [platforms.GRASS_LEFT, 700, 100],
                  [platforms.GRASS_MIDDLE, 750, 100],
                  [platforms.GRASS_RIGHT, 800, 100],
                  [platforms.GRASS_MIDDLE, 850, 100],
                  [platforms.GRASS_MIDDLE, 900, 100],
                  [platforms.GRASS_RIGHT, 950, 100],


                  [platforms.GRASS_LEFT, 1120, 300],
                  [platforms.GRASS_MIDDLE, 1170, 300],
                  [platforms.GRASS_RIGHT, 1220, 300],


                  [platforms.GRASS_LEFT, 900, 450],
                  [platforms.GRASS_MIDDLE, 950, 450],
                  [platforms.GRASS_RIGHT, 1000, 450]
                  ]

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.GRASS_MIDDLE)
        block.rect.x = 300
        block.rect.y = 280
        block.boundary_left = 100
        block.boundary_right = 400
        block.change_x = 2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block2 = platforms.MovingPlatform(platforms.GRASS_MIDDLE)
        block2.rect.x = 1050
        block2.rect.y = 250
        block2.boundary_top = 100
        block2.boundary_bottom = 400
        block2.change_y = 2
        block2.player = self.player
        block2.level = self
        self.platform_list.add(block2)