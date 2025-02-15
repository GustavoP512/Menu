import pygame
import funciones_caballos as fc

def run_game():
    pygame.init()

    screen=pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Speed Horse')

    fc.carrera(screen)

run_game()