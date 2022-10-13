from enum import Enum


class Results(Enum):
    GOOD = 1
    PARTIAL = 2
    BAD = 3
    SUPERIOR = 69
    INFERIOR = 420


class Categories(Enum):
    GENDER = "gender"
    POSITION = "positions"
    SPECIES = "species"
    RESOURCE = "resource"
    RANGE_TYPE = "range_type"
    REGION = "regions"
    RELEASE_YEAR = "release_date"
    