import uielement
import pygame
import pygame.freetype

class LivesUI(uielement.UIElement):

    def __init__(self, ship, x=0, y=0):

        super().__init__(x,y)

        # Keep a reference to the ship
        self.ship = ship

        pygame.freetype.init()

        self.font = pygame.freetype.Font('munro.ttf')
        self.font.fgcolor = pygame.Color('white')
        self.font.size = 24

        self.last_lives = self.ship.lives

        self.image, self.rect = self.font.render(f'Lives: {self.ship.lives}')
        self.rect.move_ip(self.x, self.y)

    def update(self, tick):

        if self.ship.lives != self.last_lives:
            self.image, self.rect = self.font.render(f'Lives: {self.ship.lives}')
            self.rect.move_ip(self.x, self.y)

        # Always mark as dirty in case we have issues blitting
        self.dirty = 1
