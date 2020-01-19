import pygame
import numpy as np

import physics
import constants

class Ship(physics.PhysicsObject):

    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, angle=0.0):

        super().__init__(x=x, y=y, vx=vx, vy=vy, angle=angle)

        self.name = 'Ship'

        self.lives = 3
        self.score = 0
        
        self.firing = False
        self.firing_cooldown = 0
        self.thrusting = False

        self.image = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.rect = pygame.Rect(x,y,32,32)
        self.visible = 1

        self.base_images = [pygame.Surface([32,32], flags=pygame.SRCALPHA) for i in range(360) ]
        self.base_images_thrust = [pygame.Surface([32,32], flags=pygame.SRCALPHA) for i in range(360) ]
        
        self.init_base_image()

        self.mask = pygame.Mask([32,32])
        self.masks = [ pygame.mask.from_surface(surf) for surf in self.base_images ]

        self.thrust_sound = pygame.mixer.Sound("sounds/thrust.wav")
        self.thrust_channel = pygame.mixer.Channel(constants.THRUST_CHANNEL)

        self.explode_sound = pygame.mixer.Sound("sounds/ship-explode.wav")
        self.explode_channel = pygame.mixer.Channel(constants.SHIP_EXPLODE_CHANNEL)

    def init_base_image(self):

        for theta in range(360):

            peak = pygame.Vector2(12,0)
            right = pygame.Vector2(-12,12)
            left = pygame.Vector2(-12,-12)
            butt = pygame.Vector2(-8,0)

            left_thruster = pygame.Vector2(-10,-10)
            mid_thruster = pygame.Vector2(-16,0)
            right_thruster = pygame.Vector2(-10,10)

            for c in [peak, right, left, butt, left_thruster, mid_thruster, right_thruster]:
                c.rotate_ip(-theta)
                c += (16,16)

            # Non thrusting image
            pygame.draw.aalines(self.base_images[theta], (255,255,255), True, [peak, right, butt, left])
            pygame.draw.aalines(self.base_images[theta], (255,255,255), True, [peak, right, butt, left])
                        
            # Thrusting image
            pygame.draw.aalines(self.base_images_thrust[theta], (255,255,255), True, [peak, right, butt, left])
            pygame.draw.aalines(self.base_images_thrust[theta], (255,255,255), True, [peak, right, butt, left])
            pygame.draw.aalines(self.base_images_thrust[theta], pygame.Color("#ff8c00ff"), False, [left_thruster,mid_thruster, right_thruster])
            pygame.draw.aalines(self.base_images_thrust[theta], pygame.Color("#ff8c00ff"), False, [left_thruster,mid_thruster, right_thruster])
            pygame.draw.aaline(self.base_images_thrust[theta], pygame.Color("#ff8c00ff"), butt, mid_thruster)

        self.image = self.base_images[int(self.angle)]

    def update(self, tick):

        super().update(tick)

        self.firing_cooldown -= tick

        idx = int(np.round(self.angle)) % 360

        if self.firing and self.firing_cooldown <= 0 :
            self.firing_cooldown = constants.FIRE_COOLDOWN
            pygame.event.post(pygame.event.Event(constants.FIRE_EVENT))

        if self.thrusting:
            self.image = self.base_images_thrust[idx]
            if not self.thrust_channel.get_busy():
                self.thrust_channel.play(self.thrust_sound, loops=-1)
        else:
            self.image = self.base_images[idx]
            if self.thrust_channel.get_busy():
                self.thrust_channel.fadeout(constants.FADE_OUT_TIME)

        self.mask = self.masks[idx]
        self.dirty = 1

    def thrust(self, tick):

        super().thrust(tick)

        self.thrusting = True

    def die(self):

        self.explode_channel.play(self.explode_sound)
        self.lives -= 1
        self.thrusting = False
        self.firing = False

        if self.lives < 1:
            pygame.event.post(pygame.event.Event(constants.GAME_OVER))

    @property
    def dead(self):

        return self.explode_channel.get_busy()
