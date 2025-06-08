from dataclasses import dataclass

@dataclass
class Review:
    user_opinion: str
    user_rating: int

    def __post_init__(self):
        if not (1 <= self.user_rating <= 10):
            raise ValueError("User rating must be between 1 and 10")
        if not self.user_opinion.strip():
            raise ValueError("User opinion cannot be empty")