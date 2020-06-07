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
game_DIR = path.dirname(__file__)
map_DIR = path.join(game_DIR, 'maps')
img_DIR = path.join(game_DIR, 'assets/img')
song_DIR = path.join(game_DIR, 'assets', 'song')
font_DIR = path.join(game_DIR, 'assets', 'fontes')

# Layers: -- Faz o jogo dar blit numa sequência específica
WALL_LAYER = 1
PLAYER_LAYER = 3
FRUITS_LAYER = 2

# Jogador
PLAYER_SPEED = 15
delay_movimentos = 3
PLAYER_VISION = 100

# DIREÇÃO DE MOVIMENTO
RIGHT = +1
LEFT = -1
UP = -1
DOWN = +1
STILL = 0

# Tamanho da cobrinha
snake_HEAD_WIDTH = 15
snake_HEAD_HEIGHT = 15
snake_BODY_WIDTH = 15
snake_BODY_HEIGHT = 15

# Tamanho dos objetos
object_WIDTH = 20
object_HEIGHT = 20


# FRUTAS
LISTA_FRUTAS = ['abacaxi.png', 'cereja.png', 'laranja.png', 'limao.png', 'maca.png', 'morango.png', 'uva.png']

# Configuração do MHS:
A = 10 # amplitude do movimento
T = 20000  # período em milisseg
OMEGA = 2*pi/T

# Cores
BLACK = (0, 0, 0)

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