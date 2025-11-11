import sys
import pygame
import tkinter as tk
from tkinter import filedialog
from auto import automaton

root = tk.Tk()
root.withdraw()

size = width, height = 1000, 564
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (92,92,92)

def mouse_click(world:automaton, mouse_x:int, mouse_y:int) -> None:
    x = int(mouse_x / 10)
    y = int(mouse_y / 10)
    if world.read(x,y) == world.LIVE:
        world.write(x,y,world.DEAD)
    else:
        world.write(x,y,world.LIVE)

def main():
    pygame.init()
    pygame.font.init()
    world = automaton()
    print(world)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Autómatas Celulares")

    play = pygame.image.load("play.png")
    playrect = play.get_rect()
    playrect = playrect.move(404,500)
    
    pause = pygame.image.load("pause.png")
    pauserect = pause.get_rect()
    pauserect = pauserect.move(468, 500)
        
    clear = pygame.image.load("clear.png")
    clearrect = clear.get_rect()
    clearrect = clearrect.move(532,500)
    
    load = pygame.image.load("load.png")
    loadrect = load.get_rect()
    loadrect = loadrect.move(596,500)
    
    save = pygame.image.load("save.png")
    saverect = save.get_rect()
    saverect = saverect.move(660,500)

    myfont = pygame.font.SysFont("Minecraft", 30)

    running = False

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("fin :p")
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if y <=500:
                    mouse_click(world,x,y)
                else: 
                    if playrect.collidepoint(x,y):
                        running=True
                    if pauserect.collidepoint(x,y):
                        running=False
                    if clearrect.collidepoint(x,y):
                        world.reset()
                    if loadrect.collidepoint(x,y):
                        file_path_string = filedialog.askopenfilename(filetypes=(
                            ("Conway GoL files", "*.cgl"),
                            ("All files", "*.*")
                            ))
                        if file_path_string != "":
                            world.load(file_path_string)
                    if saverect.collidepoint(x,y):
                        file_path_string=filedialog.asksaveasfilename(
                            filetypes=(
                                ("Conway GoL files", "*.cgl"),
                                ("All files", "*.*")
                                ))
                        if file_path_string != "":
                            world.save(file_path_string)

        if running:
            world.update()

        screen.fill(BLACK)
        world.draw(screen)
        screen.blit(play, playrect)
        screen.blit(pause, pauserect)
        screen.blit(clear, clearrect)
        screen.blit(load, loadrect)
        screen.blit(save, saverect)

        textsurface = myfont.render("Running" if running else "Pause", True, WHITE)
        screen.blit(textsurface, (100,516))
        screen.blit(
            myfont.render(str(world.iterations), True, WHITE), (750, 516))
        screen.blit(
            myfont.render(str(world.livecells), True, WHITE), (850, 516))  

        pygame.display.flip()

if __name__ == "__main__":
    main()