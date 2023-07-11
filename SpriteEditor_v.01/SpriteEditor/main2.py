import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import pygame
import Make_Transparent as mt
import ast
import os
import random

clock = pygame.time.Clock()

pixel_animation = []
pixels = []
load_sprite = False

pygame.init()

title = "ICEPIX"
FPS = 60

WINDOW_SIZE = (600, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

screen_division = 2
zoom = screen_division / 2
w1 = WINDOW_SIZE[0] // screen_division
w2 = WINDOW_SIZE[1] // screen_division

window = tk.Tk()
window.title(title)
window.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
window.resizable(False, False)

pygame.display.set_caption(title)
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'  # Set the position of the window (x, y)

screen = pygame.display.set_mode(WINDOW_SIZE, 32)

can_paint = True
current_color = WHITE
def open_sprite():
    global load_sprite, pixels
    res = messagebox.askquestion('Open Sprite', 'Do you want to open a Sprite?')
    if res == 'yes':
        file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                          filetypes=(("Sprite File", "*.sprite"), ("Text Files", "*.txt")))
        if file:
            with open(file, "r") as f:
                pixels = ast.literal_eval(f.read())
            load_sprite = True
    else:
        messagebox.showinfo('Return', 'Returning to the main application')

def pick_color():
    global current_color
    color = colorchooser.askcolor(title="Pick a Color")
    if color[1]:
        current_color = color[1]

def create_pixel(xpos, ypos, color):
    pixels.append([xpos, ypos, [color]])

def clear_pixels():
    global pixels
    pixels = []

def draw_sprite_editor():
    global w1, w2, zoom

    display = pygame.Surface((w1, w2))
    zoom = screen_division / 2
    w1 = WINDOW_SIZE[0] // screen_division
    w2 = WINDOW_SIZE[1] // screen_division

    tag=0
    display.fill(BLACK)
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseX -= mouseX // screen_division * zoom
    mouseY -= mouseY // screen_division * zoom
    mouseX //= zoom
    mouseY //= zoom

    i = 0
    for pixel in pixels:
        if can_paint:
            pygame.draw.rect(display, pixels[i][2][0], pygame.Rect(pixels[i][0], pixels[i][1], 1, 1))
        i += 1

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()

def main_program():
    tag=0
    a=0
    screen_division=2
    mouseX, mouseY = 10,10
    mouse_down = False
    current_color = WHITE
    w1 = WINDOW_SIZE[0] / screen_division
    w2 = WINDOW_SIZE[1] / screen_division
    display = pygame.Surface((w1, w2))
    global pixels, pixel_animation, can_paint

    screen_division = 2
    zoom = screen_division / 2
    w1 = WINDOW_SIZE[0] // screen_division
    w2 = WINDOW_SIZE[1] // screen_division

    moving_right = False
    moving_left = False

    while True:
        draw_sprite_editor()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
                    print(pixels)
                if event.button == 3:
                    screen_division += 2
                if event.button == 2:
                    screen_division -= 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Sprite",
                                                        filetypes=(("Sprite File", "*.sprite"), ("Text Files", "*.txt")))
                    if file:
                        with open(file, "w") as f:
                            f.write(str(pixels))
                if event.key == pygame.K_c:
                    pick_color()
                if event.key == pygame.K_KP1:
                    current_color = WHITE
                if event.key == pygame.K_KP2:
                    current_color = CYAN
                if event.key == pygame.K_KP3:
                    current_color = RED
                if event.key == pygame.K_KP4:
                    print(pixel_animation[a])
                if event.key == pygame.K_KP5:
                    brush_type = "random"
                if event.key == pygame.K_KP6:
                    pygame.image.save(screen, "screenshot.png")
                    mt.transImage("screenshot.png", str(tag) + ".png")
                    tag += 1
                if event.key == pygame.K_KP7:
                    pixel_animation.append(pixels)
                    pixels = []
                if event.key == pygame.K_KP9:
                    count_p = 0
                    import time

                    for p in pixel_animation:
                        count_temp = 0
                        for j in p:
                            pygame.draw.rect(display, pixel_animation[count_p][count_temp][2][0],
                                             pygame.Rect(pixel_animation[count_p][count_temp][0],
                                                         pixel_animation[count_p][count_temp][1], 1, 1))
                            time.sleep(0.5)
                            count_temp += 1
                        count_p += 1
                if event.key == pygame.K_KP8:
                    can_paint = True
                    pixels = pixels[1:-1]
                if event.key == pygame.K_DELETE:
                    pixels = []

        if can_paint and mouse_down:
            create_pixel(mouseX, mouseY, current_color)

if __name__ == "__main__":
    open_sprite()

    canvas = tk.Canvas(window, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])
    canvas.pack()

    open_sprite_button = tk.Button(window, text="Open Sprite", command=open_sprite)
    open_sprite_button.pack()

    color_button = tk.Button(window, text="Pick a Color", command=pick_color)
    color_button.pack()

    clear_button = tk.Button(window, text="Clear Pixels", command=clear_pixels)
    clear_button.pack()

    main_program()

    window.mainloop()
