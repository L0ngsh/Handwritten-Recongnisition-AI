from .settings import *

class Button:
    def __init__(self, x, y, width, height, color, text=None, textColor=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.textColor = textColor

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        if self.text:
            pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2)
            
            buttonFont = get_font(22)
            textSurface = buttonFont.render(self.text, 1, self.textColor)
            win.blit(
                textSurface,
                (self.x + self.width/2 - textSurface.get_width()/2,
                 self.y + self.height/2 - textSurface.get_height()/2)
            )

    def clicked(self, pos):
        x, y = pos

        if not (x >= self.x and x < self.x + self.width):
            return False
        if not (y >= self.y and y < self.y + self.height):
            return False
        
        return True    
