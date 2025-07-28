import pygame
from configuration import *
from Sprites import *
import math

class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.game=game
        self._layer = WEAPON_LAYER
        self.groups = self.game.all_sprites, self.game.weapons
        super().__init__(self.groups)

        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.weapon_spritesheet.get_image(447, 353, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.animationCounter = 1
    
    def animate(self):
        
        animation =[self.game.weapon_spritesheet.get_image(0,0, self.width, self.height), 
                    self.game.weapon_spritesheet.get_image(32,0, self.width, self.height), 
                    self.game.weapon_spritesheet.get_image(64,0, self.width, self.height)]
        
        self.image = animation[math.floor(self.animationCounter)]
        self.animationCounter += 0.1
        if self.animationCounter >= 3:
            self.animationCounter = 0

    def update(self):
        self.animate()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.game=game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.bullets
        super().__init__(self.groups)

        self.x = x
        self.y = y

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.bullet_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = self.game.player.direction

        self.damage = 1
        self.timer = 0

    def move(self):
        if self.direction == 'up':
            self.rect.y -= BULLET_SPEED
        if self.direction == 'down':
            self.rect.y += BULLET_SPEED
        if self.direction == 'left':
            self.rect.x -= BULLET_SPEED
        if self.direction == 'right':
            self.rect.x += BULLET_SPEED

    def collide_blocks(self):
        collide = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if collide:    
            self.kill()

    def collide_enemy(self):
        collide = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if collide:
            collide[0].damage(self.damage)
            self.kill()
        elif self.timer > 150:
            self.kill()
        else:
            self.timer += 1
        
        # collide = pygame.sprite.spritecollide(self, self.game.enemies, False)
        # if collide:    
        #     self.kill()

    def update(self):
        self.move()
        self.collide_blocks()
        self.collide_enemy()


class ENEMY_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.game=game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.bullets
        super().__init__(self.groups)

        self.x = x
        self.y = y

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.enemy_bullet_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = self.game.player.direction

        self.damage = 1
        self.timer = 0

    def move(self):
        if self.direction == 'up':
            self.rect.y -= BULLET_SPEED
        if self.direction == 'down':
            self.rect.y += BULLET_SPEED
        if self.direction == 'left':
            self.rect.x -= BULLET_SPEED
        if self.direction == 'right':
            self.rect.x += BULLET_SPEED

    def collide_blocks(self):
        collide = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if collide:    
            self.kill()

    def collide_player(self):
        collide = pygame.sprite.spritecollide(self, self.game.mainPlayer, False)
        if collide:
            collide[0].damage(self.damage)
            self.game.player.damage(self.damage)
            self.kill()
        elif self.timer > 150:
            self.kill()
        else:
            self.timer += 1
        # collide = pygame.sprite.spritecollide(self, self.game.enemies, False)
        # if collide:    
        #     self.kill()

    def update(self):
        self.move()
        self.collide_blocks()
        self.collide_player()