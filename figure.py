import pygame

class Figure():
    def __init__(self, pos, img) -> None:
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)