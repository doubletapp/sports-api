from enum import Enum


class TeamType(Enum):

    HOME = "HOME"
    AWAY = "AWAY"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


# class EventType(Enum):

class MethodScoreType(Enum):

    PENALTY = "Penalty"
    GOAL = "Goal"
    OWNGOAL = "Own goal"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
