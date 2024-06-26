import pygame
from tkinter import ttk
from tkinter import Tk
from environment import Field

# Pygame general settings
WIDTH = 1200
HEIGHT = 600
FPS = 120

# Cells settings
cell_size = 8
cell_speed = 100
cell_speed_per_frame = cell_speed / FPS
cells_number = 0

def get_cell_number():
    global cells_number
    try:
        result = int(entry.get())
        cells_number = result
        root.quit()
    except ValueError:
        label.pack()
    

root = Tk()
root.title("Setting")
root.geometry("200x100+400+200")

ttk.Label(text="Enter cell number").pack()

entry = ttk.Entry()
entry.pack()

btn = ttk.Button(text="Click", command=get_cell_number)
btn.pack()

label = ttk.Label(text="Enter an integer")

root.mainloop()
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Socio Life")
clock = pygame.time.Clock()

# Initializing an object that acts as an aggregator of all processes
# The field in which the cells are moved
field = Field(WIDTH, HEIGHT, cell_size, cells_number, cell_speed_per_frame)

# Function of drawing elements on the screen
def drawfield():

    for flag in field.flags:
        rect = pygame.Rect((flag.x, flag.y), (cell_size * 2, cell_size * 2))
        rect.center = (flag.x, flag.y)
        pygame.draw.rect(
            screen,
            (54, 250, 255),
            rect
        )

    for cell in field.cells:
        pygame.draw.circle(
            screen,
            (254, 255, 255),
            (cell.x, cell.y),
            cell_size
        )

# Game loop
running = True
while running and cells_number != 0:

    # Game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            field.put_the_flag(pos[0], pos[1], cell_size) # Creating a flag

    screen.fill(pygame.Color("black"))
    drawfield() # Drawing elements on the screen

    # Initializing cells moving
    if len(field.flags) == 0:
        field.rand_move()
    else:
        field.move_to_flag()

    field.check_collision() # Checking cells for collisions

    clock.tick(FPS)
    pygame.display.set_caption(f"Socio Life | {int(clock.get_fps())} FPS")
    pygame.display.flip()
    