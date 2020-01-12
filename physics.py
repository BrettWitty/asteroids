import pygame
import numpy as np

import constants

class PhysicsObject(pygame.sprite.DirtySprite):

    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, angle=0):

        pygame.sprite.DirtySprite.__init__(self)

        self.name = 'N/A'

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle

        self.mask = None

    def update(self, tick):

        self.x += self.vx * tick/1000.0
        self.y += self.vy * tick/1000.0

        if self.x > 1.0:
            self.x =  -1.0 + (self.x % 1.0)
        if self.x < -1.0:
            self.x = 1.0 - (self.x % -1.0)

        if self.y > 1.0:
            self.y =  -1.0 + (self.y % 1.0)
        if self.y < -1.0:
            self.y = 1.0 - (self.y % -1.0)

        # Convert to screen space
        self.rect.centerx = int((1.0 + self.x) * (constants.SCREEN_WIDTH //2))
        self.rect.centery = int((1.0 - self.y) * (constants.SCREEN_HEIGHT //2))

    def rotate(self, tick):

        self.angle += tick/1000.0*360.0
        self.angle %= 360

    @property
    def speed(self):
        return np.square([self.vx, self.vy]).sum()

    def thrust(self, t):

        # Thrust for a time
        thrust_vx = np.cos(self.angle * constants.DEG_TO_RAD)
        thrust_vy = np.sin(self.angle * constants.DEG_TO_RAD)

        self.vx += constants.THRUST*thrust_vx
        self.vy += constants.THRUST*thrust_vy
