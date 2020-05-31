from .question import (
    Answer,
    MultiChoiceAnswer,
    TrueFalseAnswer,
    Question,
    MultiChoiceQuest,
    TrueFalseQuest,
)
from .exam import Exam

__all__ = [
    "Exam",
    "Answer",
    "MultiChoiceAnswer",
    "TrueFalseAnswer",
    "Question",
    "MultiChoiceQuest",
    "TrueFalseQuest",
]

__version_info__ = (0, 0)
__version__ = ".".join(map(str, __version_info__))
