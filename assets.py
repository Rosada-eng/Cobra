import pygame
import os
from config import snake_WIDTH, snake_HEIGHT, object_WIDTH, object_HEIGHT, Img_DIR, Song_DIR, Font_DIR

#BACKGROUND = 'background'
SNAKE_HEAD_IMG = 'snake_head_img'
SNAKE_BODY_IMG = 'snake_body_img'
APPLE_IMG = 'apple_img'
CHERRY_IMG = 'cherry_img'
ORBS_ANIM = 'orbs_anim'
HEALTH_BARR = 'health_barr'
SCORE_FONT = 'score_font'

def load_assets():
    assets = {}
    assets[SNAKE_HEAD_IMG] = pygame.image.load(os.path.join(Img_DIR, 'head_img.png')).convert_alpha()
    assets[SNAKE_HEAD_IMG] = pygame.transform.scale(assets['snake_head_img'], (snake_WIDTH, snake_HEIGHT))
    assets[SNAKE_BODY_IMG] = pygame.image.load(os.path.join(Img_DIR, 'body1_img.png')).convert_alpha()
    assets[SNAKE_BODY_IMG] = pygame.transform.scale(assets['snake_body_img'], (snake_WIDTH, snake_HEIGHT))
    assets[APPLE_IMG] = pygame.image.load(os.path.join(Img_DIR, 'maca.png')).convert_alpha()
    assets[APPLE_IMG] = pygame.transform.scale(assets['apple_img'], (object_WIDTH, object_HEIGHT))
    assets[CHERRY_IMG] = pygame.image.load(os.path.join(Img_DIR, 'cereja.png')).convert_alpha()
    assets[CHERRY_IMG] = pygame.transform.scale(assets['cherry_img'], (object_WIDTH, object_HEIGHT))

    # Carrega orbs para animação
    orbs_anim = []
    for i in range(1, 6):
        nome_arquivo = os.path.join(Img_DIR, 'orb{}.png'.format(i))
        img = pygame.image.load(nome_arquivo).convert_alpha()
        img = pygame.transform.scale (img, (object_WIDTH, object_HEIGHT))
        orbs_anim.append(img)
    assets[ORBS_ANIM] = orbs_anim

    # Carrega imagens da barra de vida
    health_barr = []
    for i in range(0, 21):
        nome_arquivo = 'assets/img/health/VIDA_{0}.png'.format(i)
        img = pygame.image.load(nome_arquivo).convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width()/2), int(img.get_height()/2)))
        health_barr.append(img)
    assets[HEALTH_BARR] = health_barr

    # Carrega fonte (colocar fontes específicas que serão usadas)
    assets[SCORE_FONT] = pygame.font.Font(os.path.join(Font_DIR, 'PressStart2P.ttf'), 28)

    # Carrega sons do jogo
    
    return assets

# Mudar assets das frutas para lista e adicionar mais opções