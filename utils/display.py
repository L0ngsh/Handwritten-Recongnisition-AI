from .settings import *

class Display:
    def __init__(self, x, y, width, height, text, fontSize=22, border=False, textColor=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.border = border
        self.textColor = textColor
        self.fontSize = fontSize

    def draw(self, win):
        pygame.draw.rect(win, BLACK if self.border else WHITE, (self.x, self.y, self.width, self.height), 2)
        
        buttonFont = get_font(self.fontSize)
        textSurface = buttonFont.render(self.text, 1, self.textColor)
        win.blit(
            textSurface,
            (self.x + self.width/2 - textSurface.get_width()/2,
                self.y + self.height/2 - textSurface.get_height()/2)
        )