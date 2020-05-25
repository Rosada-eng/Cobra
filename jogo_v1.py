# ===== INICIALIZAÇÃO =====
# ----- Importar bibliotecas 
import pygame
import random

pygame.init()

Delay_movimentos = 3
# ---- Gerar tela principal
WIDTH = 20*32
HEIGHT = 20*32
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ('The SNAKE is gonna SMOKE!! ')

# ----- Carrega os Assets:
snake_WIDHT = 10
snake_HEIGHT = 10
bixinho_WIDTH = 25
bixinho_HEIGHT = 25
object_WIDTH = 20
object_HEIGHT = 20
assets = {}

background = pygame.image.load ('assets/img/terra_solo.jpg').convert()
background = pygame.transform.scale (background, (WIDTH, HEIGHT))
bixinho = pygame.image.load ('assets/img/head_img.png').convert_alpha()
bixinho = pygame.transform.scale (bixinho, (snake_WIDHT, snake_HEIGHT))
cereja = pygame.image.load ('assets/img/cereja.png').convert_alpha()
cereja = pygame.transform.scale (cereja, (object_WIDTH, object_HEIGHT))
maca = pygame.image.load ('assets/img/maca.png').convert_alpha()
maca = pygame.transform.scale (maca, (object_WIDTH, object_HEIGHT))
body_image = pygame.image.load('assets/img/body1_img.png').convert_alpha()
body_image = pygame.transform.scale(body_image, (snake_WIDHT, snake_HEIGHT))
# Carrega orbs para animação
orbs_anim = []
for i in range(1, 6):
    nome_arquivo = 'assets/img/orb{}.png'.format(i)
    img = pygame.image.load(nome_arquivo).convert_alpha()
    img = pygame.transform.scale (img, (object_WIDTH, object_HEIGHT))
    orbs_anim.append(img)
# Carrega imagens da barra de vida
health_barr = []
for i in range(0, 21):
    nome_arquivo = 'assets/img/health/VIDA_{0}.png'.format(i)
    img = pygame.image.load(nome_arquivo).convert_alpha()
    img = pygame.transform.scale(img, (int(img.get_width()/2), int(img.get_height()/2)))
    health_barr.append(img)

score_font = pygame.font.SysFont (None, 26) # Falta adicionar estilo da fonte do placar

# Controle do jogo e FPS
game = True
clock = pygame.time.Clock()
FPS = 30


# ----- Inicia Estrutura de Dados:
# Classes:

class Snake(pygame.sprite.Sprite):
    def __init__ (self, img):
        # Construtor da classe mãe:
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH - bixinho_WIDTH)
        self.rect.centery = random.randint(0, HEIGHT - bixinho_HEIGHT)
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
    def __init__(self, img, parte_seguinte, player): # 'parte_seguinte' é o pedaço a frente do que será criado
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.player = player
        self.parte_seguinte = parte_seguinte
        self.rect.center = parte_seguinte.ultimas_posicoes[0]
        self.ultimas_posicoes = []

    def update(self):
        # Atualiza posição com a posição mais antiga da parte da frente
        self.rect.center = self.parte_seguinte.ultimas_posicoes[0]
        self.ultimas_posicoes.append(self.rect.center)
        # Guarda as últimas posições e joga fora o resto
        self.ultimas_posicoes = self.ultimas_posicoes[-Delay_movimentos:]



class Fruit(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - object_WIDTH)
        self.rect.y = random.randint(0, HEIGHT - object_HEIGHT)
        self.speedx = 0
        self.speedy = 0
        
        
class Orbe(pygame.sprite.Sprite):
    def __init__(self, anim):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação dos orbes
        self.anim = orbs_anim
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


class Life(pygame.sprite.Sprite):
    def __init__(self, barr, vida):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.barr = health_barr
        self.frame = 20  # Começa com vida cheia
        self.image = self.barr[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        # Guarda valor da vida
        self.vida = vida

    def update(self):
        # Verifica valor da vida e atualiza barra de vida
        self.vida = vida
        self.frame = (2*vida)
        self.image = self.barr[self.frame]
                


# ----- Cria grupos de sprite
all_sprites = pygame.sprite.Group()
all_fruits = pygame.sprite.Group()
all_orbs = pygame.sprite.Group()
snake_body = pygame.sprite.Group()

# ----- Cria jogador e o adiciona nos grupos:
player = Snake(bixinho)
all_sprites.add(player)
snake_body.add(player)
ultima_parte = player # Guarda última parte criada para a cobrinha

# ----- Cria frutas e as adiciona nos grupos
apple = Fruit(maca)
cherry = Fruit(cereja)
for i in range (2):
    all_fruits.add(apple)
    all_sprites.add(apple)
    all_fruits.add(cherry)
    all_sprites.add(cherry)

# ----- Cria barra de vida e a adiciona em all_sprites
vida = 10
barra_vida = Life(health_barr, vida)
all_sprites.add(barra_vida)

# ----- Cria orbs e adiciona nos sprites
orbes = Orbe(orbs_anim)
all_sprites.add(orbes)
all_orbs.add(orbes)


score = 0
colisao = 0
delay_orbe = 30000 #30 seg 


# ============ LOOP PRINCIPAL ============
while game:
    clock.tick(FPS)

    # ----- Analisa os eventos
    for event in pygame.event.get():
        #QUIT:
        if event.type == pygame.QUIT:
            game = False

        # ---- Verifica as Teclas:
        # ABAIXAR A TECLA
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.speedx != 6: #não permite andar p/ trás
                player.speedx = -6
                player.speedy = 0 #não permite andar na diagonal
            if event.key == pygame.K_RIGHT and player.speedx != -6:
                player.speedx = 6
                player.speedy = 0
            if event.key == pygame.K_UP and player.speedy != 6:
                player.speedy = -6
                player.speedx = 0
            if event.key == pygame.K_DOWN and player.speedy != -6:
                player.speedy = 6
                player.speedx = 0
            

    # ----- Atualiza estado do jogo
    # Atualizando posição do Player
    all_sprites.update()        

    # Verifica se houve colisão do jogador com frutas
    hits = pygame.sprite.spritecollide (player, all_fruits, True)
    if len(hits) > 0:
        nova_parte = Snake_Body(body_image, ultima_parte, player)
        all_sprites.add(nova_parte)
        snake_body.add(nova_parte)
        # Atualiza última parte 
        ultima_parte = nova_parte

        score += 50
        if hits[0] == apple:
            apple = Fruit(maca)
            all_fruits.add(apple)
            all_sprites.add(apple)
        else:
            cherry = Fruit(cereja)
            all_fruits.add(cherry)
            all_sprites.add(cherry)

    #verifica se houve colisão com o orbe
    hits = pygame.sprite.spritecollide (player, all_orbs, True)
    
    if len(hits)>0:
        colisao = 1
        last_update = pygame.time.get_ticks()
        vida -= 1
        if vida == 0: # Se a vida zerar, game over
            game = False

    if colisao != 0:
        now = pygame.time.get_ticks()
        elapsed_ticks = now - last_update
        if elapsed_ticks < delay_orbe:
            now = pygame.time.get_ticks()
            elapsed_ticks = now - last_update
        elif elapsed_ticks >= delay_orbe:
            orbes = Orbe(orbs_anim)
            all_orbs.add(orbes)
            all_sprites.add(orbes)
            colisao = 0
  

    # ---- Gera Saídas:
    window.fill ((0,0,0))                   # preenche a tela com a cor preta
    window.blit (player.image, player.rect) # insere imagem player
    
    # Desenha os objetos:

    # Desenha o placar
    text_surface = score_font.render ("{:08d}".format(score), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 10)
    window.blit (text_surface, text_rect)

    all_sprites.draw(window)

    #Atualiza o Frame
    pygame.display.update()


# ========== FINALIZAÇÃO ==========
pygame.quit()