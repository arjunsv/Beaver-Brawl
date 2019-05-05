"""
Boilerplate code constructs from:
http://programarcadegames.com/python_examples/sprite_sheets/

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe
"""

import pygame

import constants
import levels
import time
import random

from player import Player, Portal, Shuriken, Item
from player import Projectile, Stick, MegaStick

def main():
    pygame.init()
    pygame.font.init() 

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("BeaverTale")

    player = Player(100, 1)
    player2 = Player(100, 2)
    player2.attack = Stick

    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_01(player2))
   
    current_level_no = 0
    current_level = level_list[current_level_no]

    items = pygame.sprite.Group()
    speed_items = pygame.sprite.Group()
    
    last_mushroom = time.time()
    last_speed = time.time()

    active_sprite_list = pygame.sprite.Group()
    player_projectiles = pygame.sprite.Group()
    player2_projectiles = pygame.sprite.Group()
    player_specs = pygame.sprite.Group()
    player2_specs = pygame.sprite.Group()
    player_portals = pygame.sprite.Group()
    player2_portals = pygame.sprite.Group()


    player.level = current_level
    player2.level = current_level

    player.rect.x = 1050
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    player2.rect.x = 100
    player2.rect.y = constants.SCREEN_HEIGHT - player2.rect.height
    active_sprite_list.add(player)
    active_sprite_list.add(player2)

    done = False

    clock = pygame.time.Clock()

    # Game Loop
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                done = True 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    if time.time() - player.last_shot > 1:
                        if player.direction == "L":
                            projectile = player.attack(-1)
                        else:
                            projectile = player.attack(1)
                        # Set the bullet so it is where the player is
                        projectile.rect.x = player.rect.x + 60
                        projectile.rect.y = player.rect.y + 30
                        if player.attack == Stick:
                            projectile.rect.x = player.rect.x
                            projectile.rect.y = player.rect.y - 10

                        # Add the bullet to the lists
                        player_projectiles.add(projectile)
                        player.last_shot = time.time()
                if event.key == pygame.K_RSHIFT:
                    player_specs
                    # if time.time() - player.last_spec > 0.1:
                    #     if player.direction == "L":
                    #         spec = Shuriken(-1, player)
                    #     else:
                    #         spec = Shuriken(1, player)

                    #     spec.rect.x = player.rect.x + 60
                    #     spec.rect.y = player.rect.y + 30
                    #     player_specs.add(spec)
                    #     player.last_spec = time.time()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            # Player 2 code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player2.go_left()
                if event.key == pygame.K_d:
                    player2.go_right()
                if event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_q:
                    if time.time() - player2.last_shot > 1:
                # Fire a bullet if the user clicks the mouse button
                        if player2.direction == "L":
                            projectile = player2.attack(-1)
                        else:
                            projectile = player2.attack(1)
                        # Set the bullet so it is where the player is
                        projectile.rect.x = player2.rect.x + 60
                        projectile.rect.y = player2.rect.y + 30

                        if player2.attack == Stick:
                            projectile.rect.x = player2.rect.x
                            projectile.rect.y = player2.rect.y - 10
                        elif player2.attack == MegaStick:
                            projectile.rect.x = player2.rect.x - 40
                            projectile.rect.y = player2.rect.y - 100

                        # Add the bullet to the lists
                        player2_projectiles.add(projectile)
                        player2.last_shot = time.time()

                # Portal
                elif event.key == pygame.K_e and player2.can_portal:
                    if player2.portal_up:
                        if player2.direction == 1:
                            start_portal = Portal(player2, player, 1, True, 5)
                            end_portal = Portal(player2, player, -1, False, 5)
                        else:
                            start_portal = Portal(player2, player, -1, True, 5)
                            end_portal = Portal(player2, player, 1, False, 5)
                        player2_portals.add(start_portal)
                        player2_portals.add(end_portal)
                        player2.last_portal = time.time()
                        player2.portal_up = False


                elif event.key == pygame.K_RSHIFT and player.can_portal:
                    if player.portal_up:
                        if player.direction == 1:
                            start_portal = Portal(player, player2, 1, True, 5)
                            end_portal = Portal(player, player2, -1, False, 5)
                        else:
                            start_portal = Portal(player, player2, -1, True, 5)
                            end_portal = Portal(player, player2, 1, False, 5)
                        player_portals.add(start_portal)
                        player_portals.add(end_portal)
                        player.last_portal = time.time()
                        player.portal_up = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player2.change_x < 0:
                    player2.stop()
                if event.key == pygame.K_d and player2.change_x > 0:
                    player2.stop()


        # Add block collisions

        if pygame.sprite.spritecollide(player, player2_projectiles, True):
                player.health -= 10

        if pygame.sprite.spritecollide(player, player2_projectiles, True):
                player.health -= 10


        if pygame.sprite.spritecollide(player, player2_projectiles, True):
            player.health -= 10

        if pygame.sprite.spritecollide(player2, player_projectiles, True):
            player2.health -= 10

        if pygame.sprite.spritecollide(player2, player_specs, True):
            player2.health -= 40

        if pygame.sprite.spritecollide(player, player2_specs, True):
            player.health -= 40

        if pygame.sprite.spritecollide(player2, player2_portals, False):
            player2.rect.x = end_portal.rect.x + 50
            player2.rect.y = end_portal.rect.y + 100

        if pygame.sprite.spritecollide(player, player_portals, False):
            player.rect.x = end_portal.rect.x + 50
            player.rect.y = end_portal.rect.y + 100

        if pygame.sprite.groupcollide(player2_projectiles, player2_portals, True, False):
            void_projectile = MegaStick(1)
            void_projectile.rect.x = end_portal.rect.x + 50
            void_projectile.rect.y = end_portal.rect.y + 50
            player2_specs.add(void_projectile)

        if pygame.sprite.groupcollide(player_projectiles, player_portals, True, False):
            void_projectile = MegaStick(1)
            void_projectile.rect.x = end_portal.rect.x + 50
            void_projectile.rect.y = end_portal.rect.y + 50
            player_specs.add(void_projectile)


        for portal in player_portals:
            if not portal.active:
                player_portals.remove(portal)

        for portal in player2_portals:
            if not portal.active:
                player2_portals.remove(portal)

        if pygame.sprite.spritecollide(player, items, True):
            player.can_portal = True
            player.portal_up = True
            last_mushroom = time.time()


        if pygame.sprite.spritecollide(player2, items, True):
            player2.can_portal = True
            player2.portal_up = True
            last_mushroom = time.time()


        if pygame.sprite.spritecollide(player, speed_items, True):
            player.speed_mul += 0.2
            last_speed = time.time()


        if pygame.sprite.spritecollide(player2, speed_items, True):
            player2.speed_mul += 0.2
            last_speed = time.time()

        # if time.time() - player2.last_portal > 15:
        #     player2.portal_up = True

        # if time.time() - player.last_portal > 15:
        #     player.portal_up = True

        if time.time() - last_mushroom > 15 and not items:
            mushroom = Item("images/mushroom.png")
            rand = random.randint(0,1)
            if rand == 0:
                mushroom.rect.x = 750
                mushroom.rect.y = 50
            if rand == 1:
                mushroom.rect.x = 520
                mushroom.rect.y = 530

            items.add(mushroom)

        if time.time() - last_speed > 30 and not speed_items:
            speed = Item("images/speed.png")
            rand = random.randint(0,1)
            if rand == 0:
                speed.rect.x = 950
                speed.rect.y = 400
            if rand == 1:
                speed.rect.x = 50
                speed.rect.y = 370

            speed_items.add(speed)

        if player.health < 0:
            player.health = 0
            player.lives -= 1
            player.health = 100
            player.rect.y = 600
            player.rect.x = 1000

        if player2.health < 0:
            player2.health = 0
            player2.lives -= 1
            player2.health = 100
            player2.rect.y = 50


        player_projectiles.update()
        player2_projectiles.update()
        player_specs.update()
        player2_specs.update()
        player_portals.update()
        player2_portals.update()
        active_sprite_list.update()


        current_level.update()


        current_level.draw(screen)
        player_portals.draw(screen)
        player2_portals.draw(screen)
        active_sprite_list.draw(screen)
        player_projectiles.draw(screen)
        player2_projectiles.draw(screen)
        player_specs.draw(screen)
        player2_specs.draw(screen)
        player.update_heart(screen, 1)
        player2.update_heart(screen, 2)

        if player.can_portal:
            player.update_portal(screen, 1)

        if player2.can_portal:
            player2.update_portal(screen, 2)


        items.draw(screen)
        speed_items.draw(screen)
        player.level.update_text(screen)

        if player.health >= 66:
            player.update_health(screen,(0, 255, 0))
        elif player.health >= 33:
            player.update_health(screen,(255, 255, 0))
        else:
            player.update_health(screen,(255, 0, 0))

        if player2.health >= 66:
            player2.update_health(screen,(0, 255, 0))
        elif player2.health >= 33:
            player2.update_health(screen,(255, 255, 0))
        else:
            player2.update_health(screen,(255, 0, 0))

        if player.lives <= 0:
            pygame.quit()

        if player2.lives <= 0:
            pygame.quit()

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
