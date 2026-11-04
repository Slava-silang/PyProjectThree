import json

import pytest

from catalog.catalog import Catalog
from catalog.errors import InvalidVersionError, CatalogError, ItemAlreadyExistsError
from catalog.model import Classroom


def test_round_trip_json(tmp_path):
    catalog = Catalog()

    for id_ in ["001", "002", "003", "004"]:
        classroom = Classroom(
            item_id=id_,
            name="test classroom",
            number=int(id_),
            category="Math class",
            year=2020,
            size=30,
            comments=None,
        )
        catalog.add(classroom)

    path = tmp_path / "catalog.json"

    catalog.save_catalog(path)

    catalog_new = Catalog()
    catalog_new.load_catalog(path)

    assert catalog == catalog_new


def test_wrong_version(tmp_path):
    path = tmp_path / "catalog.json"

    catalog = Catalog()
    catalog.version = "3.0.0"
    for id_ in ["001", "002", "003", "004"]:
        classroom = Classroom(
            item_id=id_,
            name="test classroom",
            number=int(id_),
            category="Math class",
            year=2020,
            size=30,
            comments=None,
        )
        catalog.add(classroom)

    catalog.save_catalog(path)
    new_catalog = Catalog()
    with pytest.raises(InvalidVersionError):
        new_catalog.load_catalog(path)

def test_wrong_json(tmp_path):
    path = tmp_path / "catalog.json"

    catalog = Catalog()

    test_data = """{
        "format_version": "2.0.0",
        "items": [{
            "item_id": "101",
            "name": "test item",
            "category": "Math class",
            "number": 1,
            "year": 2020,
            "size": 30,
            "comments": None,
        ]}
    """

    with open(path, "w", encoding="utf-8") as f:
        f.write(test_data)

    with pytest.raises(CatalogError):
        catalog.load_catalog(path)

def test_saving_element_after_loading(tmp_path):
    path = tmp_path / "catalog.json"
    test_data = {
        "format_version": "2.0.0",
        "items": [
            {
                "item_id": "505",
                "name": "test item",
                "category": "Math class",
                "number": 1,
                "year": 2020,
                "size": 30,
                "comments": None,
            },
            {
                "item_id": "101",
                "name": "test item",
                "category": "Math class",
                "number": 1,
                "year": 2020,
                "size": 30,
                "comments": None,
            }
        ]
    }

    classroom = Classroom(item_id="101", name="test classroom", number=1, year=2020, size=30, comments=None, category="Math class")
    catalog = Catalog()
    catalog.add(classroom)
    catalog_copy = Catalog()
    catalog_copy.add(classroom)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4)

    with pytest.raises(ItemAlreadyExistsError):
        catalog.load_catalog(path)

    assert catalog == catalog_copy