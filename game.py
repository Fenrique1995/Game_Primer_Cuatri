import pygame 
from pygame.locals import K_a,K_d,K_SPACE, K_RETURN
import sys

ANCHO = 600
ALTURA = 800

pygame.init()#Se inicializa pygame
                                #Altura#Ancho
screen = pygame.display.set_mode((ALTURA,ANCHO))#La ventana
pygame.display.set_caption("GAME 0.2")#Titulo que aparece en la ventana

background_image_0 = pygame.image.load("Img/parallax_forest_pack/layers/parallax-forest-back-trees.png")
background_image_1 = pygame.image.load("Img/parallax_forest_pack/layers/parallax-forest-front-trees.png")
background_image_transform_0 = pygame.transform.scale(background_image_0, (ALTURA,ANCHO))
background_image_transform_1 = pygame.transform.scale(background_image_1, (ALTURA,ANCHO))
##########################################PERSONAJES############################################################
# Heroe (Player)
left = [pygame.image.load("Img/sprite/Walk_Left/L1.png"),
        pygame.image.load("Img/sprite/Walk_Left/L2.png"),
        pygame.image.load("Img/sprite/Walk_Left/L3.png"),
        pygame.image.load("Img/sprite/Walk_Left/L4.png"),
        pygame.image.load("Img/sprite/Walk_Left/L5.png"),
        pygame.image.load("Img/sprite/Walk_Left/L6.png"),
        pygame.image.load("Img/sprite/Walk_Left/L7.png"),
        pygame.image.load("Img/sprite/Walk_Left/L8.png"),
        ]

right =[pygame.image.load("Img/sprite/Walk_Right/R1.png"),
        pygame.image.load("Img/sprite/Walk_Right/R2.png"),
        pygame.image.load("Img/sprite/Walk_Right/R3.png"),
        pygame.image.load("Img/sprite/Walk_Right/R4.png"),
        pygame.image.load("Img/sprite/Walk_Right/R5.png"),
        pygame.image.load("Img/sprite/Walk_Right/R6.png"),
        pygame.image.load("Img/sprite/Walk_Right/R7.png"),
        pygame.image.load("Img/sprite/Walk_Right/R8.png"),
        ]


class Heroe:
    def __init__(self, x, y):
        # Caminar
        self.x = x
        self.y = y
        self.movx = 10
        self.movy = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        # Salto
        self.jump = False
        # Vida
        self.hitbox = (self.x, self.y, 64, 64)
##########################################MOVIMIENTO############################################################
#Esta funcion esta encargada de mover al heroe 
    def move_hero(self, userInput):
        if userInput[pygame.K_d] and self.x <= 760:
            self.x += self.movx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_a] and self.x >= 0:
            self.x -= self.movx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0
#Esta funcion esta encargada de dibujar la hitbox y de los cambios de los sprites
    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 15, 30, 40)
        pygame.draw.rect(win, (0,0,0), self.hitbox, 1)
        if self.stepIndex >= 8:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
#Esta funcion esta encargada del salto
    def jump_motion(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.movy*4
            self.movy -= 1
        if self.movy < -10:
            self.jump = False
            self.movy = 10
#La direccion del salto 
    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    def cooldown(self):
        if self.cool_down_count >= 20:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

#####################################################DIBUJO#########################################################
#Dibuja en la pantalla
def draw_game():
    screen.fill((0, 0, 0))
    screen.blit(background_image_transform_0, (0, 0))
    screen.blit(background_image_transform_1, (2, 2))
    jugador.draw(screen)
    pygame.time.delay(30)
    pygame.display.update()
#Declara al jugador y seta donde se lo dibuja
                #Y   #X
jugador = Heroe(250,450)

fps = pygame.time.Clock()

#########################BUCLE PRINCIPAL#############################
running = True
while running:

    screen.fill((0,0,0))
    fps.tick(60) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        tecla = pygame.key.get_pressed()

    jugador.move_hero(tecla)
    jugador.jump_motion(tecla)

    #Dibuja en el juego
    draw_game()
    pygame.display.flip() #Muestra los cambios

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(404) #se usa para indicar si el programa terminó con éxito o con un error (404)