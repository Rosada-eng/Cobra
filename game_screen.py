import pygame
from sprites import Snake, Snake_Body, Fruit, Orbe, Life
from assets import load_assets, SCORE_FONT
from config import FPS, Black, WIDTH, HEIGHT

def game_screen(window):
    # Carrega os assets
    assets = load_assets()

    # ----- Cria grupos de sprite
    all_sprites = pygame.sprite.Group()
    all_fruits = pygame.sprite.Group()
    all_orbs = pygame.sprite.Group()
    snake_body = pygame.sprite.Group()

    # ----- Cria jogador e o adiciona nos grupos:
    player = Snake(assets)
    all_sprites.add(player)
    snake_body.add(player)
    ultima_parte = player # Guarda última parte criada para a cobrinha

    # ----- Cria frutas e as adiciona nos grupos
    apple = Fruit(assets)
    #cherry = Fruit(assets)
    for i in range (2):
        all_fruits.add(apple)
        all_sprites.add(apple)
        #all_fruits.add(cherry)
        #all_sprites.add(cherry)

    # ----- Cria barra de vida e a adiciona em all_sprites
    vida = 10
    barra_vida = Life(assets, vida)
    all_sprites.add(barra_vida)

    # ----- Cria orbs e adiciona nos sprites
    orbes = Orbe(assets)
    all_sprites.add(orbes)
    all_orbs.add(orbes)


    score = 0
    colisao = 0
    delay_orbe = 30000 #30 seg 
    clock = pygame.time.Clock()

    game = True
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
            nova_parte = Snake_Body(assets, ultima_parte)
            all_sprites.add(nova_parte)
            snake_body.add(nova_parte)
            # Atualiza última parte 
            ultima_parte = nova_parte

            score += 50
            if hits[0] == apple:
                apple = Fruit(assets)
                all_fruits.add(apple)
                all_sprites.add(apple)
            else:
                cherry = Fruit(assets)
                all_fruits.add(cherry)
                all_sprites.add(cherry)

        # Verifica se houve colisão com o orbe
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
                orbes = Orbe(assets)
                all_orbs.add(orbes)
                all_sprites.add(orbes)
                colisao = 0
    

        # ---- Gera Saídas:
        window.fill (Black)  # preenche a tela com a cor preta
    
        # Desenha os objetos:
        window.blit (player.image, player.rect) # insere imagem player

        # Desenha o placar
        text_surface = assets[SCORE_FONT].render ("{:08d}".format(score), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH/2, 10)
        window.blit (text_surface, text_rect)

        all_sprites.draw(window)

        # Atualiza o Frame
        pygame.display.update()