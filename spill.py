import pygame
import json 
from enum import Enum, auto

from button import Button
from button import GitButton
from enemy import Enemy
from turret import Turret 
from world import World
import constants as c

class State(Enum):
    RUNNING = auto()
    LOST = auto()
    MENU = auto()
    PAUSED = auto()

#1. Oppsett
pygame.init()

# CONSTANTS
ROWS, COLS = 15, 15
TILE_SIZE = 48
SIDE_PANEL = 300
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS   * TILE_SIZE
FPS = 60

button_font = pygame.font.SysFont("Times New Roman", 25)
backgroundcolor = (255,255,255)
screen = pygame.display.set_mode((WIDTH + SIDE_PANEL, HEIGHT))
clock = pygame.time.Clock()
state = State.MENU

score = 0

# IMAGES
map_image = pygame.image.load("levels/level.png")

cursor_turret = pygame.image.load("images/turrets/cursor_turret.png").convert_alpha( )

enemy_1_img = pygame.image.load("images/enemies/enemy_1.png").convert_alpha()
enemy_2_img = pygame.image.load("images/enemies/enemy_2.png").convert_alpha()
enemy_3_img = pygame.image.load("images/enemies/enemy_3.png").convert_alpha()
enemy_4_img = pygame.image.load("images/enemies/enemy_4.png").convert_alpha()

buy_turret_image = pygame.image.load("images/buttons/buy_turret.png")
cancel_image = pygame.image.load("images/buttons/cancel.png")

with open("levels/level.tmj") as file:
    world_data = json.load(file)

def create_turret(mousepos):
    mouse_tile_x = mouse_pos[0] // TILE_SIZE
    mouse_tile_y = mouse_pos[1] // TILE_SIZE
    # Calculate the number of the tile
    mouse_tile_num = (mouse_tile_y * COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free == True:
            turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y )
            turret_group.add(turret)

# WORLD
world = World(world_data, map_image)
world.process_data()

# TURRET
turret_group = pygame.sprite.Group()

# ENEMY
enemy_group = pygame.sprite.Group()
enemy = Enemy(world.waypoints, enemy_1_img)
 
# CREATE GROUPS
enemy_group.add(enemy) 

turret_button = GitButton( WIDTH+30, 120, buy_turret_image)
cancel_button = GitButton(WIDTH+50, 180, cancel_image)


while state == State.RUNNING or state == State.MENU or state == State.LOST or state == State.PAUSED or state == True:
    # MENU
    if state == State.MENU:
        knapp = Button(WIDTH/2-50, HEIGHT/2-20, 100, 40, (255,0,0), "SPILL", (255,255,255), button_font, State.RUNNING)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if knapp.rect.collidepoint(event.pos):
                    state = knapp.newstate
            if state == None:
                state = State.MENU
        screen.fill((backgroundcolor))
        knapp.draw(screen)

    # RUNNING
    if state == State.RUNNING:

        ####################
        # UPDATING SECTION #
        ####################
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # CHECK IF MOUSE IN GAME AREA
                if mouse_pos[0] < WIDTH and mouse_pos[1] < HEIGHT:
                    create_turret(mouse_pos)
        enemy_group.update()
        
        ###################
        # DRAWING SECTION #
        ###################
        screen.fill((backgroundcolor))
        
        world.draw(screen)
        enemy_group.draw(screen) 
        turret_group.draw(screen)
        if turret_button.draw(screen) == True:
            pass
        if cancel_button.draw(screen) == True:
            pass

    # UPDATE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = False
            pygame.quit()
            raise SystemExit
    pygame.display.flip()
    clock.tick(60)