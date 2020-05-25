import pygame
import random
from assets import SNAKE_BODY_IMG, SNAKE_HEAD_IMG, APPLE_IMG, CHERRY_IMG, ORBS_ANIM, HEALTH_BARR
from config import WIDTH, HEIGHT, object_WIDTH, object_HEIGHT, snake_WIDTH, snake_HEIGHT, Delay_movimentos

class Snake(pygame.sprite.Sprite):
    def __init__ (self, assets):
        # Construtor da classe mãe:
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[SNAKE_HEAD_IMG]
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH - snake_WIDTH)
        self.rect.centery = random.randint(0, HEIGHT - snake_HEIGHT)
        self.speedx = 0
        self.speedy = 0 # Começa com velocidade zero (jogador decide como começar)
        self.ultimas_posicoes = [] # Guarda últimas posições

    def update(self):
        # Atualiza a posição da cabeça da cobrinha:
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Limita posições em que pode andar:
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <0:
            self.rect.top =0
        # Adiciona última posição na lista e limpa lista mantendo as adições mais recentes
        self.ultimas_posicoes.append(self.rect.center)
        self.ultimas_posicoes = self.ultimas_posicoes[-Delay_movimentos:]


class Snake_Body(pygame.sprite.Sprite):
    def __init__(self, assets, parte_seguinte): # 'parte_seguinte' é o pedaço a frente do que será criado
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[SNAKE_BODY_IMG]
        self.rect = self.image.get_rect()
        #self.player = player
        self.parte_seguinte = parte_seguinte
        self.rect.center = parte_seguinte.ultimas_posicoes[0]
        self.ultimas_posicoes = []

    def update(self):
        # Atualiza posição com a posição mais antiga da parte da frente
        self.rect.center = self.parte_seguinte.ultimas_posicoes[0]
        self.ultimas_posicoes.append(self.rect.center)
        # Guarda as últimas posições e joga fora o resto
        self.ultimas_posicoes = self.ultimas_posicoes[-Delay_movimentos:]

# Arrumar classe para sortear as imagens das frutas
class Fruit(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[APPLE_IMG]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - object_WIDTH)
        self.rect.y = random.randint(0, HEIGHT - object_HEIGHT)
        self.speedx = 0
        self.speedy = 0
        
        
class Orbe(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação dos orbes
        self.anim = assets[ORBS_ANIM]
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
    def __init__(self, assets, vida):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.barr = assets[HEALTH_BARR]
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
 