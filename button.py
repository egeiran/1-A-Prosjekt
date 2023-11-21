import pygame

class Button():
    def __init__(self, x: int, y: int, height: int, width: int, color: pygame.color, text: str, text_color, font: pygame.font.SysFont, newstate):
        """
        Initialize a Button object.

        Parameters:
        - x: X-coordinate of the button's top-left corner.
        - y: Y-coordinate of the button's top-left corner.
        - height: Height of the button.
        - width: Width of the button.
        - color: Color of the button.
        - text: Text displayed on the button.
        - text_color: Color of the text.
        - font: Pygame font for rendering the text.
        - newstate: New state to transition to when the button is clicked.
        """
        self.rect = pygame.Rect(x,y,height,width)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.newstate = newstate
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the button on the specified surface.

        Parameters:
        - screen: The Pygame surface to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event):
        """
        Handle button-related events.

        Parameters:
        - event: Pygame event object.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                global state
                state = self.newstate

class GitButton():
    def __init__(self, x: int, y: int, image: pygame.Surface, single_click: bool) -> None:
        """
        Initialize a GitButton object.

        Parameters:
        - x: X-coordinate of the button's top-left corner.
        - y: Y-coordinate of the button's top-left corner.
        - image: Pygame surface representing the button's image.
        - single_click: Boolean indicating whether the button should respond to a single click only.
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, screen: pygame.Surface):
        """
        Draw the GitButton on the specified surface.

        Parameters:
        - screen: The Pygame surface to draw on.

        Returns:
        - Boolean indicating whether the button was clicked.
        """
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                if self.single_click == True:
                    self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, self.rect)
        return action
        #draw button on screen