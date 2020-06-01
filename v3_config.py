import pygame
from os import path
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

# Jogador
PLAYER_SPEED = 20
delay_movimentos = 3

# Tamanho da cobrinha
snake_WIDTH = 10
snake_HEIGHT = 10

# Tamanho dos objetos
object_WIDTH = 20
object_HEIGHT = 20

# Cores
BLACK = (0, 0, 0)

# Estados para controle do fluxo
INIT = 0
GAME = 1
QUIT = 2

