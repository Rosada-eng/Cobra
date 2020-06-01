import pygame
import pytmx
import sys
from os import path
#from config import *
#from sprites import *
WIDTH = 700
HEIGHT = 450
PLAYER_SPEED = 20
FPS = 60
clock = pygame.time.Clock()
dt = clock.tick(FPS)/1000

class TiledMap:
    def __init__ (self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width*tm.tilewidth
        self.height = tm.height*tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid #ativa a função gid (identidade das imagens através dos numeros)
        for layer in self.tmxdata.visible_layers: #checa cada layer que está visivel
            if isinstance (layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
    
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    
class Player(pygame.sprite.Sprite):
    def __init__(self, jogo, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.jogo = jogo
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect()
        self.vx, self.vy = 0,0

    def get_keys(self): #Cuida da movimentação
        self.vx, self.vy = 0,0
        keys = pygame.key.get_pressed() #Salva uma dicionario de keys q estão sendo pressionadas
        if keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.vy = PLAYER_SPEED
        # Se eu utilizar elif ao invés do if, a movimentação na diagonal fica bloqueada
        if self.vx != 0 and self.vy != 0: #ou seja, vx = 100 e vy = 100. Logo, v = 100(raiz(2))
            self.vx *= 0.7071 #(multiplica pelo inverso da raiz de 2)
            self.vy *= 0.7071

    # Essa função permitiria ao personagem deslizar no eixo em que ele não colide.
    def collide_with_walls (self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False)
            if hits:
                if self.vx >0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx <0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False)
            if hits:
                if self.vy >0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy <0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y    
            ## bugg detected: O personagem teleporta quando colide de baixo para cima
    def update(self):   
        self.get_keys()
        self.x += self.vx*dt #delta X = vx*deltaT
        self.y += self.vy*dt #delta Y = vy*deltaT
        #obs.: Aqui, devem ser x e y, e nao rect, pois serão numeros FLOAT e não INT
        self.rect.x = self.x
        self.collide_with_walls ('x') #checa condições de colisao em X
        self.rect.y = self.y
        self.collide_with_walls('y') #checa condições de colisao em Y

class Obstacle (pygame.sprite.Sprite):
    def __init__(self, game, x,y, width, height):
        self.groups = game.walls 
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply (self, entity): # Aplica a câmera p/ as coordenadas da entidade
        return entity.rect.move(self.camera.topleft)

    def apply_rect (self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target): # Faz o mapa mover ao contrário da câmera -- OFFSET
        x = -target.rect.x + int(WIDTH/2) #Salva na variável a posição do target em relação à cam
        y = -target.rect.y + int(HEIGHT/2)

        # Delimitando as fronteiras do mapa
        x = min (0, x) # fronteira esquerda
        y = min (0, y) # fronteira superior
        x = max ((-self.width + WIDTH),x) #fronteira direita
        y = max ((-self.height + HEIGHT), y) #fronteira inferior

        self.camera = pygame.Rect(x, y, self.width, self.height) #ajusta a posição da câmera


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #cria uma screen com o tamanho pedido
        pygame.display.set_caption ('Teste Tiled Map') #muda o título da screen
        self.clock = pygame.time.Clock() #salva na variável o Clock
        pygame.key.set_repeat(500,100) # Inicia a função de repetir (tempo de espera, tempo para repetir cada ação)
        self.load_data()
        

    def load_data(self):
        game_DIR = path.dirname(__file__)
        map_DIR = path.join(game_DIR, 'maps')
        img_DIR = path.join(game_DIR, 'assets/img')
        self.map = TiledMap((path.join(map_DIR, 'mapa1.tmx')))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.snake =  pygame.image.load(path.join(img_DIR, 'cobra_fumando.png')).convert_alpha()
        self.snake_img = pygame.transform.scale(self.snake, (25, 25))
    
    def new(self):
        #self.player = Player(self, self.snake_img, 5, 5)
        #cria os grupos:
        self.walls = pygame.sprite.Group()
        # Spawna as barreiras
        for tile_object in self.map.tmxdata.objects:
            
            if tile_object.name == 'player':
                self.player = Player (self, self.snake_img, tile_object.x, tile_object.y )
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
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
        self.player.update()
        self.camera.update(self.player)
        

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.screen.blit(self.player.img, (self.camera.apply(self.player)))


        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

   

jogo = Game()
while True:
    jogo.new()
    jogo.run()



