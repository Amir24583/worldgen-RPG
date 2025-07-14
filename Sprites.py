from configuration import *
import pygame
import random
import math
from items import *





class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        #print(f"Game instance inside Block: {game}") 
        self.game=game
        if not hasattr(self.game, "blocks"):
            raise AttributeError("Game instance passed to Block has no 'blocks' attribute!")
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self._layer = BLOCKS_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        super().__init__(self.groups)

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_image(991, 541, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game=game
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_image(447, 353, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game=game
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self._layer = WATER_LAYER
        self.groups = self.game.all_sprites, self.game.water
        super().__init__(self.groups)

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_image(865, 160, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.animateCounter = 1

    def animation(self):
        animate = [self.game.terrain_spritesheet.get_image(864, 160, self.width, self.height), 
                   self.game.terrain_spritesheet.get_image(896,160, self.width, self.height), 
                   self.game.terrain_spritesheet.get_image(928, 160, self.width, self.height)]
        self.image = animate[math.floor(self.animateCounter)]
        self.animateCounter += 0.1
        if self.animateCounter >= 3:
            self.animateCounter = 0
    
    def update(self):
        self.animation()


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game=game
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self._layer = PLAYER_LAYER
        self.healthbar = player_healthbar(game, x, y)
        self.groups = self.game.all_sprites, self.game.mainPlayer  
        super().__init__(self.groups)
        self.x_change = 0
        self.y_change = 0


        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animationCounter = 0

        self.image = self.game.player_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = 'right'
        self.swordEquipped = False

        self.counter = 0
        self.waitTime = 10
        self.shootState = "shoot"

        self.health = PLAYER_HEALTH
        Particle(self.game, self.rect.x, self.rect.y)



    def movement(self):

        Particle(self.game, self.rect.x, self.rect.y)
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.x_change = self.x_change - PLAYER_SPEED
            self.direction = 'left'
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.x_change = self.x_change + PLAYER_SPEED
            self.direction = 'right'

        elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.y_change = self.y_change - PLAYER_SPEED
            self.direction = 'up'
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.y_change = self.y_change + PLAYER_SPEED
            self.direction = 'down'
    

    def animation(self):

        downAnimation = [self.game.player_spritesheet.get_image(0,0, self.width, self.height), 
                         self.game.player_spritesheet.get_image(32,0, self.width, self.height), 
                         self.game.player_spritesheet.get_image(64,0, self.width, self.height)]
        
        leftAnimation = [self.game.player_spritesheet.get_image(0,64, self.width, self.height), 
                         self.game.player_spritesheet.get_image(32,64, self.width, self.height), 
                         self.game.player_spritesheet.get_image(64,64, self.width, self.height)]
        
        rightAnimation = [self.game.player_spritesheet.get_image(0,96, self.width, self.height), 
                        self.game.player_spritesheet.get_image(32,96, self.width, self.height), 
                        self.game.player_spritesheet.get_image(64,96, self.width, self.height)]
        
        upAnimation = [self.game.player_spritesheet.get_image(0,32, self.width, self.height), 
                        self.game.player_spritesheet.get_image(32,32, self.width, self.height), 
                        self.game.player_spritesheet.get_image(64,32, self.width, self.height)]
        

        
        if self.direction == "down":
            if self.y_change == 0:
                self.image = self.game.player_spritesheet.get_image(0,0, self.width, self.height)
            else:
                self.image = downAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

        if self.direction == "up":
            if self.y_change == 0:
                self.image = self.game.player_spritesheet.get_image(0,32, self.width, self.height)
            else:
                self.image = upAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

        if self.direction == "left":
            if self.x_change == 0:
                self.image = self.game.player_spritesheet.get_image(32,64, self.width, self.height)
            else:
                self.image = leftAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

        if self.direction == "right":
            if self.x_change == 0:
                self.image = self.game.player_spritesheet.get_image(32,96, self.width, self.height)
            else:
                self.image = rightAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

    def collide_water(self):

        collideWater = pygame.sprite.spritecollide(self, self.game.water, False, pygame.sprite.collide_rect_ratio(0.5))

        if collideWater:
            self.game.collided = True
            if self.direction == 'left':
                self.rect.x += PLAYER_SPEED
            if self.direction == 'right':
                self.rect.x -= PLAYER_SPEED
            if self.direction== 'up':
                self.rect.y += PLAYER_SPEED
            if self.direction == 'down':    
                self.rect.y -= PLAYER_SPEED
        else:
            self.game.collided = False   

    def collide_block(self):

        
        collideBlock = pygame.sprite.spritecollide(self, self.game.blocks, False, pygame.sprite.collide_rect_ratio(0.8))


        if collideBlock:
            self.game.collided = True
            if self.direction == 'left':
                self.rect.x += PLAYER_SPEED
            if self.direction == 'right':
                self.rect.x -= PLAYER_SPEED
            if self.direction== 'up':
                self.rect.y += PLAYER_SPEED
            if self.direction == 'down':    
                self.rect.y -= PLAYER_SPEED
        else:
            self.game.collided = False    


    def collide_enemy(self):
        
        collide = pygame.sprite.spritecollide(self, self.game.enemies, False, pygame.sprite.collide_rect_ratio(0.8))

        if collide:
            self.game.collided = True
            if self.direction == 'left':
                self.rect.x += PLAYER_SPEED
            if self.direction == 'right':
                self.rect.x -= PLAYER_SPEED
            if self.direction== 'up':
                self.rect.y += PLAYER_SPEED
            if self.direction == 'down':    
                self.rect.y -= PLAYER_SPEED
        else:
            self.game.collided = False

    def collide_weapon(self):
        collide = pygame.sprite.spritecollide(self, self.game.weapons , True)

        if collide: 
            self.swordEquipped = True

    def shoot_sword(self):
        pressed = pygame.key.get_pressed()
        if self.shootState == "shoot":
            if self.swordEquipped:
                if pressed[pygame.K_SPACE]:
                    Bullet(self.rect.x, self.rect.y, self.game)
                    self.shootState = "wait"
                
    def waitAfterShoot(self):
        if self.shootState == "wait":
            self.counter += 1
            if self.counter >= self.waitTime:
                self.shootState = "shoot"
                self.counter = 0

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            self.game.running = False
            self.healthbar.kill_healthbar()
        else:
            self.healthbar.damage(self.health, PLAYER_HEALTH)


    def update(self):
        self.movement()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.collide_block()
        self.collide_water()    
        self.collide_enemy()
        self.collide_weapon()
        self.shoot_sword()
        self.waitAfterShoot()

        self.x_change = 0
        self.y_change = 0
    
                



class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game=game


        # Debugging statements to check for required attributes
        if not hasattr(self.game, 'all_sprites'):
            raise AttributeError("Game instance passed to Enemy has no 'all_sprites' attribute!")
        if not hasattr(self.game, 'enemies'):
            raise AttributeError("Game instance passed to Enemy has no 'enemies' attribute!")
        if not hasattr(self.game, 'enemy_spritesheet'):
            raise AttributeError("Game instance passed to Enemy has no 'enemy_spritesheet' attribute!")

        self._layer = PLAYER_LAYER
        self.healthbar = enemy_healthbar(game, self, x, y)
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x_change = 0
        self.y_change = 0

         

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animationCounter = 1


        self.image = self.game.enemy_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.numberSteps = random.choice([20, 40, 50, 60, 70, 80, 90])
        self.stallingSteps = 120
        self.currentSteps = 0

        self.state = "walk"

        self.health = ENEMY_HEALTH

        self.shootCounter = 0
        self.shootWaitTime = random.choice([5, 10, 20, 30, 40, 50, 60, 70, 80, 90])
        self.shootState = "halt"

    def shoot(self):
        self.shootCounter += 1
        if self.shootCounter == self.shootWaitTime:
            self.shootState = "shoot"
            self.shootCounter = 0

    
    def movement(self):

        if self.state == "walk":
            if self.direction == 'left':
                self.x_change = self.x_change - ENEMY_SPEED
                self.currentSteps += 1

                if self.shootState == "shoot":
                    ENEMY_Bullet(self.rect.x, self.rect.y, self.game)
                    self.shootState = "halt"

            elif self.direction == 'right':
                self.x_change = self.x_change + ENEMY_SPEED
                self.currentSteps += 1
                if self.shootState == "shoot":
                    ENEMY_Bullet(self.rect.x, self.rect.y, self.game)
                    self.shootState = "halt"

            elif self.direction == 'up':
                self.y_change = self.y_change - ENEMY_SPEED
                self.currentSteps += 1
                if self.shootState == "shoot":
                    ENEMY_Bullet(self.rect.x, self.rect.y, self.game)
                    self.shootState = "halt"

            elif self.direction == 'down':
                self.y_change = self.y_change + ENEMY_SPEED
                self.currentSteps += 1
                if self.shootState == "shoot":
                    ENEMY_Bullet(self.rect.x, self.rect.y, self.game)
                    self.shootState = "halt"


            # Boundary checks
            if self.rect.x + self.x_change < 0:
                self.rect.x = 0
                self.direction = random.choice(['right', 'up', 'down'])
            elif self.rect.x + self.x_change > self.game.screen.get_width() - self.width:
                self.rect.x = self.game.screen.get_width() - self.width
                self.direction = random.choice(['left', 'up', 'down'])
            if self.rect.y + self.y_change < 0:
                self.rect.y = 0
                self.direction = random.choice(['left', 'right', 'down'])
            elif self.rect.y + self.y_change > self.game.screen.get_height() - self.height:
                self.rect.y = self.game.screen.get_height() - self.height
                self.direction = random.choice(['left', 'right', 'up'])


        elif self.state == "idle":
            self.currentSteps += 1
            if self.currentSteps == self.stallingSteps:
                self.state = "walk"
                self.currentSteps = 0
                self.direction = random.choice(['left', 'right', 'up', 'down'])

            """self.rect.x = self.rect.x + self.x_change
            self.rect.y = self.rect.y + self.y_change

            self.x_change = 0
            self.y_change = 0"""
    
    
    def animation(self):

        downAnimation = [self.game.enemy_spritesheet.get_image(0,0, self.width, self.height), 
                         self.game.enemy_spritesheet.get_image(32,0, self.width, self.height), 
                         self.game.enemy_spritesheet.get_image(64,0, self.width, self.height)]
        
        leftAnimation = [self.game.enemy_spritesheet.get_image(0,32, self.width, self.height), 
                         self.game.enemy_spritesheet.get_image(32,32, self.width, self.height), 
                         self.game.enemy_spritesheet.get_image(64,32, self.width, self.height)]
        
        rightAnimation = [self.game.enemy_spritesheet.get_image(0,64, self.width, self.height), 
                        self.game.enemy_spritesheet.get_image(32,64, self.width, self.height), 
                        self.game.enemy_spritesheet.get_image(64,64, self.width, self.height)]
        
        upAnimation = [self.game.enemy_spritesheet.get_image(0,96, self.width, self.height), 
                        self.game.enemy_spritesheet.get_image(32,96, self.width, self.height), 
                        self.game.enemy_spritesheet.get_image(64,96, self.width, self.height)]
        

        
        if self.direction == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(0,0, self.width, self.height)
            else:
                self.image = downAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

        if self.direction == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(32,96, self.width, self.height)
            else:
                self.image = upAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

        if self.direction == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(32,32, self.width, self.height)
            else:
                self.image = leftAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

        if self.direction == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(32,64, self.width, self.height)
            else:
                self.image = rightAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 0

    
    def update(self):
        self.movement()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.x_change = 0
        self.y_change = 0
        if self.currentSteps == self.numberSteps:
            if self.state != 'idle':
                self.currentSteps = 0       
            self.numberSteps = random.choice([20, 40, 50, 60, 70, 80, 90])
            self.state = "idle"
        self.collide_block()
        self.collide_Player()
        self.shoot()


    def collide_block(self):

        collideBlock = pygame.sprite.spritecollide(self, self.game.blocks, False, pygame.sprite.collide_rect_ratio(0.8))
        collideWater = pygame.sprite.spritecollide(self, self.game.water, False, pygame.sprite.collide_rect_ratio(0.5))

        if collideBlock or collideWater:
            if self.direction == 'left':
                self.rect.x += ENEMY_SPEED
                self.direction = 'right'
            if self.direction == 'right':
                self.rect.x -= ENEMY_SPEED
                self.direction = 'left'
            if self.direction== 'up':
                self.rect.y += ENEMY_SPEED
                self.direction = 'down'
            if self.direction == 'down':    
                self.rect.y -= ENEMY_SPEED
                self.direction = 'up'
    
    def collide_Player(self):

        collide = pygame.sprite.spritecollide(self, self.game.mainPlayer, True)
        if collide:
            self.game.running = False

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            self.healthbar.kill_bar()
        else:
            self.healthbar.damage(self.health, ENEMY_HEALTH)


class player_healthbar(pygame.sprite.Sprite):
    def __init__(self, game,x ,y):
        self.game=game
        self._layer = HEALTH_LAYER
        self.groups = self.game.all_sprites, self.game.healthbar  
        super().__init__(self.groups)

        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE

        self.width = 40
        self.height = 10

        self.animationCounter = 0

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y-TILE_SIZE/2
    
    def move(self):
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y -TILE_SIZE/2

    def kill_healthbar(self):
        self.kill()

    def damage(self, health , totalHealth):
        self.image.fill(RED)
        width = self.rect.width * self.game.player.health/PLAYER_HEALTH
        pygame.draw.rect(self.image, GREEN, (0,0, width, self.height), 0)
    
    def update(self):
        self.move()



class enemy_healthbar(pygame.sprite.Sprite):
    def __init__(self, game, enemy,x ,y):
        self.enemy = enemy 
        self.game=game
        self._layer = HEALTH_LAYER
        self.groups = self.game.all_sprites, self.game.healthbar  
        super().__init__(self.groups)

        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE

        self.width = 40
        self.height = 10

        self.animationCounter = 0

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y-TILE_SIZE/2
    
    def move(self):
        self.rect.x = self.enemy.rect.x
        self.rect.y = self.enemy.rect.y -TILE_SIZE/2

    def damage(self, health , totalHealth):
        self.image.fill(RED)
        width = self.rect.width * health/totalHealth
        pygame.draw.rect(self.image, GREEN, (0,0, width, self.height), 0)

    def kill_bar(self):
        self.kill()

    def update(self):
        self.move()


class Particle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = HEALTH_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)


        self.width = 4
        self.height = 4

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(PARTICLE_COLOR)  # color for particles
        self.rect = self.image.get_rect()
        self.rect.x = x + random.choice([-4,-3,-1,0,1,5,10,20])
        self.rect.y = y + TILE_SIZE
       
        self.lifetime = 6
        self.counter = 0

    def move(self):
        self.rect.y += 1
        self.counter += 1
        if self.counter >= self.lifetime:
            self.counter = 0
            self.kill()

    def update(self):
        # Update logic for particles can be added here
        self.move()