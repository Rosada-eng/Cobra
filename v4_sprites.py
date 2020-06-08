import pygame
import pytmx
import random
from v4_config import *
from math import pi, sin
vect = pygame.math.Vector2

class Snake(pygame.sprite.Sprite):
    def __init__ (self, jogo, img, x, y): #será criado no proprio objeto 'jogo'
        # Construtor da classe mãe:
        self._layer = PLAYER_LAYER
        self.groups = jogo.all_sprites 
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo       
        self.image = img

        self.pos = vect (x, y) #declara as posições (x,y) em que o player será spawnado
        self.rect = self.image.get_rect()
        self.rect.center = (x + SNAKE_WIDTH/2 ,y + SNAKE_HEIGHT/2)
        self.speed = vect (0, 0) # Começa com velocidade zero 
        self.last_update = pygame.time.get_ticks()
        self.snake_count = 0
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.DOWN = False

        
    def get_keys(self):
        self.speed = vect (0, 0)
        keys = pygame.key.get_pressed() #Salva uma dicionario de keys q estão sendo pressionadas
        if keys[pygame.K_LEFT]:
            self.speed.x = -PLAYER_SPEED
            self.LEFT = True
            self.RIGHT = False
            self.UP = False
            self.DOWN = False
        elif keys[pygame.K_RIGHT]:
            self.speed.x = PLAYER_SPEED
            self.LEFT = False
            self.RIGHT = True
            self.UP = False
            self.DOWN = False
        elif keys[pygame.K_UP]:
            self.speed.y = -PLAYER_SPEED
            self.LEFT = False
            self.RIGHT = False
            self.UP = True
            self.DOWN = False
        elif keys[pygame.K_DOWN]:
            self.speed.y = PLAYER_SPEED
            self.LEFT = False
            self.RIGHT = False
            self.UP = False
            self.DOWN = True
        else:
            self.UP = False
            self.DOWN = False
            self.LEFT = False
            self.RIGHT = False

    def collide_with_walls (self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False) # retorna uma lista com os elementos do grupo q colidiram
            if hits:
                if self.speed.x >0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.speed.x <0:
                    self.pos.x = hits[0].rect.right
                self.speed.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False)
            if hits:
                if self.speed.y >0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.speed.y <0:
                    self.pos.y = hits[0].rect.bottom
                self.speed.y = 0
                self.rect.y = self.pos.y  

    def update(self):

        self.get_keys()
        self.pos.x += self.speed.x * dt #delta X = vx*deltaT
        self.pos.y += self.speed.y * dt #delta Y = vy*deltaT
        #obs.1: Usar dt garante que o personagem ande proporcionalmente à velocidade de processamento da maquina
        
        self.rect.x = self.pos.x
        self.collide_with_walls ('x') #checa condições de colisao em X
        self.rect.y = self.pos.y
        self.collide_with_walls('y') #checa condições de colisao em Y

        now = pygame.time.get_ticks()
        delta_t = now - self.last_update
        
        if self.LEFT:
            self.image = self.jogo.snake_left['L{}.png'.format(self.snake_count)]
            if delta_t > 150:
                delta_t = 0
                self.last_update = now
                self.snake_count +=1
                if self.snake_count > 2:
                    self.snake_count = 0
        elif self.RIGHT:
            self.image = self.jogo.snake_right['R{}.png'.format(self.snake_count)]
            if delta_t > 150:
                delta_t = 0
                self.last_update = now
                self.snake_count +=1
                if self.snake_count > 2:
                    self.snake_count = 0
        
        elif self.DOWN:
            self.image = self.jogo.snake_down['D{}.png'.format(self.snake_count)]
            if delta_t > 150:
                delta_t = 0
                self.last_update = now
                self.snake_count +=1
                if self.snake_count > 2:
                    self.snake_count = 0
        
        elif self.UP:
            self.image = self.jogo.snake_up['U{}.png'.format(self.snake_count)]
            if delta_t > 150:
                delta_t = 0
                self.last_update = now
                self.snake_count +=1
                if self.snake_count > 2:
                    self.snake_count = 0

    

class Fruit(pygame.sprite.Sprite):
    def __init__(self, jogo, img, x, y):
        self.groups = jogo.all_sprites, jogo.fruits
        self._layer = FRUITS_LAYER
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.image = pygame.transform.scale(self.image, (OBJECT_WIDTH, OBJECT_HEIGHT))
        self.rect = self.image.get_rect()
        self.pos = vect (x, y)
        self.rect.center = self.pos
        self.y_0 = self.pos.y
        self.last_update = pygame.time.get_ticks()
        self.t = 0
        self.phi_0 = 2*pi / (random.randint (1,5)) #phi_inicial: Porção de uma volta.
        self.argumento = 0


    def update(self):        
        now = pygame.time.get_ticks()
        delta_t = now - self.last_update        
        self.argumento = (OMEGA * delta_t + self.phi_0) % 360 # desconsidera o número de voltas já dadas
        if delta_t > T:
            delta_t = 0                
        self.pos.y = self.y_0 + A*sin(self.argumento)
        self.rect.center = self.pos
  
class Orbe(pygame.sprite.Sprite):
    def __init__(self, list_img):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação dos orbes
        self.anim = list_img
        # Inicia a animação colocando a primeira imagem na tela
        self.frame = 0                         # Guarda índice atual na animação
        self.image = self.anim[self.frame]     # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - (OBJECT_WIDTH + 50))
        self.rect.y = random.randint(0, HEIGHT - (OBJECT_HEIGHT + 50))
        # Guarda o tick que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()
        # Próxima imagem da animação (intervalo)
        self.frame_ticks = 100

    def update(self):
        # Verifica o tick atual
        now = pygame.time.get_ticks()
        # Verifica ticks decorridos desde a ultima mudança de frame
        elapsed_ticks = now - self.last_update
        # Verifica se já é hora de passar para a próxima:
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem
            self.last_update = now
            # Avança um frame
            self.frame += 1
            # Verifica se a animação acabou
            if self.frame == len(self.anim):
                # Se terminou: começa de novo
                self.frame = 0
            else:
             #Se não, passa para próxima imagem
               self.image = self.anim[self.frame]

# Falta importar vida do arquivo onde ficou salva e consertar erro do carregamento da vida
class Life(pygame.sprite.Sprite):
    def __init__(self, img, vida):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.barr = img
        self.frame = 20  # Começa com vida cheia
        self.image = self.barr[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        # Guarda valor da vida
        self.vida = vida

    def update(self):
        # Verifica valor da vida e atualiza barra de vida
        self.frame = (2*self.vida)
        self.image = self.barr[self.frame]



class Obstacle (pygame.sprite.Sprite):
    def __init__(self, jogo, x,y, width, height):
        self.groups = jogo.walls 
        self._layer = WALL_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
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

    def apply (self, entity): # Aplica a câmera p/ as coordenadas do sprite
        return entity.rect.move(self.camera.topleft)

    def apply_rect (self, rect): # Aplica a câmera p/ as coordenadas do rect
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