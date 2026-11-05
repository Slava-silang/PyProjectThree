# Classroom Catalog

A simple Python project for storing classroom information. It supports adding, finding, removing, saving, and loading classrooms. The project is used through Python code and has no command-line menu.

## Requirements

Python 3.12 or newer. The main code uses only the Python standard library.

To install development tools with uv:

```bash
uv sync
```

## Classroom fields



* `item_id` | Unique classroom ID | Non-empty string |
* `name` | Classroom name | Non-empty string |
* `number` | Room number | Positive integer |
* `category` | Classroom category | Non-empty string |
* `year` | Year of the last renovation | Integer from 0 to the current year |
* `size` | Number of student seats | Positive integer |
* `comments` | Extra information | String or `None`; default is `None` |

Fields are checked when a classroom is created.

## Catalog methods


* `add(item)` | Adds a `Classroom` with a unique ID 
* `get(item_id)` | Finds a classroom by its string ID 
* `remove(item_id)` | Removes a classroom by its string ID 
* `find_by_name(name)` | Searches for text in classroom names 
* `find_by_category(category)` | Searches for text in categories 
* `load_catalog(path)` | Loads classrooms from a JSON file  
* `save_catalog(path)` | Saves classrooms to a JSON file  
* `add_version_1_0_0(items)` | Adds a list of dictionaries in the old format  
* `add_version_2_0_0(items)` | Adds a list of dictionaries in the current format  

Search accepts part of a name or category and ignores letter case. No matches returns an empty list. An empty search string matches all classrooms.

## Other operations

* `len(catalog)` returns the number of classrooms.
* `"001" in catalog` checks whether an ID exists.
* A `for` loop returns classroom copies in the order they were added.
* `catalog == other_catalog` compares classroom data. It ignores the file format version and item order. Comparing with another type raises `NotImplementedError`.

Getting, searching, and iterating return copies. But `add()` put the original object, so changing that object later also changes the stored classroom.

## JSON files

The default file format version is `2.0.0`:

```json
{
    "format_version": "2.0.0",
    "items": [
        {
            "item_id": "001",
            "name": "Math classroom",
            "number": 101,
            "category": "Math",
            "year": 2020,
            "size": 30,
            "comments": "Has a projector"
        }
    ]
}
```

The program can load two versions:

- `1.0.0`: items must not include `year`. The loader sets it to `2000`.
- `2.0.0`: items include `year`. The `comments` field is optional.

Loading adds items to the existing catalog. Duplicate IDs are rejected, including IDs already in the catalog. If loading fails, the existing catalog stays unchanged.

## Errors

* `CatalogError` | Base catalog error
* `InvalidItemError` | Invalid classroom data
* `ItemNotFoundError` | No classroom has the requested ID 
* `ItemAlreadyExistsError` | The ID is already in use 
* `InvalidItemInFile` | Invalid JSON, file structure, or classroom data 
* `InvalidVersionError` | Unsupported file format version


## Tests

Run the tests from the project folder:

```bash
uv run pytest
```

The tests cover classroom validation, catalog operations, searching, iteration, JSON saving and loading, and error handling.