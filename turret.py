import pygame
import constants as c
 
class Turret(pygame.sprite.Sprite):
    def __init__(self, img, tile_x, tile_y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y
        # CALCULATE CENTER COORDINATES
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE 
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)