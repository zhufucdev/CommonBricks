from ai import *
from pygame.math import Vector2
import random


def predict_enter_pos(bullet):
    border_top = bullet.game.preference.display[1] - bullet.game.preference.border.stop + 10

    step = (border_top - bullet.position.y) / bullet.velocity.y
    duration = step
    while True:
        dest = bullet.position.copy()
        acceleration = bullet.velocity.copy()
        if acceleration.length() != 0:
            acceleration.scale_to_length(bullet.game.preference.acceleration)
        dest += bullet.velocity * duration + acceleration * (duration ** 2) / 2
        if dest.y <= border_top:
            break
        duration += step

    return dest


class Serve(Move):
    def __init__(self, wall, bullet):
        self.wall = wall
        self.bullet = bullet
        super(Serve, self).__init__()

    def on_start(self):
        super(Serve, self).on_start()

        duration = 0.1
        dest = self.bullet.position.copy()
        half_wall = self.wall.game.preference.wall[0] / 2
        if self.bullet.velocity.x >= 0:
            dest.x += half_wall
        else:
            dest.x -= half_wall
        super(Serve, self).__init__(Vector2(self.wall.x, self.wall.y), dest, duration)


class Pingpong(Move):
    def __init__(self, wall, bullet):
        super().__init__(Vector2(wall.x, wall.y), predict_enter_pos(bullet), 0.1)


class WallAI(AI):
    def __init__(self, game):
        super(WallAI, self).__init__(game)

    def update(self):
        bullet = self.game.bullet
        wall = self.game.wall
        if bullet.velocity.length() == 0:
            # the bullet isn't moving
            self.schedule_action(Serve(wall, bullet))
        elif bullet.velocity.y > 0:
            if bullet.velocity.y >= 300:
                self.schedule_action(Pingpong(wall, bullet))
            else:
                dest_predict = predict_enter_pos(bullet)
                dest = dest_predict.copy()
                dest.y += (wall.game.preference.border.stop - wall.game.preference.border.start) / 2
                self.schedule_action(Move(Vector2(wall.x, wall.y), dest, 0.1))
                self.schedule_action(WaitUntil(lambda: dest_predict.y <= bullet.position.y))
                self.schedule_action(Serve(wall, bullet))

