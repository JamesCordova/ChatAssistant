
import tkinter as tk
import pygame
from pygame.locals import *

class JuegoPygame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Inicializar Pygame
        pygame.init()

        # Configurar el tamaño del juego
        self.ancho = 400
        self.alto = 300

        # Crear la pantalla de Pygame
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto), DOUBLEBUF)
        
        # Obtener el identificador de la ventana
        self.hwnd = pygame.display.get_wm_info()["window"]
        
        # Otros elementos de juego (puedes personalizar según tu juego)
        self.reloj = pygame.time.Clock()
        self.jugador = pygame.Rect(50, 50, 50, 50)
        self.velocidad = 5

        # Configurar el bucle del juego
        self.ejecutar_juego()

    def ejecutar_juego(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    quit()
                elif evento.type == KEYDOWN:
                    if evento.key == K_ESCAPE:
                        pygame.quit()
                        quit()

            # Lógica del juego (aquí puedes colocar la lógica de tu juego)
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.jugador.x -= self.velocidad
            if keys[K_RIGHT]:
                self.jugador.x += self.velocidad
            if keys[K_UP]:
                self.jugador.y -= self.velocidad
            if keys[K_DOWN]:
                self.jugador.y += self.velocidad

            # Dibujar en la pantalla
            self.pantalla.fill((255, 255, 255))  # Color de fondo blanco
            pygame.draw.rect(self.pantalla, (0, 0, 255), self.jugador)  # Rectángulo azul (jugador)

            # Actualizar la pantalla
            pygame.display.flip()

            # Establecer la velocidad del juego
            self.reloj.tick(30)

            # Actualizar la ventana de Tkinter
            self.master.update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pygame en Tkinter")

    juego = JuegoPygame(root)

    root.mainloop()
