import pygame
import numpy as np

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

THRUST = 0.01
DEG_TO_RAD = np.pi / 180.0

class PhysicsObject(pygame.sprite.DirtySprite):

    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, angle=0):

        pygame.sprite.DirtySprite.__init__(self)

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle

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
        self.rect.centerx = int((1.0 + self.x) * (SCREEN_WIDTH //2))
        self.rect.centery = int((1.0 - self.y) * (SCREEN_HEIGHT //2))

    def rotate(self, tick):

        self.angle += tick/1000.0*360.0
        self.angle %= 360

    @property
    def speed(self):
        return np.square([self.vx, self.vy]).sum()

    def thrust(self, t):

        # Thrust for a time
        thrust_vx = np.cos(self.angle * DEG_TO_RAD)
        thrust_vy = np.sin(self.angle * DEG_TO_RAD)

        self.vx += THRUST*thrust_vx
        self.vy += THRUST*thrust_vy



class Ship(PhysicsObject):

    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, angle=90.0):

        super().__init__(x=x, y=y, vx=vx, vy=vy, angle=angle)

        self.lives = 3
        
        self.firing = False
        self.thrusting = False

        self.image = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.rect = pygame.Rect(x,y,32,32)
        self.visible = 1

        self.base_image = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.base_image_thrust = pygame.Surface([32,32], flags=pygame.SRCALPHA)
        self.init_base_image()

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

        if self.thrusting:
            rotated_img = pygame.transform.rotate( self.base_image_thrust, self.angle)
        else:
            rotated_img = pygame.transform.rotate( self.base_image, self.angle)
        rotated_rect = self.rect.copy()
        rotated_rect.center = rotated_img.get_rect().center
        rotated_img = rotated_img.subsurface(rotated_rect).copy()
        self.image = rotated_img
        self.dirty = 1

    def thrust(self, tick):

        super().thrust(tick)

        self.thrusting = True

class Asteroid(PhysicsObject):

    PIXEL_SIZE = [32, 48, 64,128]

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

def main():

    pygame.init()

    pygame.display.set_caption('BWasteroids')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags=pygame.SCALED)

    # Game loop
    running = True
    clock = pygame.time.Clock()
    tick = 0

    # Create data
    ship = Ship(0.0,0.0, 0.0,0.0, 90.0)

    objects = pygame.sprite.LayeredDirty(_use_update=True)
    #objects = pygame.sprite.LayeredDirty()

    objects.add(ship)

    rng = np.random.default_rng()

    for i in range(4):
        size = rng.integers(0,4)
        x = 2*rng.random() -1
        y = 2*rng.random() -1
        vx = (2*rng.random() -1) * 0.01
        vy = (2*rng.random() -1) * 0.01
        omega = (2*rng.random() -1) * 0.1
        objects.add( Asteroid(size=size, x=x, y=y, vx=vx, vy=vy, omega=omega))

    print("Running...")

    space = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    space.fill((15,15,15))
    screen.blit(space,(0,0))
    pygame.display.update( pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
    objects.clear(screen, space)
        
    while running:

        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_i:
                    print(f"({clock.get_fps():0.3f} FPS)")

            if event.type == pygame.KEYUP:

                if event.key in (pygame.K_UP, pygame.K_w):
                    ship.thrusting = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship.rotate( tick )

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship.rotate( -tick )

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ship.thrust(tick)

        # Simulate()
        objects.update(tick)
        
        # render()
        rects = objects.draw(screen)
        pygame.display.update(rects)
        tick = clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
