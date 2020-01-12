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

        self.base_images = [ pygame.Surface([px,px], flags=pygame.SRCALPHA) for i in range(360) ]
        self.init_base_image(px)

        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.explosion_channel = pygame.mixer.Channel(constants.EXPLOSION_CHANNEL)

    def init_base_image(self, px):

        # Pick 3 vertices of a 16-gon. Pull them into the center
        NUM_DENTS = 4
        NUM_PIECES = 15
        rng = np.random.default_rng()
        dents = rng.permutation( [True] * NUM_DENTS + [False] * (NUM_PIECES - NUM_DENTS +1) )
        dent_radius = [ ]

        for i, d in enumerate(dents):

            if d:
                r = (1.0-0.3)*rng.random() + 0.3
            else:
                r = 1.0

            dent_radius.append(r)

        offset = np.pi / 180

        for n in range(360):

            pts = []

            for i, r in enumerate(dent_radius):

                theta = 2*np.pi * i/NUM_PIECES
                x = int(r*np.cos(theta + n*offset)*(px//2)) + (px//2)
                y = int(r*np.sin(theta + n*offset)*(px//2)) + (px//2)

                pts.append( (x,y) )

            pygame.draw.aalines(self.base_images[n], pygame.Color("#bc8f8fff"), True, pts)
            pygame.draw.aalines(self.base_images[n], pygame.Color("#bc8f8fff"), True, pts)

    def update(self, tick):

        super().update(tick)

        self.angle += self.omega * tick

        self.image = self.base_images[ int(np.round(self.angle)) % 360 ]

        self.dirty = 1
