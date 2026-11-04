import json
from _collections_abc import Iterator
from dataclasses import asdict, replace

from .errors import (
    CatalogError,
    InvalidItemError,
    InvalidItemInFile,
    InvalidVersionError,
    ItemAlreadyExistsError,
    ItemNotFoundError,
)
from .model import Classroom


class Catalog:
    def __init__(self):
        self._items: dict[str, Classroom] = {}
        self.version = "2.0.0"

    def add(self, item: Classroom) -> None:

        if not isinstance(item, Classroom):
            raise InvalidItemError(f"Item {item} is wrong type")

        if item.item_id in self._items:
            raise ItemAlreadyExistsError(f"Item {item.item_id} already exists")

        self._items[item.item_id] = item

    def get(self, item_id: str) -> Classroom:

        if not isinstance(item_id, str):
            raise InvalidItemError("Item id must be string type")

        item = self._items.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found")
        return replace(item)

    def remove(self, item_id: str) -> Classroom:

        if not isinstance(item_id, str):
            raise InvalidItemError("Item id must be string type")

        item = self._items.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found")

        return self._items.pop(item_id)

    def find_by_category(self, category: str) -> list[Classroom]:
        found = []

        for item in self._items.values():
            if category.casefold() in item.category.casefold():
                found.append(replace(item))

        return found

    def find_by_name(self, name: str) -> list[Classroom]:
        found = []

        for item in self._items.values():
            if name.casefold() in item.name.casefold():
                found.append(replace(item))

        return found

    def add_version_1_0_0(self, items: list[dict]) -> None:
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemInFile(f"Item {item} is wrong type")
            try:
                classroom = Classroom(**item, comments="")
            except (InvalidItemError, TypeError) as error:
                raise InvalidItemInFile(
                    f"File contains invalid item: {error}"
                ) from error
            self.add(classroom)

    def add_version_2_0_0(self, items: list[dict]) -> None:
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemInFile(f"Item {item} is wrong type")
            try:
                classroom = Classroom(**item)
            except (InvalidItemError, TypeError) as error:
                raise InvalidItemInFile(
                    f"File contains invalid item: {error}"
                ) from error
            self.add(classroom)

    def load_catalog(self, path: str) -> None:

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as error:
            raise CatalogError(f"File {path} is not found") from error
        except json.JSONDecodeError as error:
            raise InvalidItemInFile("Invalid json file") from error

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

    def save_catalog(self, path: str) -> None:
        items = []
        for item in self._items.values():
            items.append(asdict(item))
        saved_items = {
            "format_version": self.version,
            "items": items,
        }

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(saved_items, file, ensure_ascii=False, indent=4)
        except OSError as error:
            raise CatalogError(f"Cannot write items to file {path}: {error}") from error

    def __len__(self) -> int:

        return len(self._items)

    def __iter__(self) -> Iterator[Classroom]:

        yield from self._items.values()

    def __contains__(self, item_id: str) -> bool:

        if not isinstance(item_id, str):
            raise InvalidItemError("Item id must be string type")

        return self._items.get(item_id) is not None

    def __eq__(self, catalog: object) -> bool:
        if not isinstance(catalog, Catalog):
            raise NotImplementedError(
                "Cannot compare Catalog with another type of data"
            )
        return self._items == catalog._items
