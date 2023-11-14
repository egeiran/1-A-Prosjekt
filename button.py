import pygame

class Button():
    def __init__(self, x, y, height, width, color, text, text_color, font, newstate):
        self.rect = pygame.Rect(x,y,height,width)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.newstate = newstate
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                global state
                state = self.newstate

class GitButton():
    def __init__(self, x, y, image, single_click) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                if self.single_click == True:
                    self.clicked = True
        if pygame.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.image, self.rect)
        return action
        #draw button on screen