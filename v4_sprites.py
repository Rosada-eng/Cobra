import pygame
import pytmx
from random import *
from v4_config import *
from math import pi, sin
vect = pygame.math.Vector2

# ------------ COBRA ------------
class Snake(pygame.sprite.Sprite):
    def __init__ (self, jogo, img, x, y): #será criado no proprio objeto 'jogo'
        # Construtor da classe mãe:
        self._layer = LAYERS['PLAYER']
        self.groups = jogo.all_sprites  
        pygame.sprite.Sprite.__init__(self, self.groups)
        # --- Atributos Player ---
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.max_stamine = PLAYER_MAX_STAMINE
        self.player_vision = PLAYER_VISION
        self.snake_width = SNAKE_WIDTH
        self.snake_height = SNAKE_HEIGHT
        # LEVEL UP:
        self.next_level_xp = 1000
        self.current_xp = 0
        # Atributos da Fruta 
        self.fruit_xp = 20
        self.fruit_stamine = 10
        # Condições do
        # configurações gerais do sprite
        self.jogo = jogo       
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x + self.snake_width/2 ,y + self.snake_height/2)
        self.posic = vect (x, y) #declara as posições (x,y) em que o player será spawnado
        self.veloc = vect (0, 0) # Começa com velocidade zero 
        self.dir = vect (1, 0) # começa virado pra direita
        self.stamine = 0 # Stamina inicial
        self.last_update = pygame.time.get_ticks()
        self.snake_count = 0
        self.charge = VENENO_CHARGE
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        self.last_shoot = 0 # no começo, não houve disparos
        self.last_dir = self.dir
        # configurações para o ataque
        self.ATACK = False
        self.last_atack = 0
        #self.current_position = vect (0,0)
        self.target = 0 # variável que guardará quem é o target mais próximo
        self.to_target = vect (0,0)
        self.dist_to_target = 0
        self.count_step = 0
        self.INGRASS = False
        self.last_hit = 0 # último hit do pássaro na cobra
        self.ANALISE = True # analisa múltiplos hits do pássaro na cobra
        self.score = 0
        
        
    def get_keys(self):
        self.veloc = vect (0, 0)
        self.interactive_objects()
        CHANCE = 0.005
        keys = pygame.key.get_pressed() #Salva uma dicionario de keys q estão sendo pressionadas
        if keys[pygame.K_LEFT]:
            self.veloc.x = -self.speed
            self.dir = vect (-1, 0)
            self.LEFT = True
            self.RIGHT = False
            self.UP = False
            self.DOWN = False
            if self.INGRASS:
                if random() < CHANCE:
                    channel2 = self.jogo.sound_effects['1step_grass'].play() 
                    """ configurar para não repetir tantas vezes """
        elif keys[pygame.K_RIGHT]:
            self.veloc.x = self.speed
            self.dir = vect (1, 0)
            self.LEFT = False
            self.RIGHT = True
            self.UP = False
            self.DOWN = False
            if self.INGRASS:
                if random() < CHANCE:
                    channel2 = self.jogo.sound_effects['1step_grass'].play()
        elif keys[pygame.K_UP]:
            self.veloc.y = -self.speed
            self.dir = vect (0, -1)
            self.LEFT = False
            self.RIGHT = False
            self.UP = True
            self.DOWN = False
            if self.INGRASS:
                if random() < CHANCE:
                    channel2 = self.jogo.sound_effects['1step_grass'].play()
        elif keys[pygame.K_DOWN]:
            self.veloc.y = self.speed
            self.dir = vect (0, 1)
            self.LEFT = False
            self.RIGHT = False
            self.UP = False
            self.DOWN = True
            if self.INGRASS:
                if random() < CHANCE:
                    channel2 = self.jogo.sound_effects['1step_grass'].play()
        else:
            self.UP = False
            self.DOWN = False
            self.LEFT = False
            self.RIGHT = False
        self.last_dir = self.dir # guarda última direção
        # Configura disparo do veneno
        if keys[pygame.K_SPACE]:
            now_time = pygame.time.get_ticks() # grava instante atual           
            if now_time - self.last_shoot > VENENO_FREQUENCY:
                self.last_shoot = now_time # se passou tempo mínimo, grava novo 'último tiro'
                self.charge = 0
                # Ajusta posição do disparo dependendo da movimentação que a cobra tava
                if self.LEFT:
                    pos = self.posic + VENENO_DESLOC_LEFT
                elif self.RIGHT:
                    pos = self.posic + VENENO_DESLOC_RIGHT
                elif self.UP:
                    pos = self.posic + VENENO_DESLOC_UP
                elif self.DOWN:
                    pos = self.posic + VENENO_DESLOC_DOWN
                else:
                    # Ajusta posição do tiro quando a cobra tava parada
                    if self.last_dir == vect (1, 0):
                        pos = self.posic + VENENO_DESLOC_RIGHT            
                    elif self.last_dir == vect (-1, 0):
                        pos = self.posic + VENENO_DESLOC_LEFT            
                    elif self.last_dir == vect (0, -1):
                        pos = self.posic + VENENO_DESLOC_UP            
                    else: 
                        pos = self.posic + VENENO_DESLOC_DOWN            
                dir = self.last_dir  
                # Posição do tiro: tem que ajustar à boca da cobra quando anda na horizontal
                Veneno (self.jogo, pos, dir)
                # Pequeno impulso para trás do disparo
                self.vel = vect (-KICKBACK, 0)

        if keys[pygame.K_x]:
            # checa distância entre Player e a Presa:
            to_target_1 = vect (self.jogo.presa1.posic.x - self.posic.x, self.jogo.presa1.posic.y - self.posic.y) # vetor Distância inicial p/ Presa 1
            to_target_2 = vect (self.jogo.presa2.posic.x - self.posic.x, self.jogo.presa2.posic.y - self.posic.y) # vetor Distância inicial p/ Presa 2
            to_target_3 = vect (self.jogo.presa3.posic.x - self.posic.x, self.jogo.presa3.posic.y - self.posic.y) # vetor Distância inicial p/ Presa 3

            dist_to_target_1 = to_target_1.magnitude() # distância inicial (em pixels) entre Player e Presa 1
            dist_to_target_2 = to_target_2.magnitude() # distância inicial (em pixels) entre Player e Presa 2
            dist_to_target_3 = to_target_3.magnitude() # distância inicial (em pixels) entre Player e Presa 3
            
            if dist_to_target_1 <= ATACK_RANGE and self.jogo.presa1.alive and self.stamine == PLAYER_MAX_STAMINE: 
                self.last_atack = pygame.time.get_ticks()
                #self.current_position = vect(self.posic.x, self.posic.y) # guarda a posição inicial antes de dar o bote
                self.ATACK = True # executa a animação de ataque qnd rodar o update
                self.target = self.jogo.presa1
                self.score += GUAXI_SCORE

            elif dist_to_target_2 <= ATACK_RANGE and self.jogo.presa2.alive and self.stamine == PLAYER_MAX_STAMINE : 
                self.last_atack = pygame.time.get_ticks()
                #self.current_position = vect(self.posic.x, self.posic.y) # guarda a posição inicial antes de dar o bote
                self.ATACK = True # executa a animação de ataque qnd rodar o update
                self.target = self.jogo.presa2
                self.score += GUAXI_SCORE

            elif dist_to_target_3 <= ATACK_RANGE and self.jogo.presa3.alive and self.stamine == PLAYER_MAX_STAMINE: 
                self.last_atack = pygame.time.get_ticks()
                #self.current_position = vect(self.posic.x, self.posic.y) # guarda a posição inicial antes de dar o bote
                self.ATACK = True # executa a animação de ataque qnd rodar o update
                self.target = self.jogo.presa3
                self.score += GUAXI_SCORE

    def collide_with_walls (self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False) # retorna uma lista com os elementos do grupo q colidiram
            if hits:
                if self.veloc.x >0:
                    self.posic.x = hits[0].rect.left - self.rect.width
                if self.veloc.x <0:
                    self.posic.x = hits[0].rect.right
                self.veloc.x = 0
                self.rect.x = self.posic.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide (self, self.jogo.walls, False)
            if hits:
                if self.veloc.y >0:
                    self.posic.y = hits[0].rect.top - self.rect.height
                if self.veloc.y <0:
                    self.posic.y = hits[0].rect.bottom
                self.veloc.y = 0
                self.rect.y = self.posic.y  

    def interactive_objects (self):
        # -- Analisa configurações de mato para esconder player e mudar sua velocidade
        hits = pygame.sprite.spritecollide (self, self.jogo.mato_grosso, False) # retorna uma lista com os elementos do grupo q colidiram
        if hits:
            self.speed = 0.7*PLAYER_SPEED
            self.INGRASS = True
        else:
            self.speed = 1.0*PLAYER_SPEED
            self.INGRASS = False

    def update(self):
        self.get_keys()
        if self.ATACK and self.stamine >= 0.8*SNAKE_MAX_STAMINE:
            number_frames = 5 # numero de frames p/ animar o bote
            self.to_target = vect (self.target.posic.x - self.posic.x, self.target.posic.y - self.posic.y)
            move_step = self.to_target / number_frames 
            
            
            now = pygame.time.get_ticks()
            delta_t = now - self.last_atack       
            if delta_t > 30:
                self.posic.x += move_step.x
                self.posic.y += move_step.y
                self.rect.center = (self.posic.x, self.posic.y)
                self.count_step +=1
                self.last_atack = now      
                if self.count_step >= number_frames:
                    self.target.kill()
                    channel1 = self.jogo.sound_effects['bite1'].play() 
                    channel1.queue(self.jogo.sound_effects['bite2'])  
                    channel1.queue(self.jogo.sound_effects['bite3']) 
                    self.count_step = 0
                    self.ATACK = False
                    self.target.alive = False

                    ## Consome STAMINA
                    self.stamine -= 0.8* self.stamine
                    ## Adiciona tempo
                    self.jogo.tempo_fase += 30*1000
                    # Adiciona XP:
                    self.current_xp += 300
    
        else:
            self.posic.x += self.veloc.x * dt #delta X = vx*deltaT
            self.posic.y += self.veloc.y * dt #delta Y = vy*deltaT
            #obs.1: Usar dt garante que o personagem ande proporcionalmente à velocidade de processamento da maquina
            self.rect.x = self.posic.x
            self.collide_with_walls ('x') #checa condições de colisao em X
            self.rect.y = self.posic.y
            self.collide_with_walls('y') #checa condições de colisao em Y

            now = pygame.time.get_ticks()
            delta_t = now - self.last_update   
            self.charge = (now - self.last_shoot)/VENENO_DURATION * VENENO_CHARGE
            if self.charge > VENENO_CHARGE:
                self.charge = VENENO_CHARGE

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

        # --- Player colide com a frutas:
        hits = pygame.sprite.spritecollide (self, self.jogo.fruits, False, pygame.sprite.collide_mask)
        for hit in hits:
            self.jogo.sound_effects['pick_fruit'].play()
            self.current_xp += 200
            self.stamine += self.fruit_stamine
            print(self.current_xp/self.next_level_xp)
            
            hit.kill()
            # aumenta stamina e score
            self.stamine += FRUTAS_STAMINA
            self.score += FRUIT_SCORE
            if self.stamine > SNAKE_MAX_STAMINE:
                self.stamine = SNAKE_MAX_STAMINE

         # --- Player colide com pássaros
        now = pygame.time.get_ticks()
        delay = now - self.last_hit
        if delay > 2000:
            self.ANALISE = True
        if self.ANALISE and not self.INGRASS:
            hits = pygame.sprite.spritecollide (self, self.jogo.crazy_birds, False, pygame.sprite.collide_mask)           
            self.last_hit = pygame.time.get_ticks()   
            # Se colidiu, trava colisão por delay=2s para evitar múltiplas colisões num único instante    
            for hit in hits:
                self.ANALISE = False
                self.health -= BIRD_DAMAGE
                self.jogo.sound_effects['hit'].play()
                hit.speed = vect (0, 0)
                if self.health <= 0:
                    self.playing = False


                    """ Arrumar para adequar o código de baixo para o Sprite"""
            # if hits:
            #     self.player.posic += vect (BIRD_KNOCKBACK, 0).rotate(90)

        # hits = pygame.sprite.groupcollide(self.veneno, self.crazy_birds, True, True, pygame.sprite.collide_mask)
        # for hit in hits:
        #     self.player.stamine += 10
        

        # --- PLayer colide com pássaros
        # hits = pygame.sprite.spritecollide (self.player, self.birds, False)
        # for hit in hits:
        #     self.player.health -= BIRD_DAMAGE
        #     hit.speed = vect (0, 0)
        #     if self.player.health <= 0:
        #         self.playing = False
        # if hits:
        #     self.player.posic += vect (BIRD_KNOCKBACK, 0).rotate(-hits[0].angulo)
                
    def level_up(self):
        if self.current_xp >= self.next_level_xp:
            self.speed *= 1.2
            self.health *= 1.1
            self.max_stamine *= 1.4
            self.player_vision *= 1.2
            self.snake_width *= 1.2
            self.snake_height *= 1.2

            self.fruit_stamine *= 2
            self.fruit_xp *= 2

            self.next_level_xp *= 1.8



# ------------ VENENO DA COBRA ------------
class Veneno (pygame.sprite.Sprite):
    def __init__ (self, jogo, pos, dir): # recebe posição e direção do player
        self.groups = jogo.all_sprites, jogo.veneno
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = jogo.veneno_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.hit_rect = VENENO_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.posic = vect (pos) # corrige erro da cobra e disparo atualizarem com mesma posição
        self.rect.center = self.posic
        spread = uniform (-VENENO_DESVIO, VENENO_DESVIO)
        self.veloc = dir.rotate(spread) * VENENO_SPEED # pequeno desvio vetor velocidade
        self.spawn_time = pygame.time.get_ticks() # instante que foi criado

    def update (self):
        self.posic += self.veloc * dt
        self.rect.center = self.posic
        self.hit_rect.center = self.rect.center
        if pygame.sprite.spritecollideany(self, self.jogo.walls):
            self.kill() # se colide com parede, já era
        self.time_now = pygame.time.get_ticks()

        if self.time_now - self.spawn_time > VENENO_DURATION:
            self.kill() # vida útil do disparo


# ------------ PÁSSARO ------------
# class Bird (pygame.sprite.Sprite):
#     def __init__ (self, jogo, x, y):
#         self.groups = jogo.all_sprites, jogo.birds
#         pygame.sprite.Sprite.__init__(self, self.groups)
#         self.jogo = jogo
#         self.image = jogo.bird_img
#         self.rect = self.image.get_rect()
#         self.hit_rect = BIRD_HIT_RECT.copy() # faz cópia do ret. de col. pra cada pássaro
#         self.hit_rect.center = self.rect.center
#         self.posic = vect (x, y) # pos. inicial
#         self.veloc = vect (0, 0) # vel. inicial
#         self.acel = vect (0, 0) # acel. inicial
#         self.rect.center = self.posic
#         self.angulo = 0 # rotação inicial
#         #self.health = BIRD_HEALTH
#         self.speed = choice(BIRD_SPEEDS)
#         self.last_update = pygame.time.get_ticks()
#         self.bird_count = 0


#     def dist_birds (self): # distância entre pássaros
#         for bird in self.jogo.birds:
#             if bird != self:
#                 # mede distância
#                 dist = self.posic - bird.posic
#                 # Se está dentro do círculo, gera aceleração de repulsão
#                 if 0 < dist.length() < BIRD_ZONE:
#                     self.acel += dist.normalize()

#     def update (self):
#         # -- rotação --
#         if self.jogo.player.posic != self.posic:
#             self.angulo = (self.jogo.player.posic - self.posic).angle_to(vect(1, 0)) # subtração de vetores: pássaro sempre aponta pro player
#         else:
#             self.angulo = 0
#         self.image = pygame.transform.rotate (self.jogo.bird_img, self.angulo) # gira imagem no ângulo acima
#         # -- vetores --
#         self.rect.center = self.posic
#         self.acel = vect (1, 0).rotate(-self.angulo) # declara aceleração de modulo unitario
#         self.dist_birds() # verifica distância de outros pássaros para ajustar a acel.
#         self.acel.scale_to_length(choice(BIRD_SPEEDS))
#         self.acel += self.veloc * (-1) # limita velocidade máxima
#         self.veloc += self.acel * dt
#         self.posic += self.veloc * dt + 0.5*self.acel*dt**2 # s = s0 + v*t + (1/2)*a*t**2
        # -- colisão com barreiras (não tem)
        # -- Saúde --
        # if self.health <= 0:
        #     self.kill()

        # -- Animação --
        #now = pygame.time.get_ticks()
        #delta_t = now - self.last_update
        #self.image = self.jogo.owl_up['U{}.png'.format(self.bird_count)]
        #if delta_t > 150:
        #    delta_t = 0
        #    self.last_update = now
        #    self.bird_count += 1
        #    if self.bird_count >2:
        #        self.bird_count = 0


    # def draw_life_bar (self):
    #     # -- Configura cor --
    #     if self.health > 75 * BIRD_HEALTH / 100: # 75%
    #         color = GREEN
    #     elif self.health > 50 * BIRD_HEALTH / 100: # 50%
    #         color = YELLOW
    #     elif self.health > 25 * BIRD_HEALTH / 100: # 25%
    #         color = ORANGE
    #     else: 
    #         color = RED
    #     # -- Configura retângulo --
    #     width_bar = int (self.rect.width * self.health / BIRD_HEALTH) # tamanho da barra proporcional à vida
    #     self.health_bar = pygame.Rect (0, 0, width_bar, 6)
    #     # Só desenha barra quando leva primeiro dano
    #     if self.health < BIRD_HEALTH:
    #         pygame.draw.rect (self.image, color, self.health_bar)


# ------------ PRESAS ------------
class Prey (pygame.sprite.Sprite):
    def __init__(self, jogo, img, x,y):
        self.groups = jogo.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.rect = self.image.get_rect()
        self.hit_rect = GUAXI_HIT_RECT.copy() # PRECISA DESSE?
        self.hit_rect.center = self.rect.center
        self.posic = vect(x, y) # pos. de spawn
        self.rect.center = self.posic
        self.dir = vect(1,0) # Versor da velocidade
        self.speed = GUAXI_SPEED
        self.veloc = self.dir * self.speed
        self.alive = True

        self.last_position = vect(x,y) # Ou trabalha com distancia ou com tempo
        self.distance = vect(0,0) # distância que percorre antes de mudar de direção
        # variáveis p/ guardar direção de movimento p/ animação
        self.RIGHT = False
        self.LEFT = False
        self.UP = False
        self.DOWN = False
        self.last_update = pygame.time.get_ticks()
        self.guaxi_count = 0


    def update(self):
        now = pygame.time.get_ticks()
        delta_t = now - self.last_update
        if self.jogo.player.ATACK:
            self.veloc = (0,0)
            #self.kill() -- está configurado no ataque
            
        else:
            self.veloc = self.dir * self.speed
            self.posic += self.veloc * dt
            self.rect.center = self.posic
            distance = self.posic - self.last_position
            D = distance.length()
            if D >= 4*32:
                self.dir = self.dir.rotate(90)
                self.veloc = self.dir * self.speed
                self.last_position = (self.posic.x, self.posic.y)
                D = 0

            if self.dir == (1,0): #movendo para direita
                self.image = self.jogo.guaxi_right['R{}.png'.format(self.guaxi_count)]
                if delta_t > 150:
                    delta_t = 0
                    self.last_update = now
                    self.guaxi_count += 1
                    if self.guaxi_count > 2:
                        self.guaxi_count = 0
            
            elif self.dir == (-1,0): #movendo para esquerda
                self.image = self.jogo.guaxi_left['L{}.png'.format(self.guaxi_count)]
                if delta_t > 150:
                    delta_t = 0
                    self.last_update = now
                    self.guaxi_count += 1
                    if self.guaxi_count > 2:
                        self.guaxi_count = 0
            
            elif self.dir == (0,1): # movendo para baixo
                self.image = self.jogo.guaxi_down['D{}.png'.format(self.guaxi_count)]
                if delta_t > 150:
                    delta_t = 0
                    self.last_update = now
                    self.guaxi_count += 1
                    if self.guaxi_count > 2:
                        self.guaxi_count = 0
            
            elif self.dir == (0,-1):  #movendo para cima
                self.image = self.jogo.guaxi_up['U{}.png'.format(self.guaxi_count)]
                if delta_t > 150:
                    delta_t = 0
                    self.last_update = now
                    self.guaxi_count += 1
                    if self.guaxi_count > 2:
                        self.guaxi_count = 0
    
    #def kill_prey(self):
        
        
# ------------ FRUTA ------------
class Fruit(pygame.sprite.Sprite):
    def __init__(self, jogo, img, x, y):
        self.groups = jogo.all_sprites, jogo.fruits
        self._layer = LAYERS['FRUIT']
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.image = pygame.transform.scale(self.image, (OBJECT_WIDTH, OBJECT_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = vect (x, y)
        self.rect.center = self.pos
        self.y_0 = self.pos.y
        self.last_update = pygame.time.get_ticks() # referência para fazer o efeito de movimentação da fruta
        self.t = 0
        self.phi_0 = 2*pi / (randint (1,5)) #phi_inicial: Porção de uma volta.
        self.argumento = 0
   
    def update(self):        
        now = pygame.time.get_ticks()
        delta_t = now - self.last_update # análise do tempo p/ criar efeito da fruta
        self.argumento = (OMEGA * delta_t + self.phi_0) 
        if delta_t > T:
            delta_t = 0  
            self.last_update = now              
        self.pos.y = self.y_0 + A*sin(self.argumento)
        self.rect.center = self.pos

        delta_respawn = now - self.jogo.last_spawn
        if delta_respawn >= 90000: # respawn de 1,5 min:
            self.jogo.respawn('fruit')
            



# ------------ ORBE ------------  
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
        self.rect.x = randint(0, WIDTH - (OBJECT_WIDTH + 50))
        self.rect.y = randint(0, HEIGHT - (OBJECT_HEIGHT + 50))
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


# ------------ OBSTÁCULO ------------
class Object (pygame.sprite.Sprite):
    def __init__(self, jogo, x,y, width, height, type):
        self.type = type
        if self.type == 'WALL':
            self.groups = jogo.walls
        if self.type == 'MATO':
            self.groups = jogo.mato_grosso
        if self.type == 'DETECT':
            self.groups = jogo.detect_prey
        self._layer = LAYERS[type]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


# ------------ CÂMERA ------------
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


# ------------ MAPA ------------
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


# ------------ PÁSSAROS ------------
class CrazyBirds(pygame.sprite.Sprite):
    def __init__ (self, jogo, img, x, y, vx, vy):
        self._layer = LAYERS['BIRD']
        self.groups = jogo.all_sprites, jogo.crazy_birds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.posic = vect (x, y)
        self.hit_rect = BIRD_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.speed = vect (vx, vy)
        self.vx = vx
        self.vy = vy
        self.acel = vect (self.vx/10, self.vy/10) # acel. pra quando colidir com player
        self.rect.center = self.posic
        self.last_update = pygame.time.get_ticks()
        self.bird_horizon_count = 0 # contador para troca de imagens

    def update (self):
        
        self.posic += self.speed * dt
        self.rect.center = self.posic
        self.hit_rect.center = self.rect.center
        # Verifica se os que vão pra direita já atravessaram o mapa
        if self.posic.x > self.jogo.map.width and self.vx > 0:
            self.posic.x = -30
            self.posic.y = randint (OBJECT_HEIGHT, self.jogo.map.height - OBJECT_HEIGHT)
        # Verifica se os que vão pra esquerda já atravessaram o mapa
        if self.posic.x < - OBJECT_WIDTH and self.vx < 0:
            self.posic.x = self.jogo.map.width + 30
            self.posic.y =  randint (OBJECT_HEIGHT, self.jogo.map.height - OBJECT_HEIGHT)
        # Verifica se os que vão pra cima já atravessaram o mapa
        if self.posic.y < - OBJECT_HEIGHT and self.vy < 0:
            self.posic.y = self.jogo.map.height + 30
            self.posic.x =  randint (OBJECT_WIDTH, self.jogo.map.width - OBJECT_WIDTH)
        # Verifica se os que vão pra baixo já atravessaram o mapa
        if (self.posic.y > OBJECT_HEIGHT + self.jogo.map.height) and self.vy > 0:
            self.posic.y = - 30
            self.posic.x =  randint (OBJECT_WIDTH, self.jogo.map.width - OBJECT_WIDTH)

        now = pygame.time.get_ticks()
        delta_t = now - self.last_update
        # Se passou o tempo, troca de imagem
        if delta_t > 150:
            delta_t = 0
            self.last_update = now
            self.bird_horizon_count += 1
            if self.bird_horizon_count > 3:
                self.bird_horizon_count = 0
        # Carrega imagem dos que vão pra direita
        if self.vx > 0:
            self.image = self.jogo.bird_right_img['right00{}.png'.format(self.bird_horizon_count)]
        # Carrega imagem dos que vão pra esquerda
        elif self.vx < 0:
            self.image = self.jogo.bird_left_img['left00{}.png'.format(self.bird_horizon_count)]
        else:
            # Carrega imagem dos que vão pra baixo
            if self.vy > 0:
                self.image = self.jogo.bird_down_img['down00{}.png'.format(self.bird_horizon_count)]
            # Carrega imagem dos que vão pra cima
            elif self.vy < 0:
                self.image = self.jogo.bird_up_img['up00{}.png'.format(self.bird_horizon_count)]

        # Acelera pássaro novamente após colisão com player
        if abs(self.speed.x) < abs(self.vx):
            self.speed.x += self.acel.x * dt
            self.posic.x += self.speed.x * dt
            self.rect.center = self.posic
            self.hit_rect.center = self.rect.center
        if abs(self.speed.y) < abs(self.vy):
            self.speed.y += self.acel.y * dt
            self.posic.y += self.speed.y * dt
            self.rect.center = self.posic
            self.hit_rect.center = self.rect.center

