import pygame
from os import path
from v3_config import snake_WIDTH, snake_HEIGHT, object_WIDTH, object_HEIGHT, img_DIR, song_DIR, font_DIR

#SNAKE_HEAD_IMG = 'snake_head_img'
#SNAKE_BODY_IMG = 'snake_body_img'
#APPLE_IMG = 'apple_img'
#CHERRY_IMG = 'cherry_img'
#ORBS_ANIM = 'orbs_anim'
#HEALTH_BARR = 'health_barr'
#SCORE_font = 'score_font'


class Assets (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_assets()
    
    def load_assets(self):
        # Carrega as imagens necessárias
        self.SNAKE_HEAD_IMG = pygame.image.load(path.join(img_DIR, 'head_img.png')).convert_alpha()
        self.SNAKE_HEAD_IMG = pygame.transform.scale(SNAKE_HEAD_IMG, (snake_WIDTH, snake_HEIGHT))
        self.SNAKE_BODY_IMG = pygame.image.load(path.join(img_DIR, 'body1_img.png')).convert_alpha()
        self.SNAKE_BODY_IMG = pygame.transform.scale(SNAKE_BODY_IMG, (snake_WIDTH, snake_HEIGHT))
        self.APPLE_IMG = pygame.image.load(path.join(img_DIR, 'maca.png')).convert_alpha()
        self.APPLE_IMG = pygame.transform.scale(APPLE_IMG, (object_WIDTH, object_HEIGHT))
        self.CHERRY_IMG = pygame.image.load(path.join(img_DIR, 'cereja.png')).convert_alpha()
        self.CHERRY_IMG = pygame.transform.scale(CHERRY_IMG, (object_WIDTH, object_HEIGHT))

        # Carrega orbs para animação
        orbs_anim = []
        for i in range(1, 6):
            nome_arquivo = path.join(img_DIR, 'orb{}.png'.format(i))
            img = pygame.image.load(nome_arquivo).convert_alpha()
            img = pygame.transform.scale (img, (object_WIDTH, object_HEIGHT))
            orbs_anim.append(img)
        self.ORBS_ANIM = orbs_anim

        # Carrega imagens da barra de vida
        health_barr = []
        for i in range(0, 21):
            nome_arquivo = 'assets/img/health/VIDA_{0}.png'.format(i)
            img = pygame.image.load(nome_arquivo).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()/2), int(img.get_height()/2)))
            health_barr.append(img)
        self.HEALTH_BARR = health_barr

        # Carrega fonte (colocar fontes específicas que serão usadas)
        self.SCORE_font = pygame.font.Font(path.join(font_DIR, 'PressStart2P.ttf'), 28)

        # Carrega sons do jogo
        # -- criar outra class
        
assets = Assets()


# Mudar assets das frutas para lista e adicionar mais opções