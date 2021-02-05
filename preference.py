from pygame import Rect

class Preference:
    def __init__(self):
        self.fullscreen = False
        self.display = (1240, 720)
        self.army = (50, 5)
        self.brick = (30, 30)
        self.margin = (10, 10)
        self.wall = (50, 5)
        self.border = range(20, 120)
        self.bullet = 8
        # Unit: pixel per second
        self.velocity = 500
        self.dead_region = Rect(0, self.display[1] - 5, self.display[0], 5)
        self.reflect_region_top = Rect(0, 0, 5, self.display[1])
        self.reflect_region_left = Rect(0, 0, self.display[0], 5)
        self.reflect_region_right = Rect(self.display[0] - 5, 0, 5, self.display[1])
        # Unit: pixel per second
        self.acceleration = -10
