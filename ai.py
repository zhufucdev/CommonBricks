import time

from pygame import Vector2


class Action:
    def __init__(self, duration):
        self.duration = duration
        self.finished = False

    def on_start(self):
        pass

    def update(self) -> tuple[int, int]:
        pass

    def on_finish(self):
        pass


class Wait(Action):
    """ Let AI do nothing in the following period of time.

    Unit of duration is seconds.
    """

    def __init__(self, duration):
        super(Wait, self).__init__(duration)
        self.start_time = time.time()

    def update(self) -> tuple[int, int]:
        if time.time() - self.start_time >= self.duration:
            self.finished = True


class WaitUntil(Action):
    def __init__(self, condition):
        super(WaitUntil, self).__init__(-1)
        self.condition = condition

    def update(self):
        if self.condition():
            self.finished = True


class Move(Action):
    def __init__(self, starting=None, destination=None, duration=None):
        super().__init__(duration)
        self.starting = starting
        self.destination = destination

        if starting is not None:
            self.velocity = (destination - starting) / duration

    def on_start(self):
        self.start_time = time.time()

    def update(self) -> tuple[int, int]:
        process = time.time() - self.start_time

        if process >= self.duration:
            self.on_finish()
            self.finished = True
            return self.destination
        else:
            move = self.starting.copy() + self.velocity * process
            return move


class AI:
    def __init__(self, game):
        self.game = game
        self.scheduler = []
        self.execute_action(Wait(1))

    def _prepare_action(self, action):
        action.ai = self
        self.current_action = action

    def schedule_action(self, action):
        self.scheduler.insert(0, action)
        print(f"AI: Scheduler changed. {len(self.scheduler)} present.")

    def execute_action(self, action):
        print(f"AI: Execute {type(action)}")
        self._prepare_action(action)
        action.on_start()

    def update(self):
        """
        Called when there's nothing to do.

        Actions should be scheduled, or nothing would happen.
        """
        raise NotImplementedError()

    def involve(self):
        if self.current_action.finished:
            if not self.scheduler:
                self.update()

            if self.scheduler:
                action = self.scheduler.pop()
                self.execute_action(action)
            else:
                return None

        return self.current_action.update()
