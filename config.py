import pygame
from os import path

# Identifica diretórios de imagens, sons e fontes
Img_DIR = path.join(path.dirname(__file__), 'assets', 'img')
Song_DIR = path.join(path.dirname(__file__), 'assets', 'song')
Font_DIR = path.join(path.dirname(__file__), 'assets', 'fontes')

# Confiurações gerais
Delay_movimentos = 3
WIDTH = 20*32
HEIGHT = 20*32
FPS = 30

# Tamanho da cobrinha
snake_WIDTH = 10
snake_HEIGHT = 10

# Tamanho dos objetos
object_WIDTH = 20
object_HEIGHT = 20

# Cores
Black = (0, 0, 0)

# Estados para controle do fluxo
INIT = 0
GAME = 1
QUIT = 2

# Fontes
#score_font = pygame.font.SysFont(None, 26) # Falta adicionar estilo da fonte do placar 