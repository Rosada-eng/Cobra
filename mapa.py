# ===== INICIALIZAÇÃO =====
#Importar bibliotecas 
import pygame
import random
from os import path
<<<<<<< HEAD
import pytmx
from pytmx.util_pygame import load_pygame


=======
>>>>>>> b062f24b0b6f40a54943261373b4fb90705fdc63

# Inicializa pygame
pygame.init()


# ---- Gerar tela principal
WIDTH = 20*32
HEIGHT = 30*32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ('The SNAKE is gonna SMOKE!! ')


<<<<<<< HEAD
class TiledMap:
=======

class TiledMap():
>>>>>>> b062f24b0b6f40a54943261373b4fb90705fdc63
    def __init__ (self, filename):
        # Lê o arquivo .tmx e deixa os tiles transparentes
        tm = load_pygame(filename, pixelalpha = True) 
        # configurações:
        self.width = tm.width * tm.tilewidth # Num. de Tiles * Tamanho dos Tiles (em X)
        self.height = tm.height * tm.tileheight # Num. de Tiles * Tamanho dos Tiles (em Y)
        # cria variável que guarda os dados lidos no objeto
        self. tmxdata = tm

    def render (self, surface):
        # Captura a Identidade do Tile:
        ti = self.tmxdata.get_tile_image_by_gid()
        # Torna todos os Layers do Tiled visíveis:
        for layer in self.tmxdata.visible_layers:
            # Se for uma camada do tipo Layer:
            if isinstance (layer, pytmx.TiledTileLayer):
                # Pega as cordenadas (x,y), a identidade (gid) de cada tile, um layer de cada vez
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        # Desenha o tile 
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
<<<<<<< HEAD
    
=======
>>>>>>> b062f24b0b6f40a54943261373b4fb90705fdc63
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

<<<<<<< HEAD
#carregar o Mapa:
map_folder = path.join(path.dirname(__file__), 'maps')
=======



# -- Gerar o mapa:

game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
>>>>>>> b062f24b0b6f40a54943261373b4fb90705fdc63
map = TiledMap(path.join(map_folder, 'tilemap.tmx'))
map_img = map.make_map()
map_rect = map_img.get_rect()

# blit
screen.blit(map_img, (WIDTH//2, HEIGHT//2))