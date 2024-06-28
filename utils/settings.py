import pygame

pygame.init()
pygame.font.init()

## IA

MODEL_PATH = './model/handWritten.model.keras'
INPUT_SIZE = 28
EPOCHS = 50

HIDDEN_LAYERS = 2
NODES_IN_HIDDEN_LAYERS = 128

## UI

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

ROWS = COLS = INPUT_SIZE
PIXEL_SIZE = 18

DRAW_WIDTH = DRAW_HEIGHT = PIXEL_SIZE * ROWS

WIDTH = DRAW_WIDTH + 530
HEIGHT = DRAW_HEIGHT + 110

TOOLBAR_HEIGHT = 100

BG_COLOR = BLACK

def get_font(size):
    return pygame.font.SysFont('comicsans', size)