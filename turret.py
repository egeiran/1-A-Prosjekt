import pygame
import math
import constants as c
from turret_data import TURRET_DATA
from world import World
 
class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheets: pygame.sprite.Sprite, tile_x: int, tile_y: int, shot_fx) -> None:
        """
        Initialize a Turret object.

        Parameters:
        - sprite_sheets: Sprite sheets for turret animation.
        - tile_x: X-coordinate of the tile where the turret is placed.
        - tile_y: Y-coordinate of the tile where the turret is placed.
        - shot_fx: Sound effect for turret shots.
        """
        pygame.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pygame.time.get_ticks()
        self.selected = False
        self.target = None
        
        #POSITION
        self.tile_x = tile_x
        self.tile_y = tile_y
        # CALCULATE CENTER COORDINATES
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE 
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        # SOUND
        self.shot_fx = shot_fx

        #ANIMATION
        self.sprite_sheet = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheet[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # UPDATE IMAGE
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # TRANSPARANT CIRCLE RANGE
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet: pygame.Surface):
        """
        Load images from the provided sprite sheet.

        Parameters:
        - sprite_sheet: The sprite sheet containing turret animation frames.

        Returns:
        - List of animation frames.
        """
        # MAKE PICTURES FROM SPRITE SHEET
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group: pygame.sprite.Group, world: World, sound):
        """
        Update the turret's state.

        Parameters:
        - enemy_group: Group of enemy sprites.
        - world: The game world.
        - sound: Boolean indicating whether sound is enabled.
        """
        # if target picked, play firing animation
        if self.target:
            self.play_animation()
        else:
            # SEARCH FOR NEW TARGET ONCE TURRET HAS COOLED DOWN
            if pygame.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group, sound)

    def pick_target(self, enemy_group: pygame.sprite.Group, sound):
        """
        Pick a target from the enemy group within the turret's range.

        Parameters:
        - enemy_group: Group of enemy sprites.
        - sound: Boolean indicating whether sound is enabled.
        """
        #find an enemy to target
        x_dist = 0
        y_dist = 0
        #check distance to each enemy
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= c.DAMAGE
                    if sound == True:
                        self.shot_fx.play()
                    break

    def play_animation(self):
        """
        Play the firing animation for the turret.
        """
        # UPDATE IMAGE
        self.original_image = self.animation_list[self.frame_index]
        # CHECK IF ENOUGH TIME HAS PASSED
        if pygame.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # CHECK IF ANIMATION IS FINISHED
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()
                self.target = None

    def upgrade(self):
        """
        Upgrade the turret to the next level, updating attributes and images.
        """
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        # UPGRADE TURRET IMAGE
        self.animation_list = self.load_images(self.sprite_sheet[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        # UPGRADE RANGE CIRCLE
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        
    def draw(self, screen: pygame.Surface):
        """
        Draw the turret on the screen.

        Parameters:
        - screen: The Pygame surface to draw on.
        """
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image,self.rect)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)