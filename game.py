import pygame 
from pygame.locals import K_a, K_d, K_SPACE, K_RETURN, K_r, QUIT, K_BACKSPACE
import sys
import random
import sqlite3
import json

ANCHO = 600
ALTURA = 800

pygame.init()#Se inicializa pygame
                                #Altura#Ancho
screen = pygame.display.set_mode((ALTURA,ANCHO))#La ventana
pygame.display.set_caption("GAME 1.3")#Titulo que aparece en la ventana

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

#Heroe vida
heart = [pygame.image.load("Img/sprite/Life/hearts/heart_01.png")]


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
        self.vida = 3
        self.vidas = 1
        self.vivo = True
        self.score = 0
        # Nombre del jugador
        self.nombre = ""
        #Sonido de golpe
        self.hit_sound_01 = pygame.mixer.Sound("Sound/hit20.mp3.flac")

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
                self.hit_sound_01.play()
            if self.face_right:
                win.blit(attack_right[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
                self.espada_hitbox = pygame.Rect(self.x + 25, self.y + 15, 30, 40)
                pygame.draw.rect(screen, (0,0,0), self.espada_hitbox, 1)
                self.slash()
                self.hit_sound_01.play()
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
                    if self.face_right:
                        enemigo.x += 10
                    elif self.face_left:
                        enemigo.x -= 10
                    print("jugador golpea enemigo ",self.score)
    def heart_handler(self):
        match self.vida:
            case 2:
                heart_01.set_invisible()
            case 1:
                heart_02.set_invisible()
        if self.vida < 3:
            self.damaged = True
        if self.vida < 2:
            self.damaged = True
        self.damaged = False

class Enemigo:
    def __init__(self, x, y , direction):
        self.x = x
        self.y = y
        self.direction = direction
        #Vida
        self.hitbox = pygame.Rect(self.x,self.y,64,64)
        self.vida = 1
        self.images = [pygame.image.load("Img/sprite/Enemy/Grue_01.png"),pygame.image.load("Img/sprite/Enemy/Grue_02.png")]
        self.hit_sound_02 = pygame.mixer.Sound("Sound/hit28.mp3.flac")
    def draw(self,win):
        self.hitbox = pygame.Rect(self.x+15, self.y + 15, 30, 40)
        pygame.draw.rect(win, (0, 0, 0), self.hitbox, 1)
        if self.direction == left:
            win.blit(self.images[1], (self.x, self.y))
        if self.direction == right:
            win.blit(self.images[0], (self.x, self.y))
    def move(self):
        if self.direction == left:
            self.x -= 5
        if self.direction == right:
            self.x += 5
    def sprint(self):
        if self.direction == left:
            self.x -= 15
        if self.direction == right:
            self.x += 15
    def run(self):
        if self.direction == left:
            self.x -= 20
        if self.direction == right:
            self.x += 20
    def hit(self):
        if jugador.hitbox.colliderect(self.hitbox):
            self.hit_sound_02.play()
            if jugador.vida > 0:
                jugador.vida -= 1
                if jugador.face_left:
                    jugador.x += 10
                elif jugador.face_right:
                    jugador.x -= 10
                print("enemigo golpea jugador")
                if jugador.vida == 0 and jugador.vidas > 0:
                    jugador.vidas -= 1
                    jugador.vida = 3
                elif jugador.vida == 0 and jugador.vidas == 0:
                    jugador.vivo = False

    def off_screen(self):
        return not(self.x >= -10 and self.x <= 770)

class Button:
    def __init__(self, rect, text, color, hover_color, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.color, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

class Corazon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = heart
        self.visible = True
    def draw(self,win):
        if self.visible:
            win.blit(self.images[0], (self.x, self.y))
    def set_invisible(self):
        self.visible = False

heart_01 = Corazon(750,20)
heart_02 = Corazon(720,20)
heart_03 = Corazon(690,20)

#####################################################DIBUJO#########################################################

def draw_start_screen(boton_start,boton_score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Presiona start para empezar', True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 200))
    screen.blit(text, text_rect)
    boton_start.draw(screen, font)
    boton_score.draw(screen, font)
    
    menu_music.play(1)

#Boton de start
verde = (0, 255, 0)

boton_start_rect = pygame.Rect((300, 250, 150, 50))
boton_start = Button(boton_start_rect, 'Start', (0, 128, 0), verde , lambda: None)
boton_score_rect = pygame.Rect((300, 350, 150, 50))
boton_score = Button(boton_score_rect, 'Score', (0, 128, 0), verde , lambda: None)
boton_return_rect = pygame.Rect((50, 50, 150, 50))
boton_return = Button(boton_return_rect, 'Volver', (0, 128, 0), verde , lambda: None)

#nombre del usuario y su funcion input
font = pygame.font.Font('freesansbold.ttf', 32)
nombre = ""
input_rect = pygame.Rect(310,310,140,32)
blanco = (255, 255, 255)
activo = False

def input_nombre(): 
    boton_start.check_hover(mouse_pos)
    text_surface = font.render(nombre,True, (255, 255, 255))
    pygame.draw.rect(screen,blanco,input_rect,2)
    screen.blit(text_surface,(input_rect.x,input_rect.y))
    jugador.nombre = nombre
    input_rect.w = max(140,text_surface.get_width())


#Dibuja en la pantalla
def draw_game():
    menu_music.stop()
    screen.fill((0, 0, 0))
    screen.blit(background_image_transform_0, (0, 0))
    screen.blit(background_image_transform_1, (2, 2))
    font = pygame.font.Font('freesansbold.ttf',32)
    text = font.render('Score: '+str(jugador.score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center =(70,40)
    screen.blit(text, text_rect)
    #Dibuja al jugador
    jugador.draw(screen,tecla)
    
    heart_01.draw(screen)
    heart_02.draw(screen)
    heart_03.draw(screen)
    
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
            jugador.vida = 3
            jugador.score = 0
            heart_01.visible = True
            heart_02.visible = True
    pygame.time.delay(30)
    pygame.display.update()

#Declara al jugador y setea donde se lo dibuja
                #Y   #X
jugador = Heroe(250,450)
#Declara una lista para enemigos
enemigos = []

fps = pygame.time.Clock()
mouse_pos = (0,0)

#En esta funcion se encarga de guardar el nombre del jugador y el score acumulado al terminar el juego
def save_to_sqlite(variable_name, obj_attribute):
    try:
        mi_conexion = sqlite3.connect('src/mi_basede_datos.sql')
        cursor = mi_conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mi_tabla (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                score INTEGER
            )
        ''')

        # Verificar si el nombre ya existe en la base de datos
        cursor.execute('SELECT score FROM mi_tabla WHERE nombre = ?', (variable_name,))
        resultado = cursor.fetchone()

        if variable_name == "Anon" and resultado is not None:
            # Si el nombre es "Anon" y ya existe, verificar si el nuevo score es mayor
            score_existente = resultado[0]
            if obj_attribute > score_existente:
                # El nuevo score es mayor, actualizar el score existente
                cursor.execute('''
                    UPDATE mi_tabla
                    SET score = ?
                    WHERE nombre = "Anon"
                ''', (obj_attribute,))
        else:
            # Si el nombre no existe o no es "Anon", realizar la inserción
            if variable_name == "":
                cursor.execute('''
                    INSERT INTO mi_tabla (nombre, score)
                    VALUES (?, ?)
                ''', ("Anon", obj_attribute))
            else:
                cursor.execute('''
                    INSERT INTO mi_tabla (nombre, score)
                    VALUES (?, ?)
                ''', (variable_name, obj_attribute))

        mi_conexion.commit()
        mi_conexion.close()

    except Exception as e:
        print(f"Se produjo una excepción al guardar en la base de datos: {e}")

def load_from_sqlite():
    try:
        mi_conexion = sqlite3.connect('src/mi_basede_datos.sql')
        cursor = mi_conexion.cursor()

        cursor.execute('SELECT nombre, score FROM mi_tabla')
        rows = cursor.fetchall()

        mi_conexion.close()

        return {nombre: score for nombre, score in rows}
    except Exception as e:
        print(f"Se produjo una excepción al cargar desde la base de datos: {e}")
        return {}

json_data = load_from_sqlite()

def display_sorted_data(data):
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    y_position = (ALTURA - len(sorted_data) * 30) // 2  # Centrar verticalmente

    for nombre, score in sorted_data:
        text = font.render(f"{nombre}: {score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(ALTURA // 2, y_position))
        screen.blit(text, text_rect)
        y_position += 30

def display_scores_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Scores', True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 50))
    screen.blit(text, text_rect)

    display_sorted_data(json_data)
    boton_return.draw(screen, font)

menu_music = pygame.mixer.Sound("Sound/awesomeness.wav")

#########################BUCLE PRINCIPAL#############################
running = True
game_start = False
show_scores = False
while running:

    screen.fill((0,0,0))
    fps.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and boton_score.hovered:
                show_scores = True
                boton_return.check_hover(mouse_pos)
            if pygame.mouse.get_pressed()[0] and boton_return.hovered:
                show_scores = False
            if input_rect.collidepoint(mouse_pos):
                activo = True
            if game_start:
                draw_game()
            elif show_scores:
                display_scores_screen()
        else:
            if activo == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        nombre = nombre[0:-1]
                    else:
                        nombre += event.unicode
            # Dibuja la pantalla de inicio
            draw_start_screen(boton_start, boton_score)
            boton_start.check_hover(mouse_pos)
            boton_score.check_hover(mouse_pos)
            text_surface = font.render(nombre,True, (255, 255, 255))
            pygame.draw.rect(screen,blanco,input_rect,2)
            screen.blit(text_surface,input_rect)
            # Verifica clic en el botón
            if pygame.mouse.get_pressed()[0] and boton_start.hovered:
                game_start = True
                jugador 
                enemigos 
            elif boton_score.hovered:
                show_scores = True

        if event.type == pygame.QUIT:
            running = False
        tecla = pygame.key.get_pressed()

    jugador.move_hero(tecla)
    jugador.jump_motion(tecla)
    jugador.heart_handler()

    #Se dibuja el Enemigo y se gestiona el movimiento asi como la vida
    if len(enemigos) == 0:
        num_rand = random.randint(0,2)
        if num_rand == 1:
            monstruo = Enemigo(750, 460, left)
            enemigos.append(monstruo)
        if num_rand == 2:
            monstruo = Enemigo(50, 460, right)
            enemigos.append(monstruo)
    if jugador.score < 10 :
        for enemigo in enemigos:
            monstruo.move()
            monstruo.hit()
            if monstruo.vida == 0:
                enemigos.remove(monstruo)
                jugador.score+=2
            if monstruo.off_screen():
                enemigos.remove(monstruo)
    if jugador.score >= 10 :
        for enemigo in enemigos:
            monstruo.sprint()
            monstruo.hit()
            if monstruo.vida == 0:
                enemigos.remove(monstruo)
                jugador.score+=2
            if monstruo.off_screen():
                enemigos.remove(monstruo)
    if jugador.score >= 20 :
        for enemigo in enemigos:
            monstruo.run()
            monstruo.hit()
            if monstruo.vida == 0:
                enemigos.remove(monstruo)
                jugador.score+=2
            if monstruo.off_screen():
                enemigos.remove(monstruo)

    if game_start:
        draw_game()#Dibuja en el juego
    else:
        # Dibuja la pantalla de inicio
        draw_start_screen(boton_start,boton_score)
        boton_start.check_hover(mouse_pos)

        # Verifica clic en el botón
        if pygame.mouse.get_pressed()[0] and boton_start.hovered:
            game_start = True
            jugador 
            enemigos 
    if game_start == False:
            input_nombre()

    if show_scores:
        display_scores_screen()

    pygame.display.flip() #Muestra los cambios

save_to_sqlite(jugador.nombre, jugador.score)

pygame.quit()
sys.exit(404) #se usa para indicar si el programa terminó con éxito o con un error (404)