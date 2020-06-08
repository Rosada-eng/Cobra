import pygame
import pytmx
import random
#from v3_assets import assets
from v4_config import *
from math import pi, sin

class Snake(pygame.sprite.Sprite):
    def __init__ (self, jogo, img, x, y): #será criado no proprio objeto 'jogo'
        # Construtor da classe mãe:
        self._layer = PLAYER_LAYER
        self.groups = jogo.all_sprites 
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo       
        self.image = img
        #self.image = pygame.transform.scale(self.image, (snake_WIDTH, snake_HEIGHT))
        self.x = x #declara as posições (x,y) em que o player será spawnado
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x + snake_WIDTH/2 ,y + snake_HEIGHT/2)
        self.speedx = 0
        self.speedy = 0 # Começa com velocidade zero 
        self.last_update = pygame.time.get_ticks()
        self.snake_count = 0
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.DOWN = False

        
    def get_keys(self):
        self.speedx, self.speedy = 0,0
        keys = pygame.key.get_pressed() #Salva uma dicionario de keys q estão sendo pressionadas
        if keys[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
            self.LEFT = True
            self.RIGHT = False
            self.UP = False
            self.DOWN = False
        elif keys[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
            self.LEFT = False
            self.RIGHT = True
            self.UP = False
            self.DOWN = False
        elif keys[pygame.K_UP]:
            self.speedy = -PLAYER_SPEED
            self.LEFT = False
            self.RIGHT = False
            self.UP = True
            self.DOWN = False
        elif keys[pygame.K_DOWN]:
            self.speedy = PLAYER_SPEED
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
                if self.speedx >0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.speedx <0:
                    self.x = hits[0].rect.right
                self.speedx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False)
            if hits:
                if self.speedy >0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.speedy <0:
                    self.y = hits[0].rect.bottom
                self.speedy = 0
                self.rect.y = self.y  

    def update(self):

        self.get_keys()
        self.x += self.speedx*dt #delta X = vx*deltaT
        self.y += self.speedy*dt #delta Y = vy*deltaT
        #obs.1: Usar dt garante que o personagem ande proporcionalmente à velocidade de processamento da maquina
        
        self.rect.x = self.x
        self.collide_with_walls ('x') #checa condições de colisao em X
        self.rect.y = self.y
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

    


class First_Body(pygame.sprite.Sprite):
    def __init__(self, jogo, img, ref, number): # Ref é a parte do corpo que vem antes da nova entidade
        # number: é o numero de movimentos que a parte está atrasada em relação à cabeça.
        # Construtor da classe mãe
        self._layer = PLAYER_LAYER
        self.groups = jogo.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.ref = ref
        self.image = pygame.transform.scale(self.image, (snake_BODY_WIDTH, snake_BODY_HEIGHT))
        self.rect = self.image.get_rect()
        self.number = number
        self.x = self.ref.rect.x  - snake_BODY_WIDTH/2 # O programa está levando em consideração o centro da imagem p/ dar blit
        self.y = self.ref.rect.y + snake_BODY_HEIGHT/2 #    Isso é consequência da Câmera
        self.rect.center = (self.x, self.y)

        self.set_direction = STILL


    def update(self):
        self.rect.center = (self.jogo.player.position[-self.number][0] - snake_BODY_WIDTH/2 , self.jogo.player.position[-self.number][1] + snake_BODY_HEIGHT/2)
        #self.y = self.ref.last_position_y[-1] # Move para a última posição da referencia antes de ela ter se movido

       # if self.rect.center != self.last_position[-1]:
       #         self.last_position.append (self.rect.center)
        #self.last_position_y.append (self.y) # Guarda as últimas posições x,y antes de mover

class Body(pygame.sprite.Sprite):
    def __init__(self, jogo, img, ref, number): # Ref é a parte do corpo que vem antes da nova entidade
        # number: é o numero de movimentos que a parte está atrasada em relação à cabeça.
        # Construtor da classe mãe
        self._layer = PLAYER_LAYER
        self.groups = jogo.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.ref = ref
        self.image = pygame.transform.scale(self.image, (snake_BODY_WIDTH, snake_BODY_HEIGHT))
        self.rect = self.image.get_rect()
        self.number = number
        self.x = self.ref.rect.x  - (2*self.number -1)*snake_BODY_WIDTH/2 # O programa está levando em consideração o centro da imagem p/ dar blit
        self.y = self.ref.rect.y + snake_BODY_HEIGHT/2 #    Isso é consequência da Câmera
        self.rect.center = (self.x, self.y)

        self.set_direction = STILL


    def update(self):
        self.rect.center = (self.jogo.player.position[-self.number][0] -(2*self.number - 1)* snake_BODY_WIDTH/2 , self.jogo.player.position[-self.number][1] + snake_BODY_HEIGHT/2)
        #self.y = self.ref.last_position_y[-1] # Move para a última posição da referencia antes de ela ter se movido

       # if self.rect.center != self.last_position[-1]:
       #         self.last_position.append (self.rect.center)
        #self.last_position_y.append (self.y) # Guarda as últimas posições x,y antes de mover

class Snake_Body(pygame.sprite.Sprite):
    def __init__(self, jogo, img, parte_seguinte): # 'parte_seguinte' é o pedaço a frente do que será criado
        # Construtor da classe mãe
        self._layer = PLAYER_LAYER
        self.groups = jogo.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.image = pygame.transform.scale(self.image, (snake_BODY_WIDTH, snake_BODY_HEIGHT))
        self.rect = self.image.get_rect()
        self.parte_seguinte = parte_seguinte #salva a lista com as últimas posições
        self.rect.center = parte_seguinte.ultimas_posicoes[0] #adota a coordenada da #delayº última posição
        self.ultimas_posicoes = [] #zera a lista 

    def update(self):
        # Atualiza posição com a posição mais antiga da parte da frente
        self.rect.center = self.parte_seguinte.ultimas_posicoes[0]
        self.ultimas_posicoes.append(self.rect.center)
        # Guarda as últimas posições e joga fora o resto
        self.ultimas_posicoes = self.ultimas_posicoes[-delay_movimentos:]

class Fruit(pygame.sprite.Sprite):
    def __init__(self, jogo, img, x, y):
        self.groups = jogo.all_sprites, jogo.fruits
        self._layer = FRUITS_LAYER
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.image = pygame.transform.scale(self.image, (object_WIDTH, object_HEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x,y)
        self.y_0 = y
        self.last_update = pygame.time.get_ticks()
        self.t = 0
        self.phi_0 = 2*pi / (random.randint (1,5)) #phi_inicial: Porção de uma volta.
        self.argumento = 0


    def update(self):
        
        now = pygame.time.get_ticks()
        delta_t = now - self.last_update
        
        self.argumento = (OMEGA*delta_t + self.phi_0)%360 # desconsidera o número de voltas já dadas
        if delta_t > T:
            delta_t = 0
                
        self.y = self.y_0 + A*sin(self.argumento)
        self.rect.center = (self.x, self.y)
  
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
        self.rect.x = random.randint(0, WIDTH - (object_WIDTH + 50))
        self.rect.y = random.randint(0, HEIGHT - (object_HEIGHT + 50))
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