import pygame 
from pygame.locals import K_a,K_d
import sys

ANCHO = 600
ALTURA = 800

pygame.init()#Se inicializa pygame
                                #Altura#Ancho
screen = pygame.display.set_mode((ALTURA,ANCHO))#La ventana
pygame.display.set_caption("GAME 0.1")#Titulo que aparece en la ventana

##########################################PERSONAJES############################################################
hit_box_eje_x = 80
hit_box_eje_y = 420
#Funcion que se va a encargar de dibujar
def draw_hit_box():
                                    #X #Y #Altur#Ancho
    pygame.draw.rect(screen,(255,255,0),(hit_box_eje_x,hit_box_eje_y,20,60))

################################################################################################################

fps = pygame.time.Clock()

#########################BUCLE PRINCIPAL#############################
running = True
while running:
    
    screen.fill((0,0,0))
    fps.tick(60) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Re-dibuja el cuadrado
        pressed_keys = pygame.key.get_pressed()
        if True in pressed_keys:
            if pressed_keys [K_a]:
                if hit_box_eje_x > 0:
                    hit_box_eje_x -= 5#se movera a la izquierda
                    draw_hit_box()
            if pressed_keys [K_d]:
                if hit_box_eje_x < 800:
                    hit_box_eje_x += 5#se movera a la derecha
                    draw_hit_box()




    pygame.display.flip() #Muestra los cambios

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(404) #se usa para indicar si el programa terminó con éxito o con un error (404)