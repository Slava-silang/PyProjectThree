from dataclasses import dataclass
from datetime import datetime

from .errors import InvalidItemError


# Create the constructor and comparison methods with dataclass.
@dataclass
class Classroom:
    item_id: str
    name: str
    number: int
    category: str
    # The year refers to the year of last renovation
    year: int
    # The size refers to how many students can sit inside
    size: int
    # A classroom can have no comment.
    comments: str | None = None

    def __post_init__(self):
        # The ID must be text and cannot contain only spaces.
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise InvalidItemError("ID field cannot be empty")

        # The name must be text and cannot contain only spaces.
        if not isinstance(self.name, str) or not self.name.strip():
            raise InvalidItemError("Name field must be non-empty string")

        # Use type() to reject booleans, which also count as integers.
        if type(self.number) is not int or self.number <= 0:
            raise InvalidItemError("Number field must be positive integer")

        # The category must contain text.
        if not isinstance(self.category, str) or not self.category.strip():
            raise InvalidItemError("Category field cannot be empty")

        # Allow years from zero to the current year.
        if type(self.year) is not int or not (0 <= self.year <= datetime.now().year):
            raise InvalidItemError("Invalid year")

        # The size must be a positive integer.
        if type(self.size) is not int or self.size <= 0:
            raise InvalidItemError("Size field must be positive integer")

        # Allow either text or None for comments.
        if self.comments is not None and not isinstance(self.comments, str):
            raise InvalidItemError("Comment field must be string type")

    def __str__(self):
        return f"""{self.name}:
    ID: {self.item_id}
    Number: {self.number}
    Category: {self.category}
    Last year of renovation: {self.year}
    Max number of students: {self.size}"""
