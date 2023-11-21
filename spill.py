import pygame
import json 
import sys
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

# GAME VARIABLES
game_over = False
game_outcome = 0  # -1 is a loss 1 is a win
level_started = False
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None
sound = True
backgroundcolor = (255,255,255)
screen = pygame.display.set_mode((c.WIDTH + c.SIDE_PANEL, c.HEIGHT))
clock = pygame.time.Clock()
state = State.MENU
score = 0

dy_list = {
    "T": {
        "dy": 1,
        "speed": 0.5
    },
    "O": {
        "dy": 11,
        "speed": 0.5
    },
    "W": {
        "dy": 21,
        "speed": 0.5
    },
    "E": {
        "dy": 31,
        "speed": 0.5
    },
    "R": {
        "dy": 39,
        "speed": -0.5
    }
}

# IMAGES
map_image = pygame.image.load("levels/level.png")

cursor_turret = pygame.image.load("images/turrets/cursor_turret.png").convert_alpha()
#TURRET SPRITESHEET
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pygame.image.load(f"images/turrets/turret_{x}.png").convert_alpha() 
    turret_spritesheets.append(turret_sheet)

#enemies
enemy_images = {
    "weak": pygame.image.load("images/enemies/enemy_1.png").convert_alpha(),
    "medium": pygame.image.load("images/enemies/enemy_2.png").convert_alpha(),
    "strong": pygame.image.load("images/enemies/enemy_3.png").convert_alpha(),
    "elite": pygame.image.load("images/enemies/enemy_4.png").convert_alpha(),
}
enemy_1_img = pygame.image.load("images/enemies/enemy_1.png").convert_alpha()
enemy_2_img = pygame.image.load("images/enemies/enemy_2.png").convert_alpha()
enemy_3_img = pygame.image.load("images/enemies/enemy_3.png").convert_alpha()
enemy_4_img = pygame.image.load("images/enemies/enemy_4.png").convert_alpha()

buy_turret_image = pygame.image.load("images/buttons/buy_turret.png").convert_alpha()
cancel_image = pygame.image.load("images/buttons/cancel.png").convert_alpha()
upgrade_turret_image = pygame.image.load("images/buttons/upgrade_turret.png").convert_alpha()
begin_image = pygame.image.load("images/buttons/begin.png").convert_alpha()
restart_image = pygame.image.load("images/buttons/restart.png").convert_alpha()
fast_forward_image = pygame.image.load("images/buttons/fast_forward.png").convert_alpha()
# gui
coin_image = pygame.image.load("images/gui/coin.png").convert_alpha()
heart_image = pygame.image.load("images/gui/heart.png").convert_alpha()
sound_on_image = pygame.image.load("images/gui/sound_on.png").convert_alpha()
sound_on_image = pygame.transform.scale_by(sound_on_image, 0.05)
sound_off_image = pygame.image.load("images/gui/sound_off.png").convert_alpha()
sound_off_image = pygame.transform.scale_by(sound_off_image, 0.05)

# load sounds
shot_fx = pygame.mixer.Sound("sound/shot.wav")
shot_fx.set_volume(0.5)

theme_song = pygame.mixer.Sound("sound/theme.wav")
theme_song.play(loops=-1)




with open("levels/level.tmj") as file:
    world_data = json.load(file)

# LOAD FONTS
button_font = pygame.font.SysFont("Consolas", 25)
text_font = pygame.font.SysFont("Consolas", 24, bold = True)
large_font = pygame.font.SysFont("Consolas", 36)
logo_font = pygame.font.SysFont("Consolas", 70)
menu_font = pygame.font.SysFont("Consolas", 100)

# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def display_data():
    # DRAW PANEL
    pygame.draw.rect(screen, "maroon", (c.WIDTH, 0, c.SIDE_PANEL, c.HEIGHT))
    pygame.draw.rect(screen, "grey0", (c.WIDTH, 0, c.SIDE_PANEL, 400), 2)
    pygame.draw.rect(screen, (131, 3, 173), (c.WIDTH, 400, c.SIDE_PANEL, c.HEIGHT-400))

    draw_text("TOWER", logo_font, "grey100", c.WIDTH + 50, 470)
    draw_text("DEFENSE", logo_font, "grey100", c.WIDTH + 2, 550)
    draw_text("LEVEL: " + str(world.level), text_font, "grey100", c.WIDTH + 10, 10)
    screen.blit(heart_image, (c.WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", c.WIDTH + 50, 40)
    screen.blit(coin_image, (c.WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", c.WIDTH + 50, 70)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    # Calculate the number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free == True:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            world.money -= c.BUY_COST

# FUNCTION TO SELECT TURRETS
def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

# FUNCTION TO CLEAR SELECTION OF TURRETS
def clear_selection():
    for turret in turret_group:
        turret.selected = False


# WORLD
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# CREATE GROUPS
# TURRET
turret_group = pygame.sprite.Group()

# ENEMY
enemy_group = pygame.sprite.Group()

# CREATE BUTTONS
turret_button = GitButton(c.WIDTH+30, 120, buy_turret_image, True)
cancel_button = GitButton(c.WIDTH+50, 180, cancel_image, True)
upgrade_button = GitButton(c.WIDTH+5, 180, upgrade_turret_image, True)
begin_button = GitButton(c.WIDTH+60, 300, begin_image, True)
restart_button = GitButton(310, 300, restart_image, True)
fast_forward_button = GitButton(c.WIDTH+60, 300, fast_forward_image, False)
sound_on_button = GitButton(0, c.HEIGHT-26, sound_on_image, True)
sound_off_button = GitButton(0, c.HEIGHT-26, sound_off_image, True)

# GAME LOOP
while state == State.RUNNING or state == State.MENU or state == State.LOST or state == State.PAUSED or state == True:
    # MENU
    if state == State.MENU:
        screen.fill((0,0,0))
        knapp = Button((c.WIDTH + c.SIDE_PANEL)/2-50, c.HEIGHT/2-20, 100, 40, (255,0,0), "SPILL", (255,255,255), button_font, State.RUNNING)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if knapp.rect.collidepoint(event.pos):
                    state = knapp.newstate
            if state == None:
                state = State.MENU
            if event.type == pygame.QUIT:
                state = False
        knapp.draw(screen)

        for dy in dy_list:
            if dy_list.get(dy)["dy"] == 0:
                dy_list[dy]["speed"] = dy_list.get(dy)["speed"] * -1
            elif dy_list.get(dy)["dy"] == 40:
                dy_list[dy]["speed"] = dy_list.get(dy)["speed"] * -1
            dy_list[dy]["dy"] += dy_list[dy]["speed"]

        draw_text("T", menu_font, (131, 3, 173), (c.WIDTH + c.SIDE_PANEL) / 2-170, 30 + dy_list["T"]["dy"])
        draw_text("O", menu_font, (131, 3, 173), (c.WIDTH + c.SIDE_PANEL) / 2-100, 30 + dy_list["O"]["dy"])
        draw_text("W", menu_font, (131, 3, 173), (c.WIDTH + c.SIDE_PANEL) / 2-30, 30 + dy_list["W"]["dy"])
        draw_text("E", menu_font, (131, 3, 173), (c.WIDTH + c.SIDE_PANEL) / 2+40, 30 + dy_list["E"]["dy"])
        draw_text("R", menu_font, (131, 3, 173), (c.WIDTH + c.SIDE_PANEL) / 2+110, 30 + dy_list["R"]["dy"])
        draw_text("DEFENSE", menu_font, (131, 3, 173), (c.WIDTH + c.SIDE_PANEL) / 2-200, 170)

        # for text in text_list:
        #     speed


    # RUNNING
    if state == State.RUNNING:
        ####################
        # UPDATING SECTION #
        ####################
        if game_over == False:
            if world.health <= 0:
                game_over = True
                game_outcome = -1
            if world.level > c.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1

            enemy_group.update(world)
            turret_group.update(enemy_group, world, sound)

        # highlight selected turret
        if selected_turret:
            selected_turret.selected = True

        ###################
        # EVENT HANDLER #
        ###################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # CHECK IF MOUSE IN GAME AREA
                if mouse_pos[0] < c.WIDTH and mouse_pos[1] < c.HEIGHT:
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        # check if there is enough money for a turret
                        if world.money >= c.BUY_COST:
                            create_turret(mouse_pos)
                    else: 
                        selected_turret = select_turret(mouse_pos)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                state = State.PAUSED

        ###################
        # DRAWING SECTION #
        ###################
        world.draw(screen)

        if sound == True:
            theme_song.set_volume(1)
            if sound_on_button.draw(screen):
                sound = False
        else:
            theme_song.set_volume(0)
            if sound_off_button.draw(screen):
                sound = True
        
        enemy_group.draw(screen) 
        for turret in turret_group:
            turret.draw(screen)

        display_data()

        if game_over == False:
            # check if level has been started or not
            if level_started == False:
                if begin_button.draw(screen):
                    level_started = True
            else:
                world.game_speed = 1
                if fast_forward_button.draw(screen):
                    world.game_speed = 2
                if pygame.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pygame.time.get_ticks() 
            # CHECK IF WAVE FINISHED
            if world.check_level_complete() == True:
                world.money += c.LEVEL_COMPLETE_REWARD
                world.level += 1
                level_started = False
                last_enemy_spawn = pygame.time.get_ticks()
                world.reset_level()
                world.process_enemies()

            draw_text(str(c.BUY_COST), text_font, "grey100", c.WIDTH + 200, 135)
            screen.blit(coin_image, (c.WIDTH + 245, 130))
            if turret_button.draw(screen) == True:
                selected_turret = None
                clear_selection()
                placing_turrets = True
            if placing_turrets == True:
                # DRAW DOTS WHERE YOU CAN CREATE TURRETS
                for r in range(c.ROWS):
                    for k in range (c.COLS):
                        # Calculate the number of the tile
                        tile_num = (k * c.COLS) + r
                        if world.tile_map[tile_num] == 7:
                            space_is_free = True
                            for turret in turret_group:
                                if (k, r) == (turret.tile_x, turret.tile_y):
                                    space_is_free = False
                        else:
                            space_is_free = False
                        if space_is_free:
                            pygame.draw.circle(screen, (0,0,0), ((r+0.5) * c.TILE_SIZE,(k+0.5) * c.TILE_SIZE), 2)
                            space_is_free = False
                cursor_rect = cursor_turret.get_rect()
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= c.WIDTH:
                    screen.blit(cursor_turret, cursor_rect)
                if cancel_button.draw(screen) == True:
                    placing_turrets = False
            # IF A TURRET IS SELECTED, SHOW UPGRADE BUTTON
            if selected_turret:
                # ONLY IF IT CAN BE UPGRADED
                if selected_turret.upgrade_level < c.TURRET_LEVELS:
                    draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.WIDTH + 215, 195)
                    screen.blit(coin_image, (c.WIDTH + 260, 195))
                    if upgrade_button.draw(screen):
                        if world.money >= c.UPGRADE_COST:
                            selected_turret.upgrade()
                            world.money -= c.UPGRADE_COST
        else:
            pygame.draw.rect(screen, "dodgerblue", (200,200,400,200), border_radius= 30)
            if game_outcome == -1:
                draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif game_outcome == 1:
                draw_text("YOU WIN!", large_font, "grey0", 315, 230)

            # restart level
            if restart_button.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pygame.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                # EMPTY GROUPS
                enemy_group.empty()
                turret_group.empty()
    if state == State.PAUSED:
        screen.fill((255,255,255))
        resume = Button((c.WIDTH + c.SIDE_PANEL) / 2 - 60, 200, 100, 200, "white", "RESUME GAME", "black", large_font, State.RUNNING)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            state = State.RUNNING
        menu = Button((c.WIDTH + c.SIDE_PANEL) / 2 - 60, 400, 100, 200, "white", "GO TO MENU / RESTART", "black", large_font, State.MENU)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume.rect.collidepoint(event.pos):
                    state = knapp.newstate
                if menu.rect.collidepoint(event.pos):
                    state = knapp.newstate
                    game_over = False
                    level_started = False
                    placing_turrets = False
                    selected_turret = None
                    last_enemy_spawn = pygame.time.get_ticks()
                    world = World(world_data, map_image)
                    world.process_data()
                    world.process_enemies()
                    # EMPTY GROUPS
                    enemy_group.empty()
                    turret_group.empty()
            if state == None:
                state = State.MENU
            if event.type == pygame.QUIT:
                state = False
        resume.draw(screen)
        menu.draw(screen)
        
    # UPDATE
    pygame.display.flip()
    clock.tick(c.FPS)

# QUIT PYGAME AND EXIT
pygame.quit()
sys.exit()