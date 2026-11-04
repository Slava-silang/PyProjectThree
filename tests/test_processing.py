import pytest

from catalog.catalog import Catalog
from catalog.errors import InvalidItemError, ItemAlreadyExistsError, ItemNotFoundError
from catalog.model import Classroom


def test_creating_right_classroom():
    """Check that a classroom stores the given field values."""
    classroom = Classroom(
        item_id="001",
        name="test",
        number=1,
        category="Math classroom",
        year=2020,
        comments="Great",
        size=30,
    )

    assert classroom.item_id == "001"
    assert classroom.name == "test"
    assert classroom.number == 1
    assert classroom.category == "Math classroom"
    assert classroom.year == 2020
    assert classroom.comments == "Great"
    assert classroom.size == 30


def test_creating_wrong_item_id():
    """Check that invalid field values raise errors."""
    with pytest.raises(InvalidItemError):
        Classroom(
            item_id=101,
            name="test",
            number=1,
            category="Math classroom",
            year=2020,
            comments="Great",
            size=30,
        )

    with pytest.raises(InvalidItemError):
        Classroom(
            item_id="101",
            name=123,
            number=1,
            category="Math classroom",
            year=2020,
            comments="Great",
            size=30,
        )

    with pytest.raises(InvalidItemError):
        Classroom(
            item_id="101",
            name="test",
            number=-100,
            category="Math classroom",
            year=2020,
            comments="Great",
            size=30,
        )

    with pytest.raises(InvalidItemError):
        Classroom(
            item_id="101",
            name="test",
            number=1,
            category=True,
            year=2020,
            comments="Great",
            size=30,
        )

    with pytest.raises(InvalidItemError):
        Classroom(
            item_id="101",
            name="test",
            number=1,
            category="Math classroom",
            year=-2020,
            comments="Great",
            size=30,
        )

    with pytest.raises(InvalidItemError):
        Classroom(
            item_id="101",
            name="test",
            number=1,
            category="Math classroom",
            year=2020,
            comments=False,
            size=30,
        )

    with pytest.raises(InvalidItemError):
        Classroom(
            item_id="101",
            name="test",
            number=1,
            category="Math classroom",
            year=2020,
            comments="Great",
            size="30",
        )


def test_catalog_processing():
    """Check adding, getting, and removing classrooms."""
    classroom_1 = Classroom(
        item_id="001",
        name="test",
        number=1,
        category="Math classroom",
        year=2020,
        comments="Great",
        size=30,
    )

    classroom_2 = Classroom(
        item_id="002",
        name="common",
        number=2,
        category="Chemistry classroom",
        year=2010,
        comments="Great",
        size=40,
    )

    catalog = Catalog()

    catalog.add(classroom_1)
    catalog.add(classroom_2)

    assert classroom_1 == catalog.get(classroom_1.item_id)
    assert classroom_2 == catalog.get(classroom_2.item_id)

    catalog.remove(classroom_1.item_id)

    with pytest.raises(ItemNotFoundError):
        catalog.get(classroom_1.item_id)


def test_duplicate_item_id():
    """Check that duplicate classroom IDs are rejected."""
    classroom_1 = Classroom(
        item_id="001",
        name="test",
        number=1,
        category="Math classroom",
        year=2020,
        comments="Great",
        size=30,
    )

    classroom_2 = Classroom(
        item_id="001",
        name="common",
        number=13,
        category="Chemistry classroom",
        year=2010,
        comments="Great",
        size=40,
    )

    catalog = Catalog()

    catalog.add(classroom_1)

    with pytest.raises(ItemAlreadyExistsError):
        catalog.add(classroom_2)


def test_catalog_search():
    """Check searching by category and by name with different letter case."""
    classroom_1 = Classroom(
        item_id="001",
        name="test",
        number=1,
        category="Math classroom",
        year=2020,
        comments="Great",
        size=30,
    )

    catalog = Catalog()
    catalog.add(classroom_1)

    assert [classroom_1] == catalog.find_by_category(classroom_1.category)
    assert [classroom_1] == catalog.find_by_name("TEST")


def test_iteration():
    """Check that iteration returns classrooms in the order they were added."""
    classroom_1 = Classroom(
        item_id="001",
        name="test",
        number=1,
        category="Math classroom",
        year=2020,
        comments="Great",
        size=30,
    )

    classroom_2 = Classroom(
        item_id="002",
        name="common",
        number=13,
        category="Chemistry classroom",
        year=2010,
        comments="Great",
        size=40,
    )

    catalog = Catalog()
    catalog.add(classroom_1)
    catalog.add(classroom_2)

    items = [classroom_1, classroom_2]

    for k, item in enumerate(catalog, 0):
        assert item == items[k]
