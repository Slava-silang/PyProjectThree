class CatalogError(Exception):
    pass
class InvalidItemError(CatalogError):
    pass
class ItemNotFoundError(CatalogError):
    pass
class ItemAlreadyExistsError(CatalogError):
    pass
class InvalidItemInFile(CatalogError):
    pass
class InvalidVersionError(CatalogError):
    pass