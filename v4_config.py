import pygame
from os import path
from math import pi
# Configurações da Tela
WIDTH = 700
HEIGHT = 450

# Clock
clock = pygame.time.Clock()
FPS = 60
dt = clock.tick(FPS)/1000

# Identifica diretórios de imagens, sons e fontes
GAME_DIR = path.dirname(__file__)
MAP_DIR = path.join(GAME_DIR, 'maps')
IMG_DIR = path.join(GAME_DIR, 'assets/img')
SONG_DIR = path.join(GAME_DIR, 'assets', 'song')
FONT_DIR = path.join(GAME_DIR, 'assets', 'fontes')

# Layers: -- Faz o jogo dar blit numa sequência específica
WALL_LAYER = 1
PLAYER_LAYER = 3
FRUITS_LAYER = 2

# Jogador
PLAYER_SPEED = 15
delay_movimentos = 3
PLAYER_VISION = 150

# DIREÇÃO DE MOVIMENTO



# Tamanho da cobrinha
SNAKE_WIDTH = 64
SNAKE_HEIGHT = 64

# Tamanho dos objetos
OBJECT_WIDTH = 20
OBJECT_HEIGHT = 20

# === Lista de Imagens p/ carregar
# FRUTAS
LISTA_FRUTAS = ['abacaxi.png', 'cereja.png', 'laranja.png', 'limao.png', 'maca.png', 'morango.png', 'uva.png']
WALK_LEFT = ['L0.png', 'L1.png', 'L2.png']
WALK_RIGHT = ['R0.png', 'R1.png', 'R2.png']
WALK_UP = ['U0.png', 'U1.png', 'U2.png']
WALK_DOWN = ['D0.png', 'D1.png', 'D2.png']

# Configuração do MHS:
A = 10 # amplitude do movimento
T = 2000  # período em milisseg
OMEGA = 2*pi/T

# Cores
BLACK = (0, 0, 0)
YELLOW = ()
GREEN = ()
RED = ()
WHITE = (255, 255, 255)

# Estados para controle do fluxo
INIT = 0
GAME = 1
QUIT = 2

# REFERÊNCIAS
"""
https://opengameart.org/content/2d-fruits  #tile de frutas
https://opengameart.org/content/lpc-terrain-repack # tile de terrenos
https://opengameart.org/content/king-cobra # tile da cobrinha

"""
