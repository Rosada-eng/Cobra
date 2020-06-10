import pygame
vect = pygame.math.Vector2

A = vect (3,4)
B = vect (1,1)

dir = vect (1,0)
e = dir.rotate_ip(-90)


print (e)