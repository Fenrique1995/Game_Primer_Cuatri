import pygame 
from pygame.locals import K_a,K_d,K_SPACE, K_RETURN, K_r
import sys
import random

ANCHO = 600
ALTURA = 800

pygame.init()#Se inicializa pygame
                                #Altura#Ancho
screen = pygame.display.set_mode((ALTURA,ANCHO))#La ventana
pygame.display.set_caption("GAME 0.3")#Titulo que aparece en la ventana

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

attack_left= [pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L1.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L2.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L3.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L4.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L5.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L6.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L7.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_L/Atk_L8.png"),
        ]
attack_right= [pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R1.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R2.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R3.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R4.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R5.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R6.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R7.png"),
        pygame.image.load("Img/sprite/Ataque/Attack_R/Atk_R8.png"),
        ]

#Enemigo
enemigo = [pygame.image.load("Img/sprite/Enemy/radioactive monsters not glowing.png")]


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
        # Ataque
        self.attack = False
        # Vida
        self.hitbox = pygame.Rect(self.x, self.y, 64, 64)
        self.vida = 30
        self.vidas = 1
        self.vivo = True

##########################################MOVIMIENTO############################################################
    def move_hero(self, userInput):
        #Esta funcion esta encargada de mover al heroe 
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
    def draw(self, win,userInput):
        #Esta funcion esta encargada de dibujar la hitbox y de los cambios de los sprites
        self.hitbox = pygame.Rect(self.x + 5, self.y + 15, 30, 40)
        pygame.draw.rect(win, (0,0,0), self.hitbox, 1)
        
        if userInput[pygame.K_RETURN]:
            self.colision = True
            if self.stepIndex >= 8:
                self.stepIndex = 0
            if self.face_left:
                win.blit(attack_left[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
                self.espada_hitbox = pygame.Rect(self.x - 25, self.y + 15, 30, 40)
                pygame.draw.rect(screen, (0,0,0), self.espada_hitbox, 1)
                self.slash()
            if self.face_right:
                win.blit(attack_right[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
                self.espada_hitbox = pygame.Rect(self.x + 25, self.y + 15, 30, 40)
                pygame.draw.rect(screen, (0,0,0), self.espada_hitbox, 1)
                self.slash()
        elif pygame.K_UP:
            self.colision = False
            if self.stepIndex >= 8:
                self.stepIndex = 0
            if self.face_left:
                win.blit(left[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
            if self.face_right:
                win.blit(right[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
    def jump_motion(self, userInput):
        #Esta funcion esta encargada del salto
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.movy*4
            self.movy -= 1
        if self.movy < -10:
            self.jump = False
            self.movy = 10
    def direction(self):
        #La direccion del salto
        if self.face_right:
            return 1
        if self.face_left:
            return -1
    def slash(self):
        #Funcion del ataque
        for enemigo in enemigos:
                if self.espada_hitbox.colliderect(enemigo.hitbox):
                    enemigo.vida -= 1
                    print("jugador golpea enemigo ")

class Enemigo:
    def __init__(self, x, y , direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.stepIndex = 0
        #Vida
        self.hitbox = pygame.Rect(self.x,self.y,64,64)
        self.vida = 1
        self.images = [pygame.image.load("Img/sprite/Enemy/radioactive monsters not glowing.png")]
    def step(self):
        if self.stepIndex >= 1:
            self.stepIndex = 0
    def draw(self,win):
        self.hitbox = pygame.Rect(self.x + 5, self.y + 15, 30, 40)
        pygame.draw.rect(win, (0, 0, 0), self.hitbox, 1)
        self.step()
        if self.direction == left:
            win.blit(self.images[self.stepIndex], (self.x, self.y))
        if self.direction == right:
            win.blit(self.images[self.stepIndex], (self.x, self.y))
    def move(self):
        if self.direction == left:
            self.x -= 5
        if self.direction == right:
            self.x += 5
    def hit(self):
        if jugador.hitbox.colliderect(self.hitbox):
            if jugador.vida > 0:
                jugador.vida -= 1
                print("enemigo golpea jugador")
                if jugador.vida == 0 and jugador.vidas > 0:
                    jugador.vidas -= 1
                    jugador.vida = 30
                elif jugador.vida == 0 and jugador.vidas == 0:
                    jugador.vivo = False

    def off_screen(self):
        return not(self.x >= -10 and self.x <= 770)

#####################################################DIBUJO#########################################################
#Dibuja en la pantalla
def draw_game():
    screen.fill((0, 0, 0))
    screen.blit(background_image_transform_0, (0, 0))
    screen.blit(background_image_transform_1, (2, 2))
    #Dibuja al jugador
    jugador.draw(screen,tecla)
    #Dibuja a los enemigos
    for enemigo in enemigos:
        monstruo.draw(screen)
    
    if jugador.vivo == False:
        screen.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf',32)
        text = font.render('HAS MUERTO! Presiona R para reiniciar', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center =(400,200)
        screen.blit(text, text_rect)
        if tecla[pygame.K_r]:
            jugador.vivo = True
            jugador.vidas = 1
            jugador.vida = 30
    pygame.time.delay(30)
    pygame.display.update()
#Declara al jugador y setea donde se lo dibuja
                #Y   #X
jugador = Heroe(250,450)
#Declara una lista para enemigos
enemigos = []

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
    
    #Se dibuja el Enemigo
    if len(enemigos) == 0:
        num_rand = random.randint(0,2)
        if num_rand == 1:
            monstruo = Enemigo(750, 460, left)
            enemigos.append(monstruo)
        if num_rand == 2:
            monstruo = Enemigo(50, 460, right)
            enemigos.append(monstruo)
    for enemigo in enemigos:
        monstruo.move()
        monstruo.hit()
        if monstruo.vida == 0:
            enemigos.remove(monstruo)
        if monstruo.off_screen():
            enemigos.remove(monstruo)

    draw_game()#Dibuja en el juego
    pygame.display.flip() #Muestra los cambios

pygame.quit()
sys.exit(404) #se usa para indicar si el programa terminó con éxito o con un error (404)