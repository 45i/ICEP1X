
from showMessage import *
from pygame import *
from setup import *
import ast
from tkinter import colorchooser, filedialog
import pygame
import sys
import os
import random
import pyautogui
from pyautogui import *
from tkinter import *
from PIL import Image

clock = pygame.time.Clock()

#initial_setup()
layercode=1
layers=1
lastlayer=0
pixel_animation = {}

a = 0

pixels = []
history={}
history_count = 0
load_sprite = False
WINDOW_SIZE=0

# #print("do you want to load a sprite?")
# action = input()
# if action == "yes":
#     #print("what file do you want to load?")
#     f_file = input()
#     arr = os.listdir()
#     if f_file in arr:
#         f = open(f_file)
#         load_data = []
#         load_data.append(ast.literal_eval(f.read()))
#         f.close()
#         pixels.append(load_data[a])
#         pixels = pixels[a]
#         #print(pixels)
#         load_sprite = True
#     else:
#         #print("there is no file with that name.")
pygame.init()
def Initialise():
    RunMainLoop()
    
FPS = 120000
pygame.display.set_caption("ICEP1X")
screen = pygame.display.set_mode((0, 0),0)
WINDOW_SIZE = (pygame.display.get_window_size()[0], pygame.display.get_window_size()[1])
pygame.display.set_mode(WINDOW_SIZE,0,vsync=FPS)
title = "ICEPIX"


# Set the position of the window (x, y)
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'


SPEED = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)


#screen = pygame.display.set_mode(WINDOW_SIZE,0, 32)
screen_division = 2
zoom = 10
w1 = WINDOW_SIZE[0] / screen_division
w2 = WINDOW_SIZE[1] / screen_division

window_pixels = WINDOW_SIZE
# Scaling Resolution
display = pygame.Surface((w1, w2))
altpressed=False
altwaspressed=False
moving_right = False
moving_left = False
root = Tk()
root.withdraw()
last_saved_file=""
saved_file=""
willshowprompt=True
history[len(history)]=pixels.copy()
import sys
def readData (file):
    global display,pixel_animation,pixels, load_sprite, a,last_saved_file,saved,layercode,layers,history_count,history
    if file != "":
        if os.path.splitext(file)[1] == ".sprite" or os.path.splitext(file)[1] == ".txt":
            f = open(file, "r")
            load_data = {}
            load_data=(ast.literal_eval(f.read()))
            f.close()
            pixel_animation=load_data
            if layercode in pixel_animation.keys():
                pixels = pixel_animation[layercode]
            else:
                pixels = []
            
            load_sprite = True
            # display.fill(BLACK)
            last_saved_file=file
            saved=False
            layers = len(pixel_animation)
            history_count=0
            history={}
        elif os.path.splitext(file)[1] == ".png":
            # background_image = pygame.image.load(file)

            # # Blit image onto display surface
            # display.blit(background_image, (0, 0))
            # pygame.display.update()
            im = Image.open(file, 'r')
            pix_val = list(im.getdata())
            for i in range(0,WINDOW_SIZE[0]):
                for j in range(0,WINDOW_SIZE[1]):
                    pixels[i][j]=pix_val[i][j]

    else:
        pixels=[]
    

def openFile( display):
    global pixel_animation,pixels, load_sprite, a,last_saved_file,saved,layercode,layers
    file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(
        ("Sprite File", "*.sprite"), ("Text Files", "*.txt")
        , ("PNG Files", "*.png")))
    readData(file)
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if filename.endswith(".sprite")or filename.endswith(".png"):
        # Open the file and do something with it
        print("Opening file: " + filename)
        willshowprompt=False
        readData(filename)
    
    

saved = False
def create_controls_file():
    
    
    # Create a new surface for the controls
    # help_text = "Pygame Controls:\n"
    # help_text += "----------------\n"
    help_text = f"Ctrl+Z: Undo\n"
    help_text += f"Ctrl+S: Save\n"
    help_text += f"Ctrl+M: Make Transparent Image\n"
    help_text += f"Ctrl+R: Render\n"
    help_text += f"Scroll Up/Down: Change Brush Size\n"
    help_text += f"Alt: Toggle Brush Visibility\n"
    help_text += f"Escape: Reset Canvas, Open Sprite or Exit\n"
    help_text += f"Shift+Click: Pick Color At Mouse Position In Canvas\n"
    help_text += f"Left/Right Arrow Keys: Change/Create Layers\n"
    help_text+=f"g: Make GIF [From Layers]]\n"
    help_text+=f"Up/Down Arrow Keys: Merge Layers Up/Down\n"
    help_text+=f"Shift+M: Merge All Layers\n"
    help_text+=f"c: Pick Color\n"



    # Create a temporary file and write the controls to it
    # with open(os.getcwd()+"\\temp.txt","w") as f:
    #     f.write(help_text)

    # # Open the temporary file with the default text editor

    # subprocess.run(["notepad.exe", os.getcwd() + "\\temp.txt"])

    # # Delete the temporary file
    # os.remove(os.getcwd()+"\\temp.txt")
    

    showAlert(help_text,button="Ok, I got it!")

if willshowprompt:
    res = showYesNo( 'Do you want to open a Sprite?')

    if res == 'Yes':

        openFile(display)
    else:
        showAlert('Returning to main application',button="OK")
        pixels=[]

history[len(history)]=pixels.copy()
current_color = WHITE

can_paint = True

def createPixel(xpos, ypos, color, pixel_size):
    global pixels
    pixels.append([xpos, ypos, [color], pixel_size])
    global saved, saved_file,last_saved_file,pixel_animation
    pixels_temp={}
    if saved:
        try:
            f = open(last_saved_file, "r")
            load_data={}
            load_data=(ast.literal_eval(f.read()))
            f.close()
            pixels_temp=(load_data)

            if pixel_animation!=pixels_temp:
                saved=False
                last_saved_file=saved_file
                saved_file=""

            else:
                saved=True
                saved_file=last_saved_file
        except:
            saved=False
            last_saved_file=saved_file
            saved_file=""
    else:
        saved=False
        last_saved_file=saved_file
        saved_file=""


random_colors = [WHITE, RED, CYAN, WHITE]

brush_type = "normal"
size_pixels = 7

tag = 0

mouseX, mouseY = 10, 10
mouse_down = False
clock = pygame.time.Clock()

BAR_HEIGHT = 30
selected_color = (255, 255, 255)
pixel_size = 1

# Font setup
fonty = pygame.font.SysFont("None",24)
color_text =pixel_text=mouse_text=""
current_history=[]
TextMode=False
def renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels, panX, panY):
    i = 0
    global count_error
    for j in range(0,len(pixels)):
        
            if can_paint == True:
                if altpressed==True: pygame.draw.rect(display, current_color, pygame.Rect(mouseX,mouseY, size_pixels, size_pixels))
                        
                if True:
                    try:    
                        pygame.draw.rect(display, pixels[j][2][0], pygame.Rect(
                            pixels[j][0], pixels[j][1], pixels[j][3], pixels[j][3]))
                    except:
                        pygame.draw.rect(display, pixels[j][2][0], pygame.Rect(
                            pixels[j][0], pixels[j][1], 1, 1))
                        count_error += 1
                        if count_error <= 1:
                            error = True
        #             i += 1
        # j+=1
            

        
        
# def renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels):
#     surface = pygame.Surface((len(pixels), len(pixels[0])))
#     for x in range(len(pixels)):
#         for y in range(len(pixels[0])):
#             surface.set_at((x, y), pixels[x][y])
#     scaled_surface = pygame.transform.scale(surface, (int(len(pixels)*zoom), int(len(pixels[0])*zoom)))
#     display.blit(scaled_surface, (mouseX - (mouseX - scaled_surface.get_width() // 2), mouseY - (mouseY - scaled_surface.get_height() // 2)))
#     pygame.draw.rect(display, WHITE, (0, WINDOW_SIZE[1] - 20, WINDOW_SIZE[0], 20))
#     font = pygame.font.Font(None, 20)
#     text = font.render(f"Zoom: {zoom:.2f}x | Pixel Size: {size_pixels}px | Mouse Position: ({mouseX}, {mouseY})", True, BLACK)
#     display.blit(text, (10, WINDOW_SIZE[1] - 20))
##outer:
pixels_last = []
def saveFile():
                            global saved_file,saved,last_saved_file
                            if saved==False:
                                file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Create file", filetypes=(
                                    ("Sprite File", "*.sprite"),)).replace(".sprite", "")
                                if file != "":
                                    with open(file+(".sprite"if ".sprite" not in file else ""), "w") as f:
                                        f.write(str(pixel_animation))
                                    f.close()
                                    saved=True
                                    saved_file=file+".sprite"
                            else:
                                with open(saved_file+(".sprite"if ".sprite" not in saved_file else ""), "w") as f:
                                    f.write(str(pixel_animation))
                                f.close()
                            last_saved_file=saved_file
                            saved=True
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]
def string_to_pixels(text, color, size):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    pixels = pygame.surfarray.array2d(surface)
    return pixels
def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"
def RunMainLoop():
    global can_paint,mouse_down,brush_type,mouseX,mouseY,current_color,size_pixels,color_text,mouse_text,pixel_text,layercode,layers,pixels,screen,w1,w2,screen_division,pixels_last,error,altpressed,history_count,SPEED,pixel_animation,saved_file,tag,count_error,altwaspressed
    import os
    while True:
        surf = pygame.Surface ((WINDOW_SIZE[0], WINDOW_SIZE[1]))
        if can_paint == True:
                if mouse_down == True:
                    if brush_type == "normal":
                        createPixel(mouseX, mouseY, current_color, size_pixels)
                        current_history.append([mouseX, mouseY, current_color, size_pixels])
                    else:
                        createPixel(
                            mouseX, mouseY, random_colors[random.randint(0, 3)], size_pixels)
    
    
        update=False
        
    
        # Draw the bottom bar
        final_text=""
        info_text=""
        # Render and display the text
        if color_text!=f"Color: RGB{current_color if '#' not in current_color else hex_to_rgb(current_color)}":
            update=True
            color_text = f"Color: RGB{current_color if '#' not in current_color else hex_to_rgb(current_color)}"
        if color_text!=f"Pixel Size: {size_pixels}":    
            update=True
            pixel_text = f"Pixel Size: {size_pixels}"
        if mouse_text!=f"Mouse Position: {pygame.mouse.get_pos()}":
            update=True
            mouse_text = f"Mouse Position: {pygame.mouse.get_pos()}"
        final_text = color_text + " | " + pixel_text + " | " + mouse_text + " | " + f"Brush Type: {brush_type}" + " | "+f"{info_text if info_text!='' else '...'} | "+f"Layer: {layercode} of {layers}"+f" | "+f"FPS: {int(clock.get_fps())}"+" | "+f"{len(pixels)} pixels in scene"+" | "+"Press F1 for controls" 
        final_surface = fonty.render(final_text, True, (255, 255, 255)) 
        #  color_surface = font.render(color_text, True, (255, 255, 255))
        # pixel_surface = font.render(pixel_text, True, (255, 255, 255))
        # mouse_surface = font.render(mouse_text, True, (255, 255, 255))
        
        screen.blit(final_surface, (10, WINDOW_SIZE[1] - BAR_HEIGHT + 5))
        # screen.blit(color_surface, (10, WINDOW_SIZE[1] - BAR_HEIGHT + 5))
        # screen.blit(pixel_surface, (250, WINDOW_SIZE[1] - BAR_HEIGHT + 5))
        # screen.blit(mouse_surface, (400, WINDOW_SIZE[1] - BAR_HEIGHT + 5))
        if update: pygame.display.update()
        
    
        display = pygame.Surface((w1, w2))
        zoom = screen_division / 2
        w1 = WINDOW_SIZE[0] / screen_division
        w2 = WINDOW_SIZE[1] / screen_division
        rel = pygame.mouse.get_rel()
        speed = (rel[0]**2 + rel[1]**2)**0.5
        FPS = pow(int(speed), 3)*100
        
        if FPS >= 100:
            FPS = 100
        clock.tick(FPS)
    
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX -= mouseX / screen_division * zoom
        mouseY -= mouseY / screen_division * zoom
    
        mouseX /= zoom
        mouseY /= zoom
        
        mouseX-= size_pixels/2
        mouseY-= size_pixels/2
        i = 0
        count_error=0
        if pixels_last != pixels or i == 0:
            renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels,pygame.mouse.get_rel()[0],pygame.mouse.get_rel()[1])
            pixels_last = pixels
        if error==True:
            # mb.showinfo('Error', 'There was an error loading the sprite\nPixel width information was not found\nDefaulting to 1x1 pixels')
            error=False
        for event in pygame.event.get():
            if pygame.key.get_mods() & KMOD_SHIFT:
                altwaspressed=altpressed
                altpressed=False
            else:
                altpressed=altwaspressed 
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.WINDOWRESIZED:
                ##print(event.dict['x'], event.dict['y'])
                coords = (event.dict['x'], event.dict['y'])
                screen = pygame.display.set_mode((pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]),0, 32)
                display = pygame.Surface(
                    (pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not pygame.key.get_mods() & KMOD_SHIFT:
                    mouse_down = True
                    history_count+=1
                elif event.button == 1 and pygame.key.get_mods() & KMOD_SHIFT:
                        color_at_mouse_pos = display.get_at((int(mouseX), int(mouseY)))
                        
                        current_color= (color_at_mouse_pos.r,color_at_mouse_pos.g,color_at_mouse_pos.b)
                        #print(current_color)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    
                    if TextMode==False:
                        mouse_down = False
                        #print(pixels)
                        history[len(history)]=pixels.copy()
                    else:
                        res=pyautogui.prompt('Text:', 'Text Mode') # type: ignore
                        if res!=None:
                            text=res
                            text_pixels=string_to_pixels(text,current_color,size_pixels)
                            pixels.extend(text_pixels)
                    
                    
                if event.button == 2 and screen_division > 2:
                    screen_division -= 2
                if event.button == 3:
                    screen_division += 2
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    if pygame.key.get_mods() & KMOD_CTRL:
                        SPEED += 10
                    else:
                        size_pixels += 2
                if event.y == -1:
                    if pygame.key.get_mods() & KMOD_CTRL and SPEED > 10:
                        SPEED -= 10
                    else:
                        size_pixels -= 2
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    if (layers not in pixel_animation.keys()):pixel_animation[layers]=pixels.copy()
                    if layercode!=1:
                        pixel_animation[layercode-1].extend(pixels)
                        pixels=pixel_animation[layercode-1].copy()
                        for i in range(layercode,layers):
                            pixel_animation[i]=pixel_animation[i+1].copy()
                        pixel_animation[layers].clear()
                        layercode-=1
                        layers-=1
                if event.key == K_DOWN:
                    
                    if layercode!=layers:
                        pixel_animation[layercode+1].extend(pixels)
                        pixels=pixel_animation[layercode+1].copy()
                        for i in range(layercode,layers):
                            pixel_animation[i]=pixel_animation[i+1].copy()
                        pixel_animation[layers].clear()
                        layers-=1
                if event.key == K_F1:
                    
                    
                    res = showYesNo( "Would you like to see the controls?")
                    if res=='Yes':
                        create_controls_file()
                if event.key==K_l and pygame.key.get_mods() & KMOD_CTRL:
                    res=pyautogui.prompt('Layer Number:', 'Layer Number') # type: ignore
                if event.key == K_g:
                    images = []
                    finalgifset=[]
                    lastlayercode=layercode
                    pixel_animation[layercode]=pixels.copy()
                    pixels=[]
                    renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels,pygame.mouse.get_rel()[0],pygame.mouse.get_rel()[1])
                    alert("Please wait while the GIF is being generated\nThis may take a while depending on the size of the sprite",button="Ok, I'll Wait!") # type: ignore
                    for layer in pixel_animation:
                        # Clear the display surface
                        renderPixels(pixel_animation[layer].copy(), display, zoom, mouseX, mouseY, size_pixels, pygame.mouse.get_rel()[0], pygame.mouse.get_rel()[1])
                        pygame.image.save(display, f"{layer}.png")
                        images.append(f"{layer}.png")
                    from PIL import Image
    
                    for image in images:
                        finalgifset.append(Image.open(image))
                    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Image", filetypes=(
                        ("GIF file", "*.gif"),)).replace(".gif","")
                    file_extension = "" if ".gif" in file else ".gif"
                    gg=prompt("Please enter the duration of each frame in milliseconds",title="GIF Duration",default=20) # type: ignore
                    finalgifset[0].save(f"{file}{file_extension}", save_all=True, append_images=finalgifset[1:], duration=eval(gg), loop=0)
                    for filename in images:
                        os.remove(filename)
                if event.key == K_ESCAPE:
                    res = showMsgCustom("Select Action",["Reset Canvas","Open Sprite","Exit"])
                    if res=='Reset Canvas':
                        pixels = []
                        renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels,pygame.mouse.get_rel()[0],pygame.mouse.get_rel()[1])
                        save = False
                        saved_file = ""
                    elif res=='Open Sprite':
                        if saved==False:
                            res =showYesNo( "Would you like to save the sprite?")
                            if res=='Yes':
                                saveFile()
                            else :
                                openFile(display)
                        else:
                            openFile(display)     
                    else:
                            pygame.quit()
                            sys.exit()
                    
                    #  pygame.draw.rect(display, current_color, pygame.Rect(mouseX,mouseY, size_pixels, size_pixels))
                    # rectangle = pygame.Rect(100, 100, 200, 100)
    
                    # mouse_x, mouse_y = pygame.mouse.get_pos()
                    # mouse_rect = pygame.Rect(mouseX, mouseY, 1, 1) 
                    
                    # if rectangle.colliderect(mouse_rect):
                    #     # Get the color of the rectangle at the mouse position
                    #     relative_mouse_x = mouse_x - rectangle.x
                    #     relative_mouse_y = mouse_y - rectangle.y
                        
                if event.key == K_z and pygame.key.get_mods() & KMOD_CTRL and len(history)>1:
                    pixels = history[len(history)-2].copy()
                    
                    history.pop(len(history)-1)
                    renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels,pygame.mouse.get_rel()[0],pygame.mouse.get_rel()[1])
                if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    if saved==False:
                        saveFile()
                    else:
                        with open(saved_file+(".sprite"if ".sprite" not in saved_file else ""), "w") as f:
                            f.write(str(pixel_animation)) # type: ignore
                        f.close()
                if event.key == K_c:
                    color = colorchooser.askcolor(title="Pick a Color")
                    if color[1]:
                        #print("Selected color:", color[1])
                        current_color = color[1]
                        root = Tk()
                        root.withdraw()
    
                if event.key == pygame.K_KP1:
                    screen.fill(BLACK)
                    pygame.display.flip()
                if event.key == pygame.K_KP2:
                    brush_type = "normal"
                    current_color = CYAN
                if event.key == pygame.K_KP3:
                    brush_type = "normal"
                    current_color = RED
                #if event.key == pygame.K_KP4:
                    #print()
                    #print()
                    #print(pixel_animation[a])
                if event.key == pygame.K_KP5:
                    brush_type = "random"
                if event.key == pygame.K_m and pygame.key.get_mods() & KMOD_CTRL:
                    
                    color = colorchooser.askcolor(title="Pick a Transparency Key",initialcolor=rgb_to_hex(current_color))
                    if color[1]:
                        
                        if color[1]:
                            current_color = color[1]
                            root = Tk()
                            root.withdraw()
                        transparency_key = hex_to_rgb(color[1])
                        root = Tk()
                        root.withdraw()
                        altwaspressed=altpressed
                        altpressed=False
                        file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Image", filetypes=(
                        ("PNG file", "*.png"),)).replace(".png","")
                        file_extension = "" if ".png" in file else ".png"
                        pygame.image.save(display, file+file_extension )
                        ##print(mt.transImage(file + file_extension, file + "_transparent"+file_extension, transparency_key))
                        import os
    
                        if os.path.exists(file + file_extension):
                            os.remove(file + file_extension)
                if  pygame.key.get_mods() & KMOD_ALT:        
                    altpressed=True if altpressed==False else False
                    altwaspressed=altpressed
                if event.key == pygame.K_m and pygame.key.get_mods() & KMOD_SHIFT:
                    res = showYesNo( "Are you sure you want to merge all the layers?")
                    if res=='Yes':
                        tmp=0
                        for layer in pixel_animation:
                            pixels.extend(pixel_animation[layer])
                            tmp+=1
                        layers=1
                        layercode=1
                        pixel_animation={}
                        pixel_animation[1]=pixels
                    renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels,pygame.mouse.get_rel()[0],pygame.mouse.get_rel()[1])
    
                if event.key == pygame.K_r and pygame.key.get_mods() & KMOD_CTRL:
                    #pygame.draw.rect(display, BLACK, pygame.Rect((0, WINDOW_SIZE[1] - BAR_HEIGHT, WINDOW_SIZE[0], BAR_HEIGHT)))
                    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Image", filetypes=(
                        ("PNG file", "*.png"),)).replace(".png","")
                    file_extension = "" if ".png" in file else ".png"
                    if file != "":
                        pygame.image.save(display, file + file_extension)
                        # info_text = mt.transImage(file + file_extension, file + "_" + str(tag) + file_extension)
                        tag += 1
    
                        # New Frame of Animation
                if event.key == pygame.K_RIGHT:
                    if layercode==layers:
                        pixel_animation[layercode]=pixels
                        layercode += 1
                        pixels = []
                        renderPixels(pixels, display, zoom, mouseX, mouseY, size_pixels,pygame.mouse.get_rel()[0],pygame.mouse.get_rel()[1])
                        layers+=1
                    else:
                        if (layercode not in pixel_animation.keys()):
                            pixel_animation[layercode]=pixels
                        layercode += 1
                        pixels = pixel_animation[layercode]
                        
    
                            
                if event.key == pygame.K_LEFT:
                    pixel_animation[layercode]=pixels
                    if (layercode-1  in pixel_animation.keys()):
                        pixels=pixel_animation[layercode-1]
                        layercode -= 1
                            
                
                # Play Animation
                if event.key == pygame.K_KP9:
                    count_p = 0
                    import time
                    for p in pixel_animation:
                        count_temp = 0
                        for j in p:
                            pygame.draw.rect(display, pixel_animation[count_p][count_temp][2][0], pygame.Rect(
                                pixel_animation[count_p][count_temp][0], pixel_animation[count_p][count_temp][1], 1, 1))
                            time.sleep(0.5)
                            count_temp += 1
                        count_p += 1
                    # can_paint = False
                    # a = 0
                    # if can_paint == False:
                    #     pixels = []
                    #     p = 0
                    #     while p != (len(pixel_animation[a][p]) - 1):
                    #         createPixel(pixel_animation[a][p][0],pixel_animation[a][p][1],pixel_animation[a][p][2][0])
                    #         p += 1
                    #         a += 1
                    #         if a > (len(pixel_animation) - 1):
                    #             a = 0
                if event.key == pygame.K_KP8:
                    can_paint = True
                    pixels = pixels[1:-1]
                if event.key == pygame.K_DELETE:
                    pixels = []
    
            
        surf = pygame.transform.scale(display, (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    
        screen.blit(surf, (0, 0))
        #pygame.display.flip()
        pygame.display.update()
    
        clock.tick(FPS)
    
    
        pygame.draw.rect(screen, (50, 50, 50), (0, WINDOW_SIZE[1] - BAR_HEIGHT, WINDOW_SIZE[0], BAR_HEIGHT))


    
