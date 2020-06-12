import pygame
from os import path
from math import pi
vect = pygame.math.Vector2

# ========== CONDIGURAÇÕES GERAIS ==========
# Identifica diretórios de imagens, sons e fontes
GAME_DIR = path.dirname(__file__)
MAP_DIR = path.join(GAME_DIR, 'maps')
IMG_DIR = path.join(GAME_DIR, 'assets', 'img')
FONT_DIR = path.join(GAME_DIR, 'assets', 'fontes')
MUSIC_DIR = path.join(GAME_DIR, 'assets', 'sounds', 'music')
EFFECTS_DIR = path.join(GAME_DIR, 'assets', 'sounds', 'effects')



# Configurações da Tela
WIDTH = 700
HEIGHT = 700

# Clock e controle de FPS
clock = pygame.time.Clock()
FPS = 60
dt = clock.tick(FPS)/1000

# Arsenal de cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BROWN = (106, 55, 5)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)

# Estados para controle do fluxo
INIT = 0
GAME = 1
QUIT = 2

# Camadas
WALL_LAYER = 1
PLAYER_LAYER = 3
FRUITS_LAYER = 2

# Configuração do MHS:
A = 10 # amplitude do movimento
T = 2000  # período em milisseg
OMEGA = 2*pi/T


# ========== CONFIGURAÇÕES DE SPRITES ==========
# Tamanho dos objetos
OBJECT_WIDTH = 20
OBJECT_HEIGHT = 20

# Configurações do jogador
PLAYER_SPEED = 15
PLAYER_HEALTH = 100
PLAYER_VISION = 150
PLAYER_HIT_RECT = pygame.Rect (0, 0, 62, 62)
SNAKE_WIDTH = 30
SNAKE_HEIGHT = 30
SNAKE_MAX_STAMINE = 100
ATACK_RANGE = 100

# Configurações do mob Guaxinim
GUAXI_WALK_LEFT = ['L0.png', 'L1.png', 'L2.png']
GUAXI_WALK_RIGHT = ['R0.png', 'R1.png', 'R2.png']
GUAXI_WALK_UP = ['U0.png', 'U1.png', 'U2.png']
GUAXI_WALK_DOWN = ['D0.png', 'D1.png', 'D2.png']
GUAXI_WIDTH = 40
GUAXI_HEIGHT = 40
GUAXI_HIT_RECT = pygame.Rect (0,0, 0.9*GUAXI_WIDTH, 0.9*GUAXI_HEIGHT)
GUAXI_SPEED = 0.6*PLAYER_SPEED

# Configurações das frutas
LISTA_FRUTAS = ['abacaxi.png', 'cereja.png', 'laranja.png', 'limao.png', 'maca.png', 'morango.png', 'uva.png']
FRUTAS_STAMINA = 5 # quantidade de stamina que a fruta fornece
SNAKE_WALK_LEFT = ['L0.png', 'L1.png', 'L2.png']
SNAKE_WALK_RIGHT = ['R0.png', 'R1.png', 'R2.png']
SNAKE_WALK_UP = ['U0.png', 'U1.png', 'U2.png']
SNAKE_WALK_DOWN = ['D0.png', 'D1.png', 'D2.png']

# Configurações do veneno da cobra
VENENO_SPEED = 50
#VENENO_ANIM = []
VENENO_IMG = 'veneno0.png'
VENENO_DURATION = 2000
VENENO_FREQUENCY = 2000 # frequência de disparos
VENENO_HIT_RECT = pygame.Rect (0, 0, 16, 16)
VENENO_DESLOC_LEFT = vect (15, 10) 
VENENO_DESLOC_RIGHT = vect (50, 10) 
VENENO_DESLOC_UP = vect (32, 0) 
VENENO_DESLOC_DOWN = vect (32, 64) 
VENENO_DAMAGE = 10 # dano que o veneno causa
KICKBACK = 75 # recuo de disparo no player
VENENO_DESVIO = 5 # desvio aleatório do veneno
VENENO_CHARGE = 150 # (igual ao comprimento da barra gerada no HUD)

# Configurações do mob Bird
BIRD_RIGHT_IMG = ['right000.png', 'right001.png', 'right002.png', 'right003.png'] # direita
BIRD_LEFT_IMG = ['left000.png', 'left001.png', 'left002.png', 'left003.png'] # esquerda
BIRD_UP_IMG = ['up000.png', 'up001.png', 'up002.png', 'up003.png'] # cima
BIRD_DOWN_IMG = ['down000.png', 'down001.png', 'down002.png', 'down003.png'] # baixo
BIRD_DAMAGE = 10 # dano que o pássaro causa
BIRD_KNOCKBACK = 30 # repulsão quando atinge player
BIRD_HIT_RECT = pygame.Rect (0, 0, 30, 30) #ret. de colisão
BIRD_SPEEDS = [40, 50, 30, 25]
BIRD_HEALTH = 100
BIRD_ZONE = 100 # círculo que evita superposição de pássaros

# CORUJA
OWL_WALK_LEFT = ['L0.png', 'L1.png', 'L2.png']
OWL_WALK_RIGHT = ['R0.png', 'R1.png', 'R2.png']
OWL_WALK_UP = ['U0.png', 'U1.png', 'U2.png']
OWL_WALK_DOWN = ['D0.png', 'D1.png', 'D2.png']
OWL_HEIGHT = 40
OWL_WIDTH = 50

# ====== CONFIG SOM =======
MASTIGANDO = {'bite1':'bite1.wav', 'bite2':'bite2.wav', 'bite3':'bite3.wav'}



# REFERÊNCIAS
"""
https://opengameart.org/content/2d-fruits  #tile de frutas
https://opengameart.org/content/lpc-terrain-repack # tile de terrenos
https://opengameart.org/content/king-cobra # tile da cobrinha

"""
