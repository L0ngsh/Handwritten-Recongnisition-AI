from .settings import *
from .button import Button
from .handwrittenRecognition import HandwrittenRecognition
from .display import Display
import pygame

pygame.init()
pygame.font.init()

ai = HandwrittenRecognition()