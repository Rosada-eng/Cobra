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
bixinho_WIDTH = 30
bixinho_HEIGHT = 30

# ----- Carrega os Assets:
background = pygame.image.load ('assets/img/terra_solo.jpg').convert()
background = pygame.transform.scale (background, (WIDTH, HEIGHT))
bixinho = pygame.image.load ('assets/img/lindwurm.png').convert_alpha()
bixinho = pygame.transform.scale (bixinho, (bixinho_WIDTH, bixinho_HEIGHT))



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
        self.speedy = 0

    def update(self):
        # Atualiza a posição da cobrinha:
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #limita posições em que pode andar:
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <0:
            self.rect.top =0


# ----- Criando objetos:
player = Snake(bixinho)
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
            if event.key == pygame.K_LEFT:
                player.speedx -= 8
            if event.key == pygame.K_RIGHT:
                player.speedx += 8
            if event.key == pygame.K_UP:
                player.speedy -= 8
            if event.key == pygame.K_DOWN:
                player.speedy += 8
            
        # SOLTAR A TECLA
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speedx += 8
            if event.key == pygame.K_RIGHT:
                player.speedx -= 8
            if event.key == pygame.K_UP:
                player.speedy += 8
            if event.key == pygame.K_DOWN:
                player.speedy -= 8

    # ----- Atualiza estado do jogo
    # Atualizando posição do Player
    player.update()
            

            



    # ---- Gera Saídas:
    window.fill ((0,0,0)) #preenche a tela com a cor preta
    window.blit (player.image, player.rect)
    
    # Desenha os objetos:
    

    #Atualiza o Frame
    pygame.display.update()






# ===== FINALIZAÇÃO =====
pygame.quit()

