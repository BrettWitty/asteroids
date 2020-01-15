import pygame
import numpy as np

from entities import *
import constants

def spawn_bullet(ship, rng, objects):

    objects.add( Bullet(ship) )
    snd = pygame.mixer.Sound("sounds/laser.wav")
    ch = pygame.mixer.Channel(constants.LASER_CHANNEL)
    ch.play(snd)

def spawn_asteroid(ship, rng, objects, *, pos=None, size=None, num=1):

    if size != None and size < 0:
        return

    if not pos:

        # Get a random position in the space (away from the ship)
        cx = ship.x
        cy = ship.y
        r = (0.8-0.4)*rng.random() + 0.4
        theta = 2*constants.PI * rng.random()

        cx += r*np.cos(theta)
        cy += r*np.sin(theta)
        max_vel = 0.01

    else:
        cx,cy = pos
        max_vel = 0.5

    for i in range(num):

        # Pick random size
        if not size:
            size = rng.integers(0,4)
        r = 0.3
        theta = 2*constants.PI * rng.random()
        x = r*np.cos(theta) + cx
        y = r*np.sin(theta) + cy
        vx = (2*rng.random() -1) * max_vel
        vy = (2*rng.random() -1) * max_vel
        omega = (2*rng.random() -1) * 0.1
        objects.add( Debris(size=size, x=x, y=y, vx=vx, vy=vy, omega=omega))

def main():

    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption('BWasteroids')
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT), flags=pygame.SCALED)

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

    spawn_asteroid(ship, rng, objects, num = 4)
    print("Running...")

    space = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    space.fill((15,15,15))
    screen.blit(space,(0,0))
    pygame.display.update( pygame.Rect(0,0,constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    objects.clear(screen, space)

    bullet_time = 100
        
    while running:

        bullet_time -= clock.get_time()

        # Events
        for event in pygame.event.get(pump=True):

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_i:
                    print(f"({clock.get_fps():0.3f} FPS)")

                if event.key == pygame.K_p:
                    for i in range(20):
                        spawn_asteroid(ship, rng, objects)

                if event.key == pygame.K_SPACE:
                    ship.firing = True

            if event.type == pygame.KEYUP:

                if event.key in (pygame.K_UP, pygame.K_w):
                    if not ship.dead:
                        ship.thrusting = False

                if event.key == pygame.K_SPACE:
                    if not ship.dead:
                        ship.firing = False

            if event.type == constants.FIRE_EVENT:
                spawn_bullet(ship, rng, objects)

            if event.type == constants.FIRE_DIE_EVENT:
                objects.remove( event.bullet )

        keys = pygame.key.get_pressed()
        if not ship.dead:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ship.rotate( tick )

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ship.rotate( -tick )

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                ship.thrust(tick)

        # Simulate()
        objects.update(tick)

        # Check for collisions
        collisions = pygame.sprite.groupcollide(objects, objects, False, False, pygame.sprite.collide_mask)

        for c1 in collisions:
            for c2 in collisions[c1]:
                if c1 in objects and c2 in objects:
                    if c1 != c2:
                        if isinstance(c1, Bullet) and isinstance(c2, Debris):
                            objects.remove(c2)
                            spawn_asteroid(ship, rng, objects, pos=(c2.x, c2.y), size=(c2.size-1), num=rng.integers(1,4))
                            c2.kill()
                            del c2
                            objects.remove(c1)
                        if isinstance(c1, Ship) and isinstance(c2, Debris):

                            if not c1.dead:
                                c1.die()
        
        # render()
        rects = objects.draw(screen)
        pygame.display.update(rects)
        tick = clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
