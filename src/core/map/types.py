"""
Core types for the hex grid system.
"""

from dataclasses import dataclass
from typing import Dict, Any

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
        self.data: Dict[str, Any] = {}  # Generic container for cell data

    @property
    def movement_cost(self) -> float:
        """Calculate movement cost for the cell."""
        return self.data.get('movement_cost', 1.0)

    def __eq__(self, other):
        """Compare cells based on coordinates."""
        if not isinstance(other, HexCell):
            return NotImplemented
        return self.coord == other.coord

    def __hash__(self):
        """Make cells hashable based on coordinates."""
        return hash(self.coord)