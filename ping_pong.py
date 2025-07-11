import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 500
FPS = 60

# Colores
CELESTE = (135, 206, 235)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (154, 205, 50)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong")
reloj = pygame.time.Clock()

# Clase para las raquetas
class Raqueta:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 20
        self.alto = 100
        self.velocidad = 8
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
    
    def mover_arriba(self):
        if self.y > 0:
            self.y -= self.velocidad
            self.rect.y = self.y
    
    def mover_abajo(self):
        if self.y < ALTO - self.alto:
            self.y += self.velocidad
            self.rect.y = self.y
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, NEGRO, self.rect)
        pygame.draw.rect(superficie, BLANCO, (self.x + 2, self.y + 2, self.ancho - 4, self.alto // 3), border_radius=8)

# Clase para la pelota
class Pelota:
    def __init__(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.radio = 12
        self.velocidad_x = random.choice([-6, 6])
        self.velocidad_y = random.choice([-4, 4])
        self.rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
    
    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.rect.x = self.x - self.radio
        self.rect.y = self.y - self.radio
        
        # Rebote en paredes superior e inferior
        if self.y <= self.radio or self.y >= ALTO - self.radio:
            self.velocidad_y = -self.velocidad_y
    
    def reiniciar(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_x = random.choice([-6, 6])
        self.velocidad_y = random.choice([-4, 4])
        self.rect.x = self.x - self.radio
        self.rect.y = self.y - self.radio
    
    def dibujar(self, superficie):
        # Sombra
        pygame.draw.circle(superficie, (100, 100, 100), (self.x + 3, self.y + 3), self.radio)
        # Pelota principal
        pygame.draw.circle(superficie, VERDE, (self.x, self.y), self.radio)
        # Brillo
        pygame.draw.circle(superficie, BLANCO, (self.x - 4, self.y - 4), self.radio // 3)

# Clase principal del juego
class JuegoPingPong:
    def __init__(self):
        self.jugador1 = Raqueta(30, ALTO // 2 - 50)
        self.jugador2 = Raqueta(ANCHO - 50, ALTO // 2 - 50)
        self.pelota = Pelota()
        self.puntaje1 = 0
        self.puntaje2 = 0
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_controles = pygame.font.Font(None, 24)
        self.pausado = False
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.pausado = not self.pausado
                elif evento.key == pygame.K_r:
                    self.reiniciar_juego()
        return True
    
    def actualizar(self):
        if self.pausado:
            return
        
        # Controles del jugador 1 (W/S)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            self.jugador1.mover_arriba()
        if teclas[pygame.K_s]:
            self.jugador1.mover_abajo()
        
        # Controles del jugador 2 (Flechas)
        if teclas[pygame.K_UP]:
            self.jugador2.mover_arriba()
        if teclas[pygame.K_DOWN]:
            self.jugador2.mover_abajo()
        
        # Mover pelota
        self.pelota.mover()
        
        # Colisiones con raquetas
        if self.pelota.rect.colliderect(self.jugador1.rect) or self.pelota.rect.colliderect(self.jugador2.rect):
            self.pelota.velocidad_x = -self.pelota.velocidad_x
            # Agregar variación aleatoria
            self.pelota.velocidad_y += random.uniform(-1, 1)
            # Aumentar velocidad ligeramente
            self.pelota.velocidad_x *= 1.02
            self.pelota.velocidad_y *= 1.02
        
        # Puntuación
        if self.pelota.x < 0:
            self.puntaje2 += 1
            self.pelota.reiniciar()
        elif self.pelota.x > ANCHO:
            self.puntaje1 += 1
            self.pelota.reiniciar()
    
    def dibujar(self):
        # Fondo
        pantalla.fill(CELESTE)
        
        # Línea central
        pygame.draw.line(pantalla, BLANCO, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)
        
        # Dibujar objetos del juego
        self.jugador1.dibujar(pantalla)
        self.jugador2.dibujar(pantalla)
        self.pelota.dibujar(pantalla)
        
        # Puntaje
        texto_puntaje = self.fuente.render(f"{self.puntaje1} - {self.puntaje2}", True, BLANCO)
        rect_puntaje = texto_puntaje.get_rect(center=(ANCHO // 2, 50))
        pygame.draw.rect(pantalla, NEGRO, rect_puntaje.inflate(40, 20), border_radius=15)
        pantalla.blit(texto_puntaje, rect_puntaje)
        
        # Controles
        texto_controles = self.fuente_controles.render("Jugador 1: W/S | Jugador 2: ↑/↓ | Espacio: Pausar | R: Reiniciar", True, BLANCO)
        rect_controles = texto_controles.get_rect(center=(ANCHO // 2, ALTO - 30))
        pygame.draw.rect(pantalla, NEGRO, rect_controles.inflate(20, 10), border_radius=10)
        pantalla.blit(texto_controles, rect_controles)
        
        # Mensaje de pausa
        if self.pausado:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(128)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            texto_pausa = self.fuente.render("PAUSADO", True, BLANCO)
            rect_pausa = texto_pausa.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(texto_pausa, rect_pausa)
            
            texto_continuar = self.fuente_controles.render("Presiona ESPACIO para continuar", True, BLANCO)
            rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
            pantalla.blit(texto_continuar, rect_continuar)
        
        pygame.display.flip()
    
    def reiniciar_juego(self):
        self.puntaje1 = 0
        self.puntaje2 = 0
        self.jugador1.y = ALTO // 2 - 50
        self.jugador2.y = ALTO // 2 - 50
        self.jugador1.rect.y = self.jugador1.y
        self.jugador2.rect.y = self.jugador2.y
        self.pelota.reiniciar()
        self.pausado = False
    
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    juego = JuegoPingPong()
    juego.ejecutar()