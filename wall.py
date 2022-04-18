import time

import pygame
from pygame import Vector2
from wall_ai import WallAI


class Wall:
    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(0, 0, game.preference.wall[0], game.preference.wall[1])
        self.rect.midbottom = game.display.get_rect().midbottom

        self.x = self.rect.midtop[0]
        self.y = self.rect.y
        self.velocity = Vector2()
        self.last_update_time = time.time()

        if game.preference.use_ai:
            self.ai = WallAI(game)

    def update(self):
        border_bottom = self.game.preference.display[1] - self.game.preference.border.start
        border_top = self.game.preference.display[1] - self.game.preference.border.stop

        if self.game.preference.use_ai:
            pos = self.ai.involve()
            if pos is None:
                x, y = self.x, self.y
            else:
                x, y = pos
        else:
            m_pos = pygame.mouse.get_pos()
            x = m_pos[0]
            y = m_pos[1]

        if y < border_top:
            y = border_top
        elif y > border_bottom:
            y = border_bottom

        t = time.time()
        delta_t = (t - self.last_update_time)
        if delta_t != 0:
            self.velocity = Vector2(x - self.x, y - self.y) / delta_t
        self.x = x
        self.y = y
        self.rect.midtop = (x, y)
        self.last_update_time = t

    def draw(self):
        pygame.draw.rect(self.game.display, (0, 0, 0), self.rect)
