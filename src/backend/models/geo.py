from enum import Enum
from typing import Tuple

from pydantic import BaseModel


class GeoType(str, Enum):
    point = "Point"


class GeoObject(BaseModel):
    type: GeoType = GeoType.point
    coordinates: Tuple[float, float]
