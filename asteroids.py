import pygame
import numpy as np

from entities import *
import constants

def main():

    pygame.init()

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

    for i in range(4):
        size = rng.integers(0,4)
        x = 2*rng.random() -1
        y = 2*rng.random() -1
        vx = (2*rng.random() -1) * 0.01
        vy = (2*rng.random() -1) * 0.01
        omega = (2*rng.random() -1) * 0.1
        objects.add( Asteroid(size=size, x=x, y=y, vx=vx, vy=vy, omega=omega))

    print("Running...")

    space = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    space.fill((15,15,15))
    screen.blit(space,(0,0))
    pygame.display.update( pygame.Rect(0,0,constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
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
