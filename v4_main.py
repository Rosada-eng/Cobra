import pygame
import pytmx
import sys
from random import *
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
# Parâmetros de controle do jogo
OPEN_GAME = True
# INIT_SCREEN = True
Fase1 = True
Fase2 = False
Fase3 = False


class Game:
    def __init__(self, Fase1, Fase2, Fase3):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #cria uma screen com o tamanho pedido
        pygame.display.set_caption ('Teste Tiled Map') #muda o título da screen
        pygame.key.set_repeat(500,100) # Inicia a função de repetir (tempo de espera, tempo para repetir cada ação)
        self.load_data()
        #self.last_hit = 0 # último hit do pássaro na cobra
        self.ANALISE = True # analisa múltiplos hits do pássaro na cobra

        self.playing = True
        self.mostrador = " "
        self.tempo_fase = FASE1
        self.last_sec = 0
        self.Fase1 = Fase1
        self.Fase2 = Fase2
        self.Fase3 = Fase3
        self.player_level = 1

        self.last_spawn = 0
        self.paused = False
        self.GAMEOVER = False

        self.last_sec = 0

        
        
    def load_data(self):
        # cria mapa
        if Fase1:       
            self.map = TiledMap((path.join(MAP_DIR, 'Fase1.tmx')))
            self.map_img = self.map.make_map()
            self.map_rect = self.map_img.get_rect()

        elif Fase2:
            self.map = TiledMap((path.join(MAP_DIR, 'mapa1.tmx')))
            self.map_img = self.map.make_map()
            self.map_rect = self.map_img.get_rect()

        self.see_img = pygame.image.load(path.join(IMG_DIR, 'now_you_see.png')).convert_alpha()
        self.see_img = pygame.transform.scale(self.see_img, (30,30))
        self.not_see_img = pygame.image.load(path.join(IMG_DIR, 'now_you_dont.png')).convert_alpha()
        self.not_see_img = pygame.transform.scale(self.not_see_img, (30,30))

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

        # ==== FONTS ====
        self.alagard = path.join(FONT_DIR, 'alagard.TTF')
        self.romulus = path.join(FONT_DIR, 'romulus.TTF')
        # ==== Telas ====
        self.cortina_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.cortina_screen.fill((210,105,30, 170))
        self.gameover_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.gameover_screen.fill((0,0,0, 220))
        # ==== SOUND ====
        # --- música de fundo ---
        pygame.mixer.music.load(path.join(MUSIC_DIR, 'sonarctica_v7.ogg'))
        pygame.mixer.music.set_volume(0.1)
        # -- Dicionário com os efeitos
        self.sound_effects = {}
        self.sound_effects['hit'] = pygame.mixer.Sound(path.join(EFFECTS_DIR, '1hit.ogg'))
        self.sound_effects['pick_fruit'] = pygame.mixer.Sound(path.join(EFFECTS_DIR, 'task_completed.wav'))
        self.sound_effects['bite1'] = pygame.mixer.Sound(path.join(EFFECTS_DIR,'mastigando', 'bite1.ogg'))
        self.sound_effects['bite2'] = pygame.mixer.Sound(path.join(EFFECTS_DIR,'mastigando', 'bite2.ogg'))
        self.sound_effects['bite3'] = pygame.mixer.Sound(path.join(EFFECTS_DIR,'mastigando', 'bite3.ogg'))
        self.sound_effects['in-grass'] = pygame.mixer.Sound(path.join(EFFECTS_DIR, 'grass_in_or_out.ogg'))
        self.sound_effects['grass_walk'] = pygame.mixer.Sound(path.join(EFFECTS_DIR,'grass_walk.ogg'))
        self.sound_effects['1step_grass'] = pygame.mixer.Sound(path.join(EFFECTS_DIR,'1step - grass_walk.ogg'))

    def draw_text(self, text, font_name, size, color, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)
    
        
    def new(self):   
        #cria os grupos:
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        # self.birds = pygame.sprite.Group ()
        self.veneno = pygame.sprite.Group()
        self.crazy_birds = pygame.sprite.Group()
        self.mato_grosso = pygame.sprite.Group()
        self.detect_prey = pygame.sprite.Group()
        # Spawna as barreiras
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Snake(self, self.snake_right['R1.png'], tile_object.x, tile_object.y)
            if tile_object.name == 'Wall':
                Object(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 'WALL')
            if tile_object.name == 'mato grosso':
                Object(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 'MATO')
            if tile_object.name == 'fruit':
                Fruit (self, choice(self.fruit_images), tile_object.x, tile_object.y)
            # if tile_object.name == 'Passaro':
            #     Bird (self, tile_object.x, tile_object.y)    
            if tile_object.name == 'presa1':
                self.presa1 = Prey(self, self.guaxi_right['R1.png'], tile_object.x, tile_object.y)    
            if tile_object.name == 'presa2':
                self.presa2 = Prey(self, self.guaxi_right['R1.png'], tile_object.x, tile_object.y)    
            if tile_object.name == 'presa3':
                self.presa3 = Prey(self, self.guaxi_right['R1.png'], tile_object.x, tile_object.y)    
        for i in range (16):
            # sorteio pra deixar aleatório a qtde de pássaros que vem de um lado e do outro
            sorteio = choice([0, 1, 2, 3])
            # pássaros que vão pra direita
            if sorteio == 0:  
                posx = randint (-300, -100)
                speedx = choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_right_img['right000.png'], posx, randint(0, self.map.height), speedx, 0)     
            # pássaros que vão pra direita
            elif sorteio == 1:  
                posx = randint (self.map.width + 20, self.map.width + 100)
                speedx = -choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_left_img['left000.png'], posx, randint(0, self.map.height), speedx, 0)     
            # pássaros que vão pra cima
            elif sorteio == 2:  
                posy = randint (self.map.height + 50, self.map.height + 150)
                speedy = -choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_up_img['up000.png'], randint(0, self.map.width), posy, 0, speedy)     
            # pássaros que vão pra baixo
            else:  
                posy = randint (-300, -100)
                speedy = choice(BIRD_SPEEDS)
                CrazyBirds(self, self.bird_down_img['down000.png'], randint(0, self.map.width), posy, 0, speedy)     
        # cria câmera
        self.camera = Camera(self.map.width, self.map.height)

    def respawn(self, type):
        if type == 'fruit':
            
            for sprite in self.fruits.sprites(): # primeiramente, remove todas as frutas que não foram colhetadas
                sprite.kill()
                self.last_spawn = pygame.time.get_ticks()
            for tile_object in self.map.tmxdata.objects:
                if tile_object.name == 'fruit':
                    Fruit (self, choice(self.fruit_images), tile_object.x, tile_object.y)


    def run(self):
        pygame.mixer.music.play (loops=-1)
        while self.playing:
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
            if event.type == pygame.QUIT:
                self.quit()


    def timer (self):
        if self.tempo_fase <= 0: # Analisa se acabou o tempo. Se sim, o jogo acaba.
            self.GAMEOVER = True
            #self.playing = False
        else:
            segundos_total = self.tempo_fase // 1000 # analisa o tempo em segundos
            seg = segundos_total % 10 # pega o último dígito (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            tempo_em_min = segundos_total / 60
            minutos = tempo_em_min // 1 # Pega a parte inteira dos minutos
            frac_min = tempo_em_min % 1 # Pega a parte fracionária do minuto
            frac_min_em_seg = (frac_min * 60) # Transforma a parte fracionária do minuto em segundos (esse valor é menor que 60)
            dez_seg = (frac_min_em_seg // 10) % 10 # retira o último digito (seg) e pega o último algarismo após essa remoção (algarismo da dez_seg)

            self.mostrador = "{0:.0f} : {1:.0f}{2}" .format(minutos, dez_seg, seg)
            return self.mostrador          

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        now = pygame.time.get_ticks()
        delta_t = now - self.last_sec
        if delta_t >= 1000: # intervalo de 1 seg
            self.last_sec = now
            self.tempo_fase -= 1000       

        # Se o jogador morre... (ainda tem que criar os if's pra fase que ele estiver)
        if self.player.health <= 0:
            self.Fase1 = False # finaliza Fase1
            self.playing = False # encerra run da atual fase
                
        if self.player.stamine >= SNAKE_MAX_STAMINE/10: # configurar para quando dá o bote
            if self.Fase1:
                self.Fase1 = False # finaliza Fase1
                self.playing = False # finaliza run da Fase1
                self.Fase2 = True # passa pra Fase2
                #self.playing = True
            # elif self.Fase2:
            #     self.Fase2 = False
            #     self.playing = False
            #     self.Fase3 = True
            # elif self.Fase3:
            #     self.Fase3 = False
            #     self.playing = False
            #     self.FASE_A_DETERMINAR = True
 
 
 
 
        # if hits:
        #     self.player.posic += vect (BIRD_KNOCKBACK, 0).rotate(90)


               
    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # -- Blit cada sprite:
        for sprite in self.all_sprites: #Analisa cada um dos sprites do grupo e mandar imprimir
            # -- Pássaro --
            # if isinstance (sprite, CrazyBirds):
            #     sprite.draw_life_bar()
            # -- Fruta --
            if isinstance (sprite, Fruit): # se for relacionado a classe Fruit
                quad_dist_to_player = (self.player.posic.x - sprite.pos.x)**2 + (self.player.posic.y - sprite.pos.y)**2
                if quad_dist_to_player <= PLAYER_VISION**2: # Exibe a fruta somente se ela estiver dentro do alcance da visão
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # --- HUD ---
        background = pygame.Surface ((190, 90)).convert_alpha()
        background.fill ((250, 215, 160))
        self.screen.blit(background, (5,5))
        # - HP:
        self.draw_text ("HP:", self.romulus, 20, BLACK, 20, 20)
        health_player_bar(self.screen, 40, 10, self.player.health / PLAYER_HEALTH)
        # - SP:
        self.draw_text ("SP:", self.romulus, 20, BLACK, 20, 35)
        stamine_player_bar (self.screen, 40, 30, self.player.stamine / SNAKE_MAX_STAMINE)
        # - Poison cooldown:
        poison_charge_bar (self.screen, 40, 45, self.player.charge)
        # - LVL:
        self.draw_text ("Lvl:", self.romulus, 20, BLACK, 20, 70)
        self.draw_text ("{}".format(self.player_level), self.romulus, 40, RED, 50,70 )
        # - Símbolo de Visibilidade
        if self.player.INGRASS:
            self.screen.blit(self.not_see_img, (160,60))
        else:
            self.screen.blit(self.see_img, (160,60))

        # -- PAUSE --
        if self.paused:
            self.screen.blit(self.cortina_screen, (0,0))
            self.draw_text("PAUSE", self.romulus, 80, (75,0,130), WIDTH/2, HEIGHT/2)
        # -- GAME OVER -- 
        if self.GAMEOVER:
            self.screen.blit(self.gameover_screen, (0,0))
            self.draw_text("GAME OVER!", self.romulus, 80, (149,165,166), WIDTH/2, HEIGHT/2)
        # -- Timer --
        self.draw_text(self.timer(), self.romulus, 40, WHITE, WIDTH/2 , 20)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()



jogo = Game(Fase1, Fase2, Fase3)

# ========== LOOPING DE COMANDO ==========
while OPEN_GAME:
    while Fase1:
        jogo.new()
        jogo.run()
        # Se o jogador passou da fase 1...
        if jogo.Fase2 == True: # a 1° condição é quando dá o bote
            Fase1 = False
            Fase2 = True
            jogo.playing = True # libera run da próxima fase
            jogo.load_data()
        # Se o jogador morreu...
        elif jogo.player.health <= 0:
            Fase1 = False
            OPEN_GAME = False # '''Esse tem que ser configurado pra só quando o jogador encerrar'''
    while Fase2:
        jogo.new()
        jogo.run()

