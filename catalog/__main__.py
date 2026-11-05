from .catalog import Catalog
from .model import Classroom


def main() -> None:
    catalog = Catalog()
    catalog.add(Classroom("001", "Math room", 101, "Math", 2020, 30))
    catalog.add(Classroom("002", "Chemistry lab", 102, "Science", 2022, 20))

    print("All classrooms:")
    for room in catalog:
        print(room)

    print("Number of classrooms:", len(catalog))
    print("ID 001 exists:", "001" in catalog)
    print("Get by ID:", catalog.get("001"))
    print("Search by name:", *catalog.find_by_name("MATH"))
    print("Search by category:", *catalog.find_by_category("science"))
    print("Removed classroom:", catalog.remove("001"))
    print("Classrooms left:", len(catalog))


if __name__ == "__main__":
    main()
