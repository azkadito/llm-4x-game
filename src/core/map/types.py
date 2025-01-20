"""
Common types used in the map system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

class TerrainType(Enum):
    """Terrain types for hex cells."""
    PLAINS = "plains"
    MOUNTAINS = "mountains"
    WATER = "water"
    FOREST = "forest"
    DESERT = "desert"

class ResourceType(Enum):
    """Resource types that can appear in cells."""
    NONE = "none"
    IRON = "iron"
    WOOD = "wood"
    GOLD = "gold"
    FOOD = "food"

@dataclass
class HexCoord:
    """Represents a hex cell coordinate using cube coordinates."""
    x: int
    y: int
    z: int

    def __post_init__(self):
        """Validate that the coordinates sum to zero."""
        if self.x + self.y + self.z != 0:
            raise ValueError(f"Invalid hex coordinates: {self.x}, {self.y}, {self.z}")

    def __hash__(self):
        """Make coordinates hashable for dict keys."""
        return hash((self.x, self.y, self.z))

class HexCell:
    """Represents a single hex cell in the grid."""
    
    def __init__(self, coord: HexCoord):
        self.coord = coord
        self.terrain: TerrainType = TerrainType.PLAINS
        self.resources: List[ResourceType] = []
        self.owner: Optional[int] = None  # Player ID
        self.improvements: List[str] = []
        self.units: List[str] = []  # Unit IDs
        self.visibility: Dict[int, bool] = {}  # Player ID -> visibility

    @property
    def movement_cost(self) -> float:
        """Calculate base movement cost for the cell."""
        terrain_costs = {
            TerrainType.PLAINS: 1.0,
            TerrainType.MOUNTAINS: 2.0,
            TerrainType.WATER: 1.5,
            TerrainType.FOREST: 1.5,
            TerrainType.DESERT: 1.2
        }
        return terrain_costs[self.terrain]

    def __eq__(self, other):
        """Compare cells based on coordinates."""
        if not isinstance(other, HexCell):
            return NotImplemented
        return self.coord == other.coord

    def __hash__(self):
        """Make cells hashable based on coordinates."""
        return hash(self.coord)