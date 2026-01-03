import pygame

class Camera:
    def __init__(self, speed=500):
        self.x = 0
        self.y = 0
        self.speed = speed

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x += self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x -= self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y += self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y -= self.speed * dt

    # world → screen
    def apply(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)

    # screen → world
    def to_world(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)
