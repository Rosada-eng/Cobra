import pygame
import pytmx
import sys
import random
from os import path
from v3_config import *
#from v3_assets import *
from v3_sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #cria uma screen com o tamanho pedido
        pygame.display.set_caption ('Teste Tiled Map') #muda o título da screen
        self.clock = pygame.time.Clock() #salva na variável o Clock
        pygame.key.set_repeat(500,100) # Inicia a função de repetir (tempo de espera, tempo para repetir cada ação)
        self.load_data()
        
        

    def load_data(self):
        #self.assets = Assets()
        
        self.map = TiledMap((path.join(map_DIR, 'mapa1.tmx')))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.SNAKE_HEAD_IMG = pygame.image.load(path.join(img_DIR, 'head_img.png')).convert_alpha()
        self.SNAKE_HEAD_IMG = pygame.transform.scale(self.SNAKE_HEAD_IMG, (snake_WIDTH, snake_HEIGHT))
       
        self.snake =  pygame.image.load(path.join(img_DIR, 'cobra_fumando.png')).convert_alpha()
        self.snake_img = pygame.transform.scale(self.snake, (25, 25))


        self.fruit_images = []
        for fruta in LISTA_FRUTAS:
            self.fruit_images.append((pygame.image.load(path.join(img_DIR, 'fruits', fruta)).convert_alpha()))

        #self.maca_img = pygame.image.load (path.join(img_DIR, 'maca.png')).convert_alpha()
        #self.maca_img = pygame.transform.scale(self.maca_img, (object_WIDTH, object_HEIGHT))
 
       # self.cereja_img = pygame.image.load (path.join(img_DIR, 'cereja.png')).convert_alpha()
        #self.cereja_img = pygame.transform.scale(self.cereja_img, (object_WIDTH, object_HEIGHT))

        #self.lista_frutas = [self.maca_img, self.cereja_img]
    
    def new(self):
        
        #cria os grupos:
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        # Spawna as barreiras
        for tile_object in self.map.tmxdata.objects:
            
            if tile_object.name == 'player':
                self.player = Snake(self, self.SNAKE_HEAD_IMG, tile_object.x, tile_object.y)
                #self.player_body = 
                #self.player = Player (self, self.snake_img, tile_object.x, tile_object.y )
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'fruit':
                #Fruta(self, tile_object.x, tile_object.y)
                Fruit (self, random.choice(self.fruit_images), tile_object.x, tile_object.y)
                
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
        self.player.update()
        self.camera.update(self.player)

        # Player colide com a frutas:
        hits = pygame.sprite.spritecollide (self.player, self.fruits, False)
        for hit in hits:
            # coloca alguma função (aumentar stamina, ex.)
            hit.kill()
        

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites: #Analisa cada um dos sprites do grupo e mandar imprimir
            self.screen.blit(sprite.image, self.camera.apply(sprite))


        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()



jogo = Game()
while True:
    jogo.new()
    jogo.run()

