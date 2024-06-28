from utils import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Handwritten Recongnisition AI')

def initGrid(rows, cols, color):
    grid = [];
    for r in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[r].append(color)

    return grid

def drawGrid(win, grid, drawGridLines):
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (10 + c * PIXEL_SIZE, 10 + r * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if drawGridLines == 1:
        for r in range(ROWS + 1):
            pygame.draw.line(win, WHITE, (10, r * PIXEL_SIZE + 10), (ROWS * PIXEL_SIZE + 10, r * PIXEL_SIZE + 10))
        for j in range(COLS + 1):
            pygame.draw.line(win, WHITE, (j * PIXEL_SIZE + 10, 10), (j * PIXEL_SIZE + 10, COLS * PIXEL_SIZE + 10))


def draw(win, grid, buttons, drawGridLines, displays):
    win.fill(WHITE)
    drawGrid(win, grid, drawGridLines)

    for button in buttons:
        button.draw(win)
    for display in displays:
        display.draw(win)

    pygame.display.update()

def getRowAndColFromPos(pos):
    y, x = pos
    x -= 10
    y -= 10

    r = x // PIXEL_SIZE
    c = y // PIXEL_SIZE

    r1 = r
    r2 = r + 1
    c1 = c
    c2 = c + 1
    
    rcs = [
        [r1, c1],
        [r1, c2],
        [r2, c2],
        [r2, c1]
    ]

    rowsAndCols = []
    for rc in rcs:
        if (rc[0] <= ROWS and rc[1] <= COLS) and (rc[0] >= 0 and rc[1] >= 0):
            rowsAndCols.append(rc)
    
    if len(rowsAndCols) == 0:
        raise IndexError

    return rowsAndCols

def getColorByAccuracy(accuracy):
    return (255 - 255 * accuracy, 255 * accuracy, 0)

run = True
clock = pygame.time.Clock()
drawGridLines = -1
grid = initGrid(ROWS, COLS, BG_COLOR)

buttons = [
    Button(10, DRAW_HEIGHT + 20, 80, 80, WHITE, 'Clear'),
    Button(100, DRAW_HEIGHT + 20, DRAW_WIDTH - 180, 80, WHITE, 'Verify Digit'),
    Button(DRAW_WIDTH - 70, DRAW_HEIGHT + 20, 80, 80, WHITE, 'Grid'),
    Button(DRAW_WIDTH + 20, DRAW_HEIGHT + 20, 245, 80, WHITE, 'Train'),
    Button(DRAW_WIDTH + 275, DRAW_HEIGHT + 20, 245, 80, WHITE, 'Test')
]

displayStartX = DRAW_WIDTH + 20
displayXTotal = WIDTH - 20 - DRAW_WIDTH 
displays = [
    Display(displayStartX, 10, displayXTotal, 50, 'AI Handwritted Recognition', 36),
    Display(displayStartX, 95, displayXTotal, 50, 'Prediction:'),
    Display(displayStartX + displayXTotal / 2 - 125, (DRAW_HEIGHT - 100) / 2 - 70 + 10, 250, 250, '', 250, True),
    Display(displayStartX + 10, DRAW_HEIGHT + 10 - 50, 250, 50, '', 22),
    Display(displayStartX + 20 + 250, DRAW_HEIGHT + 10 - 50, 250, 50, '', 22),
]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            drawingColor =  WHITE if pygame.mouse.get_pressed()[0] else BLACK
            pos = pygame.mouse.get_pos()
            try:
                for rc in getRowAndColFromPos(pos):
                    grid[rc[0]][rc[1]] = drawingColor
            except IndexError:
                if pygame.mouse.get_pressed()[0]:
                    for button in buttons:
                        if not button.clicked(pos):
                            continue
                        
                        match button.text: 
                            case 'Clear':
                                grid = initGrid(ROWS, COLS, BG_COLOR)
                            case 'Grid':
                                drawGridLines  *= -1
                            case 'Verify Digit':
                                try:
                                    digit, prediction = ai.run(grid)
                                    displays[2].text = str(digit) 
                                    displays[3].text = ''
                                    displays[4].text = ''
                                    displays[4].textColor = BLACK
                                except Exception as e:
                                    print(e)
                                    displays[3].text = 'Analysis Error:'
                                    displays[4].text = str(e)
                                    displays[4].textColor = RED
                            case 'Train':
                                displays[3].text = 'Training:'
                                displays[4].text = 'Wait...'
                                displays[4].textColor = BLACK
                                draw(WIN, grid, buttons, drawGridLines, displays)
                                if ai.train():
                                    displays[4].text = 'Complete'
                                    displays[4].textColor = GREEN
                                else:
                                    displays[4].text = 'Error, try again'
                                    displays[4].textColor = RED
                            case 'Test':
                                displays[3].text = 'Testing:'
                                displays[4].text = 'Wait...'
                                displays[4].textColor = BLACK
                                draw(WIN, grid, buttons, drawGridLines, displays)
                                try:
                                    accuracy = ai.test()
                                    displays[3].text = 'Test accuracy:'
                                    displays[4].text = f"{accuracy * 100}%"
                                    displays[4].textColor = getColorByAccuracy(accuracy)
                                except Exception as e:
                                    displays[3].text = 'Testing Error:'
                                    displays[4].text = str(e)
                                    displays[4].textColor = RED
                else:
                    pass

    draw(WIN, grid, buttons, drawGridLines, displays)

pygame.quit()