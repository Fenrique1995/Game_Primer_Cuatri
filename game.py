import pygame 
from pygame.locals import K_a,K_d,K_SPACE, K_RETURN
import sys

ANCHO = 600
ALTURA = 800

pygame.init()#Se inicializa pygame
                                #Altura#Ancho
screen = pygame.display.set_mode((ALTURA,ANCHO))#La ventana
pygame.display.set_caption("GAME 0.1")#Titulo que aparece en la ventana

background_image_0 = pygame.image.load("Img/parallax_forest_pack/layers/parallax-forest-back-trees.png")
background_image_1 = pygame.image.load("Img/parallax_forest_pack/layers/parallax-forest-front-trees.png")
background_image_transform_0 = pygame.transform.scale(background_image_0, (ALTURA,ANCHO))
background_image_transform_1 = pygame.transform.scale(background_image_1, (ALTURA,ANCHO))
##########################################PERSONAJES############################################################
hit_box_eje_x = 80
hit_box_eje_y = 465
is_jumping = False
jump_count = 10
#Funcion que se va a encargar de dibujar
def draw_hit_box():
                                            #X              #Y    #Ancho#Altura
    pygame.draw.rect(screen,(255,255,0),(hit_box_eje_x,hit_box_eje_y,20,60))

################################################################################################################
#########################################MOVIMIENTO#####################################################
def handle_jump():
    global hit_box_eje_y, is_jumping, jump_count

    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            hit_box_eje_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10
########################################################################################################

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
        if not is_jumping:
            if True in pressed_keys:
                if pressed_keys [K_a]:
                    if hit_box_eje_x > 0:
                        hit_box_eje_x -= 5#se movera a la izquierda
                        draw_hit_box()
                if pressed_keys [K_d]:
                    if hit_box_eje_x < 780:
                        hit_box_eje_x += 5#se movera a la derecha
                        draw_hit_box()
                if pressed_keys[K_SPACE]:
                    is_jumping = True
        else:
            handle_jump()

    # Dibuja la imagen de fondo en la pantalla
    screen.blit(background_image_transform_0, (0, 0))
    screen.blit(background_image_transform_1, (2, 2))
    
    #permanece dibujado el cuadrado
    draw_hit_box()

    pygame.display.flip() #Muestra los cambios

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(404) #se usa para indicar si el programa terminó con éxito o con un error (404)