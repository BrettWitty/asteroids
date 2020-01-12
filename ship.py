import pygame

import physics
import constants

class Ship(physics.PhysicsObject):

    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, angle=90.0):

        super().__init__(x=x, y=y, vx=vx, vy=vy, angle=angle)

        self.name = 'Ship'

        self.lives = 3
        
        self.firing = False
        self.firing_cooldown = 0
        self.thrusting = False

        self.image = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.rect = pygame.Rect(x,y,32,32)
        self.visible = 1

        self.base_image = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.base_image_thrust = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.mask = pygame.Mask([32,32])
        self.init_base_image()

        self.thrust_sound = pygame.mixer.Sound("sounds/thrust.wav")

        self.thrust_channel = pygame.mixer.Channel(constants.THRUST_CHANNEL)

    def init_base_image(self):

        peak = (28,16)
        right = (4,28)
        left = (4,4)
        butt = (8,16)

        pygame.draw.aalines(self.base_image, (255,255,255), True, [peak, right, butt, left])
        pygame.draw.aalines(self.base_image, (255,255,255), True, [peak, right, butt, left])

        left_thruster = (6,6)
        mid_thruster = (1,16)
        right_thruster = (6,22)

        pygame.draw.aalines(self.base_image_thrust, (255,255,255), True, [peak, right, butt, left])
        pygame.draw.aalines(self.base_image_thrust, (255,255,255), True, [peak, right, butt, left])
        pygame.draw.aalines(self.base_image_thrust, pygame.Color("#ff8c00ff"), False, [left_thruster,mid_thruster, right_thruster])
        pygame.draw.aalines(self.base_image_thrust, pygame.Color("#ff8c00ff"), False, [left_thruster,mid_thruster, right_thruster])
        pygame.draw.aaline(self.base_image_thrust, pygame.Color("#ff8c00ff"), butt, mid_thruster)

        self.image = self.base_image.copy()

    def update(self, tick):

        super().update(tick)

        self.firing_cooldown -= tick

        if self.firing and self.firing_cooldown <= 0 :
            self.firing_cooldown = constants.FIRE_COOLDOWN
            pygame.event.post(pygame.event.Event(constants.FIRE_EVENT))

        if self.thrusting:
            rotated_img = pygame.transform.rotate( self.base_image_thrust, self.angle)
            if not self.thrust_channel.get_busy():
                self.thrust_channel.play(self.thrust_sound, loops=-1)
        else:
            rotated_img = pygame.transform.rotate( self.base_image, self.angle)
            if self.thrust_channel.get_busy():
                self.thrust_channel.fadeout(constants.FADE_OUT_TIME)
        rotated_rect = self.rect.copy()
        rotated_rect.center = rotated_img.get_rect().center
        rotated_img = rotated_img.subsurface(rotated_rect).copy()
        self.image = rotated_img
        self.dirty = 1

    def thrust(self, tick):

        super().thrust(tick)

        self.thrusting = True
