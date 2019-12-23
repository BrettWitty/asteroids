import physics
import pygame
import numpy as np
import constants

class Bullet(physics.PhysicsObject):

    def __init__(self, ship):

        d = constants.BULLET_SPAWN_RADIUS
        x = ship.x + d*np.cos(constants.DEG_TO_RAD*ship.angle)
        y = ship.y + d*np.sin(constants.DEG_TO_RAD*ship.angle)
        #vx = 0.1*np.cos(ship.angle)
        #vy = 0.1*np.sin(ship.angle)
        V = constants.FIRE_SPEED
        vx = ship.vx + V*d*np.cos(constants.DEG_TO_RAD*ship.angle)
        vy = ship.vy + V*d*np.sin(constants.DEG_TO_RAD*ship.angle)

        super().__init__(x=x, y=y, vx=vx, vy=vy)

        self.image = pygame.Surface([5,5], flags=pygame.SRCALPHA)
        self.rect = pygame.Rect(x,y,5,5)
        self.visible = 1

        pygame.draw.circle(self.image, pygame.Color("#00ff7fff"), self.image.get_rect().center, 2)
        
        self.life = constants.FIRE_LIFETIME

    def update(self, tick):

        super().update(tick)

        self.life -= tick

        if self.life < 0.0:
            die_event = pygame.event.Event(constants.FIRE_DIE_EVENT, { 'bullet' : self })
            pygame.event.post(die_event)

        self.dirty = 1
