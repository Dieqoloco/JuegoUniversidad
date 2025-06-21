import pygame
import math
pygame.init()
class prota():
    def __init__(self, x, y, imagen):
        self.activar_animación = False
        self.invertidox = False
        self.invertidoy = False
        self.imagen = imagen
        self.frame_de_animacion = 0
        self.actualizar_ticks = pygame.time.get_ticks()
        self.imagen_frame = imagen[self.frame_de_animacion]
        self.forma = self.imagen_frame.get_rect()
        self.forma.center = (x,y)
    def actualizar(self):
        couldown = 200
        self.imagen_frame = self.imagen[self.frame_de_animacion]
        if self.activar_animación:
            if pygame.time.get_ticks() - self.actualizar_ticks >= couldown:
                self.frame_de_animacion += 1
                self.actualizar_ticks = pygame.time.get_ticks()
            if self.frame_de_animacion >= len(self.imagen):
                self.frame_de_animacion = 0
        else:
            self.frame_de_animacion = 0
    def dibujar(self, interfaz):
        imagen_invertida = pygame.transform.flip(self.imagen_frame,self.invertidox,self.invertidoy)
        interfaz.blit(imagen_invertida,self.forma)
        pygame.draw.rect(interfaz, (255,0,255),self.forma,1)
    def moivimiento(self, eje_x, eje_y):
        if eje_x>0:
            self.invertidox = True
            self.activar_animación = True
        elif eje_x == 0:
            self.activar_animación = False
        elif eje_x<0:
            self.invertidox = False
            self.activar_animación = True
        if eje_y<0:
            self.invertidoy = True
            self.activar_animación = True
        elif eje_y==0:
            if eje_x ==0:
                self.activar_animación = False
        else:
            self.invertidoy = False
            self.activar_animación = True
        self.forma.x = self.forma.x + eje_x
        self.forma.y = self.forma.y + eje_y
class Arma():
    def __init__(self,imagen):
        self.imagen_original = imagen
        self.angulo = 0
        self.imagen_utilizada = pygame.transform.rotate(self.imagen_original,self.angulo)
        self.forma = self.imagen_utilizada.get_rect()
    def actualizar(self, player):
        self.forma.center = player.forma.center
        self.imagen_utilizada = pygame.transform.rotate(self.imagen_utilizada,self.angulo)
        if player.invertidox == False:
            self.forma.y += 10
            self.forma.x -= player.forma.width/2
            self.rotacion(False)
        if player.invertidox == True:
            self.forma.y += 10
            self.forma.x += player.forma.width/2
            self.rotacion(True)
        posicion_mouse = pygame.mouse.get_pos()
        diferencia_x = posicion_mouse[0] - self.forma.centerx
        diferencia_y = -(posicion_mouse[1] - self.forma.centery)
        self.angulo = 180 + math.degrees(math.atan2(diferencia_y, diferencia_x))
    def dibujar(self, interfaz):
        #self.imagen_utilizada = pygame.transform.rotate(self.imagen_utilizada,self.angulo)
        interfaz.blit(self.imagen_utilizada, self.forma)
        pygame.draw.rect(interfaz, (255,0,255),self.forma,1)
    def rotacion(self, rotar):
        if rotar:
            imagen_rotada = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen_utilizada = pygame.transform.rotate(imagen_rotada,self.angulo)
        else:
            imagen_rotada = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen_utilizada = pygame.transform.rotate(imagen_rotada,self.angulo)
anchov= 900
largov= 750
ventana = pygame.display.set_mode((anchov,largov))
pygame.display.set_caption('Pinguino Cruzar hielo osos ballenas escapa juego')

cambio_de_frame = []
for p in range(2):
    protagonista_imagen = pygame.image.load('repositorio//assets/imagenes/Personajes/protagonista/pato_0.png')
    cambio_de_frame.append(protagonista_imagen)
protagonista = prota(30,30, cambio_de_frame)
frames = pygame.time.Clock()
imagen_blaster = pygame.image.load('repositorio//assets/imagenes/Armas/arma_de_portales.png')
Blaster = Arma(imagen_blaster)

M_arriba    = False
M_abajo     = False
M_derecha   = False
M_izquerda  = False

Iniciado = True
while Iniciado:
    ventana.fill((100,100,255))
    frames.tick(60)
    ejep_x = 0
    ejep_y = 0
    if M_arriba == True:
        ejep_y = -10
    if M_abajo == True:
        ejep_y = 10
    if M_derecha == True:
        ejep_x = 10
    if M_izquerda == True:
        ejep_x = -10
    
    protagonista.moivimiento(ejep_x, ejep_y)
    protagonista.dibujar(ventana)
    protagonista.actualizar()
    
    Blaster.actualizar(protagonista)
    Blaster.dibujar(ventana)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Iniciado = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                M_arriba =      True
            if evento.key == pygame.K_s:
                M_abajo =       True
            if evento.key == pygame.K_d:
                M_derecha =     True
            if evento.key == pygame.K_a:
                M_izquerda =    True
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_w:
                M_arriba =      False
            if evento.key == pygame.K_s:
                M_abajo =       False
            if evento.key == pygame.K_d:
                M_derecha =     False
            if evento.key == pygame.K_a:
                M_izquerda =    False
    if protagonista.forma.left <0:
        protagonista.forma.left = 0
    if protagonista.forma.top<0:
        protagonista.forma.top  = 0
    if protagonista.forma.right > anchov:
        protagonista.forma.right    =anchov 
    if protagonista.forma.bottom > largov:
        protagonista.forma.bottom   =largov
    pygame.display.update()
pygame.quit()