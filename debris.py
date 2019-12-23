import physics
import pygame
import numpy as np
import constants

class Debris(physics.PhysicsObject):

    PIXEL_SIZE = [32, 48, 64, 128]

    def __init__(self, size, x=0.0, y=0.0, vx=0.0, vy=0.0, angle=90.0, omega=0.0):

        super().__init__(x=x, y=y, vx=vx, vy=vy, angle=angle)

        self.omega = omega

        self.size = size

        px = self.PIXEL_SIZE[ self.size % len(self.PIXEL_SIZE)]

        self.image = pygame.Surface([px,px], flags=pygame.SRCALPHA)
        self.rect = pygame.Rect(x,y,px,px)
        self.visible = 1

        self.base_image = pygame.Surface([px,px], flags=pygame.SRCALPHA)
        self.init_base_image(px)

        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.explosion_channel = pygame.mixer.Channel(constants.EXPLOSION_CHANNEL)

    def init_base_image(self, px):

        # Pick 3 vertices of a 16-gon. Pull them into the center
        NUM_DENTS = 4
        NUM_PIECES = 15
        rng = np.random.default_rng()
        dents = rng.permutation( [True] * NUM_DENTS + [False] * (NUM_PIECES - NUM_DENTS) )

        pts = []

        for i, d in enumerate(dents):

            if d:
                r = (1.0-0.3)*rng.random() + 0.3
            else:
                r = 1.0

            theta = 2*np.pi * i/NUM_PIECES
            x = int(r*np.cos(theta)*(px//2)) + (px//2)
            y = int(r*np.sin(theta)*(px//2)) + (px//2)

            pts.append( (x,y) )

        pygame.draw.aalines(self.base_image, pygame.Color("#bc8f8fff"), True, pts)
        pygame.draw.aalines(self.base_image, pygame.Color("#bc8f8fff"), True, pts)

    def update(self, tick):

        super().update(tick)

        self.angle += self.omega * tick

        rotated_img = pygame.transform.rotate( self.base_image, self.angle)
        rotated_rect = self.rect.copy()
        rotated_rect.center = rotated_img.get_rect().center
        rotated_img = rotated_img.subsurface(rotated_rect).copy()
        self.image = rotated_img
        self.dirty = 1
