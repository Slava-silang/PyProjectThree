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
        # Store classrooms by their IDs.
        self._items: dict[str, Classroom] = {}
        # Use this version when saving files.
        self.version = "2.0.0"

    def add(self, item: Classroom) -> None:
        """Add a classroom to the catalog.

        Args:
            item: The Classroom to add.

        Returns:
            None.
        """

        # Check that the item is a Classroom.
        if not isinstance(item, Classroom):
            raise InvalidItemError(f"Item {item} is wrong type")

        # Do not allow two classrooms with the same ID.
        if item.item_id in self._items:
            raise ItemAlreadyExistsError(f"Item {item.item_id} already exists")

        self._items[item.item_id] = item

    def get(self, item_id: str) -> Classroom:
        """Find a classroom by its ID.

        Args:
            item_id: The classroom ID as a string.

        Returns:
            A copy of the matching Classroom.
        """

        if not isinstance(item_id, str):
            raise InvalidItemError("Item id must be string type")

        item = self._items.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found")
        # Return a copy to protect the stored classroom from changes.
        return replace(item)

    def remove(self, item_id: str) -> Classroom:
        """Remove a classroom by its ID.

        Args:
            item_id: The classroom ID as a string.

        Returns:
            The removed Classroom.
        """

        if not isinstance(item_id, str):
            raise InvalidItemError("Item id must be string type")

        item = self._items.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found")

        # Return the classroom that was removed.
        return self._items.pop(item_id)

    def find_by_category(self, category: str) -> list[Classroom]:
        """Find classrooms by part of their category.

        Args:
            category: The text to search for.

        Returns:
            A list of matching Classroom copies, or an empty list.
        """
        found = []

        for item in self._items.values():
            # Find part of the category without checking letter case.
            if category.casefold() in item.category.casefold():
                found.append(replace(item))

        return found

    def find_by_name(self, name: str) -> list[Classroom]:
        """Find classrooms by part of their name.

        Args:
            name: The text to search for.

        Returns:
            A list of matching Classroom copies, or an empty list.
        """
        found = []

        for item in self._items.values():
            # Find part of the name without checking letter case.
            if name.casefold() in item.name.casefold():
                found.append(replace(item))

        return found

    def add_version_1_0_0(self, items: list[dict]) -> None:
        """Add items from the old file format with empty comments.

        Args:
            items: A list of classroom dictionaries in version 1.0.0.

        Returns:
            None.
        """
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemInFile(f"Item {item} is wrong type")
            try:
                # The old format has no year field, so we put 2000 as default.
                classroom = Classroom(**item, year=2000)
            except (InvalidItemError, TypeError) as error:
                # Report invalid fields or values as a file error.
                raise InvalidItemInFile(
                    f"File contains invalid item: {error}"
                ) from error
            self.add(classroom)

    def add_version_2_0_0(self, items: list[dict]) -> None:
        """Add items from the current file format.

        Args:
            items: A list of classroom dictionaries in version 2.0.0.

        Returns:
            None.
        """
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemInFile(f"Item {item} is wrong type")
            try:
                classroom = Classroom(**item)
            except (InvalidItemError, TypeError) as error:
                # Report invalid fields or values as a file error.
                raise InvalidItemInFile(
                    f"File contains invalid item: {error}"
                ) from error
            self.add(classroom)

    def load_catalog(self, path: str) -> None:
        """Load classrooms from a JSON file into this catalog.

        Args:
            path: The path to the JSON file.

        Returns:
            None.
        """

        try:
            with open(path, "r", encoding="utf-8") as file:
                # Read the JSON data from the file.
                data = json.load(file)
        except FileNotFoundError as error:
            raise CatalogError(f"File {path} is not found") from error
        except json.JSONDecodeError as error:
            raise InvalidItemInFile("Invalid json file") from error

        # The main JSON value must be a dictionary.
        if not isinstance(data, dict):
            raise InvalidItemInFile("Invalid json file")

        # Check the file version and the list of items.
        version = data.get("format_version")
        items = data.get("items")
        if version is None:
            raise InvalidItemInFile("Data version is required")
        if not isinstance(items, list):
            raise InvalidItemInFile("This file does not contain valid items")

        # Check new items in a separate catalog before saving changes.
        temporary = Catalog()

        # Put all classrooms to tempeorary catalog.
        for item in self._items.values():
            temporary.add(item)

        # Choose the loader for the file version.
        if version == "1.0.0":
            temporary.add_version_1_0_0(items)
        elif version == "2.0.0":
            temporary.add_version_2_0_0(items)
        else:
            raise InvalidVersionError("Invalid version")

        # Update the catalog only after all items have been added.
        self._items = temporary._items

    def save_catalog(self, path: str) -> None:
        """Save the catalog to a JSON file.

        Args:
            path: The path to the file to write.

        Returns:
            None.
        """
        items = []
        for item in self._items.values():
            # Convert each classroom to a dictionary for JSON.
            items.append(asdict(item))
        # Save the version together with the items.
        saved_items = {
            "format_version": self.version,
            "items": items,
        }

        try:
            with open(path, "w", encoding="utf-8") as file:
                # Keep letters readable and add indentation.
                json.dump(saved_items, file, ensure_ascii=False, indent=4)
        except OSError as error:
            raise CatalogError(f"Cannot write items to file {path}: {error}") from error

    def __len__(self) -> int:

        # Return the number of classrooms.
        return len(self._items)

    def __iter__(self) -> Iterator[Classroom]:

        # Yield copy of items
        for item in self._items.values():
            yield replace(item)

    def __contains__(self, item_id: str) -> bool:

        if not isinstance(item_id, str):
            raise InvalidItemError("Item id must be string type")

        # Check whether this ID is in the catalog.
        return self._items.get(item_id) is not None

    def __eq__(self, catalog: object) -> bool:
        if not isinstance(catalog, Catalog):
            raise NotImplementedError(
                "Cannot compare Catalog with another type of data"
            )
        # Compare the classrooms without checking the format version.
        return self._items == catalog._items
