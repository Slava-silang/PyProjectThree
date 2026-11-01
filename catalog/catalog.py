import json
from typing import Dict, List
from dataclasses import replace
from _collections_abc import Iterator
from .model import Classroom
from .errors import ItemAlreadyExistsError, ItemNotFoundError, InvalidItemError, CatalogError, InvalidItemInFile, InvalidVersionError

class Catalog:

    def __init__(self):
        self._items: Dict[str, Classroom] = {}
        self.version = "2.0.0"

    def add(self, item: Classroom) -> None:

        if not isinstance(item, Classroom):
            raise InvalidItemError(f"Item {item} is wrong type")

        if item.item_id in self._items:
            raise ItemAlreadyExistsError(f"Item {item.item_id} already exists")

        self._items[item.item_id] = item

    def get(self, item_id: str) -> Classroom:

        if not isinstance(item_id, str):
            raise InvalidItemError(f"Item id must be string type")

        item = self._items.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found")
        return replace(item)

    def remove(self, item_id: str) -> Classroom:

        if not isinstance(item_id, str):
            raise InvalidItemError(f"Item id must be string type")

        item = self._items.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found")

        return self._items.pop(item_id)

    def find_by_category(self, category: str) -> List[Classroom]:
        found = []

        for item in self._items.values():
            if category.casefold() in item.category.casefold():
                found.append(replace(item))

        return found

    def find_by_name(self, name: str) -> List[Classroom]:
        found = []

        for item in self._items.values():
            if name.casefold() in item.name.casefold():
                found.append(replace(item))

        return found

    def add_version_1_0_0(self, items: List[Dict]) -> None:
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemInFile(f"Item {item} is wrong type")
            try:
                classroom = Classroom(**item, comments="")
            except (InvalidItemError, TypeError) as error:
                raise InvalidItemInFile(f"File contains invalid item: {error}") from error
            self.add(classroom)

    def add_version_2_0_0(self, items: List[Dict]) -> None:
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemInFile(f"Item {item} is wrong type")
            try:
                classroom = Classroom(**item)
            except (InvalidItemError, TypeError) as error:
                raise InvalidItemInFile(f"File contains invalid item: {error}") from error
            self.add(classroom)

    def load_catalog(self, path: str) -> None:

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as error:
            raise CatalogError(f"File {path} is not found") from error
        except json.JSONDecodeError as error:
            raise InvalidItemInFile(f"Invalid json file") from error

        if not isinstance(data, dict):
            raise InvalidItemInFile("Invalid json file")

        version = data.get("format_version")
        items = data.get("items")
        if version is None:
            raise InvalidItemInFile("Data version is required")
        if not isinstance(items, list):
            raise InvalidItemInFile("This file does not contain valid items")

        temporary = Catalog()

        for item in self._items.values():
            temporary.add(item)

        if version == "1.0.0":
            temporary.add_version_1_0_0(items)
        elif version == "2.0.0":
            temporary.add_version_2_0_0(items)
        else:
            raise InvalidVersionError("Invalid version")

        self._items = temporary._items

    def __len__(self) -> int:

        return len(self._items)

    def __iter__(self) -> Iterator[Classroom]:

        for item in self._items.values():
            yield item

    def __contains__(self, item_id: str) -> bool:

        if not isinstance(item_id, str):
            raise InvalidItemError(f"Item id must be string type")

        return self._items.get(item_id) is not None
