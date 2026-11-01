from dataclasses import dataclass
from .errors import InvalidItemError
from datetime import datetime

@dataclass
class Classroom:
    item_id: str
    name: str
    number: int
    category: str
    year: int
    size: int
    comments: str | None = None

    def __post_init__(self):
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise InvalidItemError("ID field cannot be empty")

        if not isinstance(self.name, str) or not self.name.strip():
            raise InvalidItemError("Name field must be non-empty string")

        if type(self.number) is not int or self.number <= 0:
            raise InvalidItemError("Number field must be positive integer")

        if not isinstance(self.category, str) or not self.category.strip():
            raise InvalidItemError("Category field cannot be empty")

        if type(self.year) is not int or not (0 <= self.year <= datetime.now().year):
            raise InvalidItemError("Invalid year")

        if type(self.size) is not int or self.size <= 0:
            raise InvalidItemError("Size field must be positive integer")

        if self.comments is not None:
            if not isinstance(self.comments, str):
                raise InvalidItemError("Comment field must be string type")
