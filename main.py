import pygame
from game import Game
from constant import *

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def main():
    run = True
    game = Game(WIN)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_coordinate = pygame.mouse.get_pos()
                mouse_pos = get_pos_from_mouse(mouse_coordinate)
                game.select(mouse_pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.undo()
                if event.key == pygame.K_RIGHT:
                    game.redo()
        
        game.update()

    pygame.quit()


if __name__ == '__main__':
    main()