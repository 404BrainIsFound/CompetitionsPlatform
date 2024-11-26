# Observer Design Pattern

class ScoreManager:
    def update(self, message) -> None:
        pass


class Subject:
    managers = []

    def __init__(self):
        self.managers = []

    def attach(self, manager: ScoreManager) -> None:
        if manager not in self.managers:
            self.managers.append(manager)

    def detach(self, manager: ScoreManager) -> None:
        self.managers.remove(manager)

    def notify(self, message):
        for manager in self.managers:
            manager.update(message)