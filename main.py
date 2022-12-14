# libreria per la GUI
from math import *

import pygame

from NRMethod import NRMethod
from utils.draw import drawgrid, drawfunction
from utils.inputBox import InputBox
from utils.passaggi import passaggi

# costanti matematiche
ln = lambda x: log(x, e)

# definisco la funzione
testof = "sin(cos(x))"
f = lambda x: eval(testof)
g = 1
zero = NRMethod(f, g)

# GUI

# schermo
screen = pygame.display.set_mode((1080, 1080))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 18)
inputbox = InputBox(5, 125, 200, 35, text="f(x)=", div=5)
guessbox = InputBox(5, 175, 200, 35, text=f"punto iniziale=", div=15)

gridsize = 4
deltax = 0
deltay = 0

Passaggi = passaggi(screen=screen, f=f, g=g, gridsize=gridsize, deltax=deltax, deltay=deltay)

while True:

    # raccogli eventi. Non serve a molto per ora
    for event in pygame.event.get():
        Passaggi.update(gridsize, deltax, deltay)
        res = inputbox.handle_event(event)
        if res:
            testof = res
            f = lambda x: eval(testof)
            zero = NRMethod(f, 3)
        res = guessbox.handle_event(event)
        if res:
            try:
                int(res)
                Passaggi.refresh(int(res))
            except:
                pass
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if not inputbox.active and not guessbox.active:
                if event.key == pygame.key.key_code("return"):
                    Passaggi.next()
                if event.key == pygame.key.key_code("E"): # rimpicciolisci
                    gridsize = gridsize-1 if gridsize > 1 else gridsize
                elif event.key == pygame.key.key_code("Q"): # ingrandisci
                    gridsize += 1
                if event.key == pygame.key.key_code("A"): # destra
                    deltax += gridsize * 4
                elif event.key == pygame.key.key_code("D"): # sinistra
                    deltax -= gridsize * 4
                if event.key == pygame.key.key_code("W"): # su
                    deltay += gridsize * 4
                elif event.key == pygame.key.key_code("S"):# giu'
                    deltay -= gridsize * 4

    inputbox.update()
    guessbox.update()

    # colore di sottofondo
    screen.fill((0, 0, 0))

    inputbox.draw(screen)
    guessbox.draw(screen)

    # disegna la griglia
    drawgrid(screen, gridsize, deltax, deltay)
    size = screen.get_size()
    dx = int(size[0] / gridsize)
    dy = dx

    # metti i punti nel grafico
    drawfunction(screen, f, gridsize, deltax, deltay)

    # passaggi
    Passaggi.draw()

    # testo dello 0 della funzione
    testo = font.render(f"zero in {zero:3f}", True, (120, 120, 255))
    screen.blit(testo, (5, 0))

    # testo della funzione
    testo = font.render(f"f(x)={testof}", True, (120, 120, 255))
    screen.blit(testo, (5, 25))

    # altri testi
    testo = font.render(f"dimensioni griglia={gridsize}", True, (120, 120, 255))
    screen.blit(testo, (5, 50))

    pygame.display.flip()

    clock.tick(60)
