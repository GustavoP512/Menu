import pygame
import funciones_caballos as fc
from clases_juego import Usuario


user=Usuario(1000)


def run_game():
    pygame.init()

    screen=pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Carrera de Caballos')

    fc.carrera(usuario=user, screen=screen)



run_game()



