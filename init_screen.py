import random
import pygame
from os import path
from config import Img_DIR, Black, GAME, QUIT, FPS

def init_screen(screen):
    # Configura velocidade
    clock = pygame.time.Clock()

    # Carrega a tela de fundo
    background = pygame.image.load(path.join(Img_DIR, 'init_teste.png')).convert()
    background_rect = background.get_rect()

    running = True
    while running:
        # Configura a velocidade do jogo
        clock.tick(FPS)

        # Analisa eventos
        for event in pygame.event.get():
            # Analisa se o jogo foi fechado
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            # Analisa se alguma tecla foi pressionada (se sim, jogo começa de verdade)
            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # Redesenha a cada loop
        screen.fill(Black) # Pinta fundo de preto
        screen.blit(background, background_rect) # Desenha imagem de fundo

        # Inverte o display
        pygame.display.flip()

    return state