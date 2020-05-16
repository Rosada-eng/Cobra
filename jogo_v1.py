# ===== INICIALIZAÇÃO =====
# ----- Importar bibliotecas 
import pygame
import random

pygame.init()


# ---- Gerar tela principal
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ('The SNAKE is gonna SMOKE!! ')

# ----- Carrega os Assets:
bixinho_WIDTH = 30
bixinho_HEIGHT = 30
object_WIDTH = 20
object_HEIGHT = 20
assets = {}

background = pygame.image.load ('assets/img/terra_solo.jpg').convert()
background = pygame.transform.scale (background, (WIDTH, HEIGHT))
bixinho = pygame.image.load ('assets/img/lindwurm.png').convert_alpha()
bixinho = pygame.transform.scale (bixinho, (bixinho_WIDTH, bixinho_HEIGHT))
cereja = pygame.image.load ('assets/img/cereja.png').convert_alpha()
cereja = pygame.transform.scale (cereja, (object_WIDTH, object_HEIGHT))
maca = pygame.image.load ('assets/img/maca.png').convert_alpha()
maca = pygame.transform.scale (maca, (object_WIDTH, object_HEIGHT))
# Carrega orbs para animação
orbs_anim = []
for i in range(1, 6):
    nome_arquivo = 'assets/img/orb{}.png'.format(i)
    img = pygame.image.load(nome_arquivo).convert_alpha()
    img = pygame.transform.scale (img, (20, 20))
    orbs_anim.append(img)

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
        self.speedy = -6 # Começa com velocidade para cima

    def update(self):
        # Atualiza a posição da cobrinha:
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
        
    def update(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y


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
        self.rect.x = random.randint(0, WIDTH - object_WIDTH)
        self.rect.y = random.randint(0, HEIGHT - object_HEIGHT)
        # Guarda o tick que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()
        # Próxima imagem da animação (intervalo)
        self.frame_ticks = 50

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
                # Se não, passa para próxima imagem
                self.image = self.anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.rect.x
                self.rect.y = self.rect.y


# ----- Cria grupos
all_sprites = pygame.sprite.Group()
all_fruits = pygame.sprite.Group()
all_orbs = pygame.sprite.Group()

# ----- Cria jogador:
player = Snake(bixinho)
all_sprites.add(player)

# ----- Cria frutas
apple = Fruit(maca)
cherry = Fruit(cereja)
for i in range (2):
    all_fruits.add(apple)
    all_sprites.add(apple)
    all_fruits.add(cherry)
    all_sprites.add(cherry)

# ----- Cria orbs
orbes = Orbe(orbs_anim)
all_sprites.add(orbes)
all_orbs.add(orbes)

score = 0

# ====== LOOP PRINCIPAL =====
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
            if event.key == pygame.K_LEFT and player.speedx != 6:
                player.speedx = -6
                player.speedy = 0
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
        score += 50
        if hits[0] == apple:
            apple = Fruit(maca)
            all_fruits.add(apple)
            all_sprites.add(apple)
        else:
            cherry = Fruit(cereja)
            all_fruits.add(cherry)
            all_sprites.add(cherry)


    # ---- Gera Saídas:
    window.fill ((0,0,0))                   # preenche a tela com a cor preta
    #window.blit (background, (0, 0))        # insere imagem background
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



# ===== FINALIZAÇÃO =====
pygame.quit()