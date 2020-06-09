import pygame
import pytmx
import sys
import random
from os import path
from v4_config import *
from v4_sprites import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #cria uma screen com o tamanho pedido
        pygame.display.set_caption ('Teste Tiled Map') #muda o título da screen
        self.clock = pygame.time.Clock() #salva na variável o Clock
        pygame.key.set_repeat(500,100) # Inicia a função de repetir (tempo de espera, tempo para repetir cada ação)
        self.load_data()
        

    def load_data(self):
        # cria mapa       
        self.map = TiledMap((path.join(MAP_DIR, 'mapa1.tmx')))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # --- Cobra ---
        # Esquerda
        self.snake_left = {}
        for img in WALK_LEFT:
            self.snake_left[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_left[img] =  pygame.transform.scale(self.snake_left[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
        # Direita
        self.snake_right = {}
        for img in WALK_RIGHT:
            self.snake_right[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_right[img] =  pygame.transform.scale(self.snake_right[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
        # Cima
        self.snake_up = {}
        for img in WALK_UP:
            self.snake_up[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_up[img] =  pygame.transform.scale(self.snake_up[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
        # Baixo
        self.snake_down = {}
        for img in WALK_DOWN:
            self.snake_down[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_down[img] =  pygame.transform.scale(self.snake_down[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
        
        # --- Frutas ---
        self.fruit_images = []
        for fruta in LISTA_FRUTAS:
            self.fruit_images.append((pygame.image.load(path.join(IMG_DIR, 'fruits', fruta)).convert_alpha()))

        # --- Pássaro ---
        self.bird_img = pygame.image.load(path.join(IMG_DIR, BIRD_IMG)).convert_alpha()

        # --- Veneno da cobra ---
        self.veneno_img = pygame.image.load(path.join(IMG_DIR, VENENO_IMG)).convert_alpha()
    
    def new(self):   
        #cria os grupos:
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.birds = pygame.sprite.Group ()
        self.veneno = pygame.sprite.Group()
        # Spawna as barreiras
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Snake(self, self.snake_right['R1.png'], tile_object.x, tile_object.y)
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height) 
            if tile_object.name == 'fruit':
                Fruit (self, random.choice(self.fruit_images), tile_object.x, tile_object.y)
            if tile_object.name == 'Passaro':
                Bird (self, tile_object.x, tile_object.y)             
        # cria câmera
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # Player colide com a frutas:
        hits = pygame.sprite.spritecollide (self.player, self.fruits, False)
        for hit in hits:
            # coloca alguma função (aumentar stamina, ex.)
            hit.kill()
        
    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites: #Analisa cada um dos sprites do grupo e mandar imprimir
            # -- Pássaro --
            if isinstance (sprite, Bird):
                sprite.draw_life_bar()
            # -- Fruta --
            if isinstance (sprite, Fruit): # se for relacionado a classe Fruit
                quad_dist_to_player = (self.player.pos.x - sprite.pos.x)**2 + (self.player.pos.y - sprite.pos.y)**2
                if quad_dist_to_player <= PLAYER_VISION**2: #spawna a fruta somente se ela estiver dentro do alcance da visão
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()



jogo = Game()
while True:
    jogo.new()
    jogo.run()

