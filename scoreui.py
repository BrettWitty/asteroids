import uielement
import pygame
import pygame.freetype
import constants

class ScoreUI(uielement.UIElement):

    def __init__(self, ship, x=0, y=0):

        # x and y are offsets from the right-hand side, in this case

        super().__init__(x,y)

        # Keep a reference to the ship
        self.ship = ship

        pygame.freetype.init()

        self.font = pygame.freetype.Font('munro.ttf')
        self.font.fgcolor = pygame.Color('white')
        self.font.size = 24

        self.last_score = self.ship.score

        self.score_text = 'Score: {self.ship.score: 8,d}'

        self.x = constants.SCREEN_WIDTH - (self.font.get_rect(self.score_text.format(self=self)).width + self.x)

        self.image, self.rect = self.font.render(self.score_text.format(self=self))
        self.rect.move_ip(self.x, self.y)

    def update(self, tick):

        if self.ship.score != self.last_score:
            self.image, self.rect = self.font.render(self.score_text.format(self=self))
            self.rect.move_ip(self.x, self.y)

        # Always mark as dirty in case we have issues blitting
        self.dirty = 1
