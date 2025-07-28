from configuration import *
import sys
import pygame
from Sprites import *
from items import *
from world_gen import world_output, load_tilemap_from_csv

class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()


    def get_image(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.spritesheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)

        return sprite



class Game:

    tilemap = []

    def __init__(self):
        self.screen = pygame.display.set_mode((windowWidth, windowHeight))
        self.clock = pygame.time.Clock()
        self.running = True
        self.gen_north = False
        self.gen_west = False
        self.gen_south = False
        self.gen_east = False
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group() 
        self.bullets = pygame.sprite.Group() 
        self.mainPlayer = pygame.sprite.Group()
        self.healthbar = pygame.sprite.Group()
        self.terrain_spritesheet = Spritesheet('GameAssets/images/terrain.png')    
        self.player_spritesheet = Spritesheet('GameAssets/images/green.png')
        self.enemy_spritesheet = Spritesheet('GameAssets/images/evil.png')
        self.weapon_spritesheet = Spritesheet('GameAssets/images/sword.png')
        self.bullet_spritesheet = Spritesheet('GameAssets/images/fireball/FB500-1.png')
        self.enemy_bullet_spritesheet = Spritesheet('GameAssets/images/powerball.png')
        self.collided = False
        self.enemy_collided = False
        self.block_collided = False
        self.camera_bounds = [0,0,windowWidth,windowHeight]
        self.create_chunk(0, 0)
       
        # Add camera
        self.camera = camera(len(self.tilemap[0]) * TILE_SIZE, len(self.tilemap) * TILE_SIZE)
        

    
    def create_tilemap(self, tilemap, x, y):
        print(x,y)
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j+x,i+y)
                if column == 'B':
                    Block(self,j+x,i+y)
                if column == 'P':
                    self.player = Player(self,j+x,i+y)
                if column == 'E':
                    self.enemy = Enemy(self,j+x,i+y)
                if column == 'R':
                    Water(self,j+x,i+y)
                if column == 'W':
                    Weapon(j+x,i+y,self)

    def create_chunk(self, x, y):
        world_output()
        self.tilemap = load_tilemap_from_csv("map.csv")
        self.create_tilemap(self.tilemap, x, y)
        


        

    def create(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.mainPlayer = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.healthbar = pygame.sprite.LayeredUpdates()
        self.create_tilemap(self.tilemap, 0, 0)

    def update(self):
        for sprite in self.all_sprites:
            if type(sprite) != Ground:
                sprite.update()
        self.bullets.update()
        print(len(self.all_sprites))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite)) 
        self.clock.tick(FPS)
        pygame.display.update()

    """
    def camera(self):
         if not pygame.sprite.spritecollide(self.player, self.blocks, False) and \
        not pygame.sprite.spritecollide(self.player, self.water, False) and \
        not pygame.sprite.spritecollide(self.player, self.enemies, False):
            pressed = pygame.key.get_pressed()
    
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                for i, sprit in enumerate(self.all_sprites):
                    sprit.rect.x += PLAYER_SPEED
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                for i, sprit in enumerate(self.all_sprites):
                    sprit.rect.x -= PLAYER_SPEED
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                for i, sprit in enumerate(self.all_sprites):
                    sprit.rect.y += PLAYER_SPEED
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                for i, sprit in enumerate(self.all_sprites):
                    sprit.rect.y -= PLAYER_SPEED
                    """

    def main(self):
        self.events()
        self.update()
        if hasattr(self, 'player'):
            self.camera.update(self.player)
        self.draw()

class camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Center the camera on the player
        print(target.rect.x, target.rect.y)
        old_x = -target.rect.x + (windowWidth // 2)
        old_y = -target.rect.y + (windowHeight // 2)

        # Keep the camera within bounds
        x = min(game.camera_bounds[0], old_x)  # Left boundary
        y = min(game.camera_bounds[1], old_y)  # Top boundary

        if y != old_y and game.gen_north == False:
            game.create_chunk(0,-chunkHeight)
            game.camera_bounds[1] += self.height
            print(game.camera_bounds)
            game.gen_north = True

        if x != old_x and game.gen_west == False:
            game.create_chunk(-chunkWidth,0)
            game.camera_bounds[0] += self.width
            print(game.camera_bounds)
            game.gen_west = True

        

        x = max(-(self.width - windowWidth), x)  # Right boundary
        y = max(-(self.height - windowHeight), y)  # Bottom boundary

        self.camera = pygame.Rect(x, y, self.width, self.height)    
        print(x,y)
        print(old_x,old_y)
        print()



    



game = Game()
game.create()

while game.running:
    game.main()

pygame.quit()
sys.exit()
    