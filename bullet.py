import pygame
import time
from pygame import Vector2
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, game):
        super(Bullet, self).__init__()

        self.game = game
        x = game.wall.x
        y = game.preference.display[1] - 60
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)

        self._update_acceleration()
        self.last_bump_time = time.time()
        self.last_bump_pos = self.position

    def _bump(self, rect, velocity=Vector2()) -> None:
        if not rect or not rect.size:
            return

        t = time.time() - self.last_bump_time
        self.velocity += self.acceleration * t
        self.last_bump_time += t
        self.last_bump_pos = self.position
        self._update_acceleration()

        collide = rect.clip(self.rect)
        if not collide:
            return

        delta_center = Vector2(rect.center) - Vector2(self.rect.center)
        radius = self.game.preference.bullet
        if collide.width > collide.height:
            self.velocity.y *= -1
            if delta_center.y > 0:
                self.position.y = rect.y - radius
            else:
                self.position.y = rect.bottom + radius
        else:
            self.velocity.x *= -1
            if delta_center.x > 0:
                self.position.x = rect.x - radius
            else:
                self.position.x = rect.right + radius

        if abs(velocity.x) > abs(self.velocity.x):
            self.velocity.x = velocity.x * 0.3
        if abs(velocity.y) > abs(self.velocity.y):
            self.velocity.y = velocity.y

    def _update_acceleration(self):
        if self.velocity.length() > 0:
            self.acceleration = self.velocity / self.velocity.length() * self.game.preference.acceleration
        else:
            self.acceleration = Vector2()

    def update(self, *args, **kwargs) -> None:
        t = time.time() - self.last_bump_time
        # Accelerate
        self.position = self.last_bump_pos + self.velocity * t + self.acceleration * (t ** 2) / 2

        # Collides
        r = self.game.preference.bullet
        self.rect = pygame.Rect(self.position.x - r, self.position.y - r, 2 * r, 2 * r)
        collide = pygame.sprite.spritecollide(self, self.game.bricks, True)
        if collide:
            self._bump(collide[0].rect)
        elif self.game.wall.rect.clip(self.rect):
            wall = self.game.wall
            self._bump(wall.rect, wall.velocity)
        elif self.game.preference.dead_region.colliderect(self.rect):
            self.game.start()
        else:
            self._bump(self.game.preference.reflect_region_top)
            self._bump(self.game.preference.reflect_region_left)
            self._bump(self.game.preference.reflect_region_right)

    def draw(self):
        pygame.draw.circle(self.game.display, (0, 0, 0), self.position,
                           self.game.preference.bullet)
