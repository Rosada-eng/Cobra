import pygame
import pytmx
import sys
import random
from os import path
from v4_config import *
from v4_sprites import *

# ========== HUD do jogo ==========
# ----- Barra de vida do jogador
def health_player_bar(surf, x, y, fracao): # (sup. de desesnho, x, y, porcentagem)
    if fracao < 0:
        fracao = 0
    BAR_WIDTH = 150
    BAR_HEIGHT = 15
    preench = fracao * BAR_WIDTH # preenchimento depende da porcentagem
    contorno_rect = pygame.Rect (x, y, BAR_WIDTH, BAR_HEIGHT) # retangulo (contorno) da barra de vida 
    preench_rect = pygame.Rect(x, y, preench, BAR_HEIGHT) # retangulo preenchimento
    if fracao > 0.75:
        color = GREEN
    elif fracao > 0.5:
        color = YELLOW
    elif fracao > 0.25:
        color = ORANGE
    else: 
        color = RED
    pygame.draw.rect(surf, color, preench_rect) # desenha 
    pygame.draw.rect(surf, BLACK, contorno_rect, 3)

# ----- Barra de Stamina
def stamine_player_bar (surf, x, y, stamina):
    BAR_WIDTH = 150
    BAR_HEIGHT = 10
    preench = stamina * BAR_WIDTH
    contorno_rect = pygame.Rect (x, y, BAR_WIDTH, BAR_HEIGHT)
    preench_rect = pygame.Rect (x, y, preench, BAR_HEIGHT)
    color = BLUE
    pygame.draw.rect(surf, color, preench_rect) 
    pygame.draw.rect(surf, BLACK, contorno_rect, 3)

# ----- Barra de carga do disparo
def poison_charge_bar (surf, x, y, charge):
    BAR_WIDTH = 150
    BAR_HEIGHT = 10
    preench = charge
    contorno_rect = pygame.Rect (x, y, BAR_WIDTH, BAR_HEIGHT)
    preench_rect = pygame.Rect (x, y, preench, BAR_HEIGHT)
    color = RED
    pygame.draw.rect(surf, color, preench_rect) 
    pygame.draw.rect(surf, BLACK, contorno_rect, 3)

# ========== CENTRAL DE COMANDO ==========
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #cria uma screen com o tamanho pedido
        pygame.display.set_caption ('Teste Tiled Map') #muda o título da screen

        pygame.key.set_repeat(500,100) # Inicia a função de repetir (tempo de espera, tempo para repetir cada ação)
        self.load_data()
        self.last_hit = 0 # último hit do pássaro na cobra
        self.ANALISE = True # analisa múltiplos hits do pássaro na cobra
        
    def load_data(self):
        # cria mapa       
        self.map = TiledMap((path.join(MAP_DIR, 'mapa1.tmx')))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # --- Cobra ---
            # Esquerda
        self.snake_left = {}
        for img in SNAKE_WALK_LEFT:
            self.snake_left[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_left[img] =  pygame.transform.scale(self.snake_left[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
            # Direita
        self.snake_right = {}
        for img in SNAKE_WALK_RIGHT:
            self.snake_right[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_right[img] =  pygame.transform.scale(self.snake_right[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
            # Cima
        self.snake_up = {}
        for img in SNAKE_WALK_UP:
            self.snake_up[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_up[img] =  pygame.transform.scale(self.snake_up[img], (SNAKE_WIDTH, SNAKE_HEIGHT))
            # Baixo
        self.snake_down = {}
        for img in SNAKE_WALK_DOWN:
            self.snake_down[img] =  pygame.image.load(path.join(IMG_DIR, 'King Snake', img)).convert_alpha()
            self.snake_down[img] =  pygame.transform.scale(self.snake_down[img], (SNAKE_WIDTH, SNAKE_HEIGHT))

        # --- Guaxinim ---
            # Esquerda
            self.guaxi_left = {}
        for img in GUAXI_WALK_LEFT:
            self.guaxi_left[img] =  pygame.image.load(path.join(IMG_DIR, 'guaxinim_cinza', img)).convert_alpha()
            self.guaxi_left[img] =  pygame.transform.scale(self.guaxi_left[img], (GUAXI_WIDTH, GUAXI_HEIGHT))
            # Direita
        self.guaxi_right = {}
        for img in GUAXI_WALK_RIGHT:
            self.guaxi_right[img] =  pygame.image.load(path.join(IMG_DIR, 'guaxinim_cinza', img)).convert_alpha()
            self.guaxi_right[img] =  pygame.transform.scale(self.guaxi_right[img], (GUAXI_WIDTH, GUAXI_HEIGHT))
            # Cima
        self.guaxi_up = {}
        for img in GUAXI_WALK_UP:
            self.guaxi_up[img] =  pygame.image.load(path.join(IMG_DIR, 'guaxinim_cinza', img)).convert_alpha()
            self.guaxi_up[img] =  pygame.transform.scale(self.guaxi_up[img], (GUAXI_WIDTH, GUAXI_HEIGHT))
            # Baixo
        self.guaxi_down = {}
        for img in GUAXI_WALK_DOWN:
            self.guaxi_down[img] =  pygame.image.load(path.join(IMG_DIR, 'guaxinim_cinza', img)).convert_alpha()
            self.guaxi_down[img] =  pygame.transform.scale(self.guaxi_down[img], (GUAXI_WIDTH, GUAXI_HEIGHT))
       
        # --- Coruja ---
            # Esquerda
        self.owl_left = {}
        for img in OWL_WALK_LEFT:
            self.owl_left[img] =  pygame.image.load(path.join(IMG_DIR, 'flying_owl', img)).convert_alpha()
            self.owl_left[img] =  pygame.transform.scale(self.owl_left[img], (OWL_WIDTH, OWL_HEIGHT))
            # Direita
        self.owl_right = {}
        for img in OWL_WALK_RIGHT:
            self.owl_right[img] =  pygame.image.load(path.join(IMG_DIR, 'flying_owl', img)).convert_alpha()
            self.owl_right[img] =  pygame.transform.scale(self.owl_right[img], (OWL_WIDTH, OWL_HEIGHT))
            # Cima
        self.owl_up = {}
        for img in OWL_WALK_UP:
            self.owl_up[img] =  pygame.image.load(path.join(IMG_DIR, 'flying_owl', img)).convert_alpha()
            self.owl_up[img] =  pygame.transform.scale(self.owl_up[img], (OWL_WIDTH, OWL_HEIGHT))
            # Baixo
        self.owl_down = {}
        for img in OWL_WALK_DOWN:
            self.owl_down[img] =  pygame.image.load(path.join(IMG_DIR, 'flying_owl', img)).convert_alpha()
            self.owl_down[img] =  pygame.transform.scale(self.owl_down[img], (OWL_WIDTH, OWL_HEIGHT))

        
        # --- Frutas ---
        self.fruit_images = []
        for fruta in LISTA_FRUTAS:
            self.fruit_images.append((pygame.image.load(path.join(IMG_DIR, 'fruits', fruta)).convert_alpha()))

        # --- Pássaro ---
        # Direita
        self.bird_right_img = {}
        for img in BIRD_RIGHT_IMG:
            self.bird_right_img[img] = pygame.image.load(path.join(IMG_DIR, img)).convert_alpha()
        # Esquerda
        self.bird_left_img = {}
        for img in BIRD_LEFT_IMG:
            self.bird_left_img[img] = pygame.image.load(path.join(IMG_DIR, img)).convert_alpha()
        # Cima
        self.bird_up_img = {}
        for img in BIRD_UP_IMG:
            self.bird_up_img[img] = pygame.image.load(path.join(IMG_DIR, img)).convert_alpha()
        # Baixo
        self.bird_down_img = {}
        for img in BIRD_DOWN_IMG:
            self.bird_down_img[img] = pygame.image.load(path.join(IMG_DIR, img)).convert_alpha()

        # --- Veneno da cobra ---
        self.veneno_img = pygame.image.load(path.join(IMG_DIR, VENENO_IMG)).convert_alpha()
    
    def new(self):   
        #cria os grupos:
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        # self.birds = pygame.sprite.Group ()
        self.veneno = pygame.sprite.Group()
        self.crazy_birds = pygame.sprite.Group()
        # Spawna as barreiras
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Snake(self, self.snake_right['R1.png'], tile_object.x, tile_object.y)
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height) 
            if tile_object.name == 'fruit':
                Fruit (self, random.choice(self.fruit_images), tile_object.x, tile_object.y)
            # if tile_object.name == 'Passaro':
            #     Bird (self, tile_object.x, tile_object.y)    
            if tile_object.name == 'presa1':
                self.guaxinim = Prey(self, self.guaxi_right['R1.png'], tile_object.x, tile_object.y)    
        for i in range (8):
            # sorteio pra deixar aleatório a qtde de pássaros que vem de um lado e do outro
            sorteio = random.choice([0, 1, 2, 3])
            # pássaros que vão pra direita
            if sorteio == 0:  
                posx = random.randint (-300, -100)
                speedx = random.choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_right_img['right000.png'], posx, random.randint(0, self.map.height), speedx, 0)     
            # pássaros que vão pra direita
            elif sorteio == 1:  
                posx = random.randint (self.map.width + 20, self.map.width + 100)
                speedx = -random.choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_left_img['left000.png'], posx, random.randint(0, self.map.height), speedx, 0)     
            # pássaros que vão pra cima
            elif sorteio == 2:  
                posy = random.randint (self.map.height + 50, self.map.height + 150)
                speedy = -random.choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_up_img['up000.png'], random.randint(0, self.map.width), posy, 0, speedy)     
            # pássaros que vão pra baixo
            else:  
                posy = random.randint (-300, -100)
                speedy = random.choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_down_img['down000.png'], random.randint(0, self.map.width), posy, 0, speedy)     
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
        # --- Player colide com a frutas:
        hits = pygame.sprite.spritecollide (self.player, self.fruits, False, pygame.sprite.collide_mask)
        for hit in hits:
            # frutinha já era
            hit.kill()
            # aumenta stamina
            self.player.stamine += FRUTAS_STAMINA
            if self.player.stamine > SNAKE_MAX_STAMINE:
                self.player.stamine = SNAKE_MAX_STAMINE
        

        # --- Player colide com pássaros
        now = pygame.time.get_ticks()
        delay = now - self.last_hit
        if delay > 2000:
            self.ANALISE = True
        if self.ANALISE:
            hits = pygame.sprite.spritecollide (self.player, self.crazy_birds, False, pygame.sprite.collide_mask)           
            self.last_hit = pygame.time.get_ticks()   
            # Se colidiu, trava colisão por delay=2s para evitar múltiplas colisões num único instante    
            for hit in hits:
                self.ANALISE = False
                self.player.health -= BIRD_DAMAGE
                hit.speed = vect (0, 0)
                if self.player.health <= 0:
                    self.playing = False
            # if hits:
            #     self.player.posic += vect (BIRD_KNOCKBACK, 0).rotate(90)


        # --- PLayer colide com pássaros
        # hits = pygame.sprite.spritecollide (self.player, self.birds, False)
        # for hit in hits:
        #     self.player.health -= BIRD_DAMAGE
        #     hit.speed = vect (0, 0)
        #     if self.player.health <= 0:
        #         self.playing = False
        # if hits:
        #     self.player.posic += vect (BIRD_KNOCKBACK, 0).rotate(-hits[0].angulo)
               
    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites: #Analisa cada um dos sprites do grupo e mandar imprimir
            # -- Pássaro --
            # if isinstance (sprite, Bird):
            #     sprite.draw_life_bar()
            # -- Fruta --
            if isinstance (sprite, Fruit): # se for relacionado a classe Fruit
                quad_dist_to_player = (self.player.posic.x - sprite.pos.x)**2 + (self.player.posic.y - sprite.pos.y)**2
                if quad_dist_to_player <= PLAYER_VISION**2: #spawna a fruta somente se ela estiver dentro do alcance da visão
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        health_player_bar(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        stamine_player_bar (self.screen, 10, 30, self.player.stamine / SNAKE_MAX_STAMINE)
        poison_charge_bar (self.screen, 10, 45, self.player.charge)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()



jogo = Game()
while True:
    jogo.new()
    jogo.run()

