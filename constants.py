import pygame
import numpy as np

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024

THRUST = 0.01
PI = np.pi
DEG_TO_RAD = PI / 180.0

BULLET_SPAWN_RADIUS = 32/1024

FIRE_COOLDOWN = 200
FIRE_LIFETIME = 1000
FIRE_SPEED = 30

# Events
SHIP_SPAWN_EVENT = pygame.event.custom_type()
FIRE_EVENT = pygame.event.custom_type()
FIRE_DIE_EVENT = pygame.event.custom_type()
EXPLODE_DEBRIS = pygame.event.custom_type()



# Audio
FADE_OUT_TIME = 200
UI_CHANNEL = 0
THRUST_CHANNEL = 1
LASER_CHANNEL = 2
EXPLOSION_CHANNEL = 3
SHIP_EXPLODE_CHANNEL = 4
