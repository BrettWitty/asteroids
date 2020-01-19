import pygame

class UIElement(pygame.sprite.DirtySprite):

    def __init__(self, x, y):

        pygame.sprite.DirtySprite.__init__(self)

        self.name = 'UI Element'

        # Unlike physics objects, this is our pixel location
        self.x = x
        self.y = y

        self.image = None
        self.rect = None

    def update(self, tick):

        pass

