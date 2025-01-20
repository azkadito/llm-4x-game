"""
Hex Grid System Implementation

This module implements the core hex grid system using cube coordinates.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math
from .pathfinding import PathFinder

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

class HexGrid:
    """Manages the hex grid map."""
    
    # Directions for neighbor calculations (cube coordinates)
    DIRECTIONS = [
        (+1, -1, 0), (+1, 0, -1), (0, +1, -1),
        (-1, +1, 0), (-1, 0, +1), (0, -1, +1)
    ]

    def __init__(self, radius: int):
        """Initialize a hex grid with given radius from center."""
        self.radius = radius
        self.cells: Dict[HexCoord, HexCell] = {}
        self._generate_grid()
        self.pathfinder = PathFinder()

    def _generate_grid(self):
        """Generate the initial grid of cells."""
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                coord = HexCoord(q, r, -q-r)
                self.cells[coord] = HexCell(coord)

    def get_cell(self, x: int, y: int, z: int) -> Optional[HexCell]:
        """Get cell at specified coordinates."""
        coord = HexCoord(x, y, z)
        return self.cells.get(coord)

    def get_neighbors(self, cell: HexCell) -> List[HexCell]:
        """Get all neighboring cells."""
        neighbors = []
        for dx, dy, dz in self.DIRECTIONS:
            neighbor_coord = HexCoord(
                cell.coord.x + dx,
                cell.coord.y + dy,
                cell.coord.z + dz
            )
            if neighbor_coord in self.cells:
                neighbors.append(self.cells[neighbor_coord])
        return neighbors

    @staticmethod
    def distance(a: HexCell, b: HexCell) -> int:
        """Calculate distance between two cells."""
        return max(
            abs(a.coord.x - b.coord.x),
            abs(a.coord.y - b.coord.y),
            abs(a.coord.z - b.coord.z)
        )

    def get_line(self, start: HexCell, end: HexCell) -> List[HexCell]:
        """Get all cells in a line between start and end."""
        N = self.distance(start, end)
        if N == 0:
            return [start]
        
        results = []
        for i in range(N + 1):
            t = i / N
            x = round(start.coord.x * (1-t) + end.coord.x * t)
            y = round(start.coord.y * (1-t) + end.coord.y * t)
            z = round(start.coord.z * (1-t) + end.coord.z * t)
            coord = HexCoord(x, y, z)
            if coord in self.cells:
                results.append(self.cells[coord])
        return results

    def find_path(self, start: HexCell, end: HexCell, max_cost: float = float('inf')) -> Optional[List[HexCell]]:
        """
        Find a path between two cells using A* algorithm.
        
        Args:
            start: Starting hex cell
            end: Target hex cell
            max_cost: Maximum total path cost (optional)
            
        Returns:
            List of cells forming the path, or None if no path found
        """
        return self.pathfinder.find_path(
            start=start,
            end=end,
            get_neighbors=self.get_neighbors,
            max_cost=max_cost
        )

    def cells_in_range(self, center: HexCell, max_distance: int) -> List[HexCell]:
        """Get all cells within a certain distance of a center cell."""
        result = []
        for q in range(-max_distance, max_distance + 1):
            r1 = max(-max_distance, -q - max_distance)
            r2 = min(max_distance, -q + max_distance)
            for r in range(r1, r2 + 1):
                s = -q - r
                if abs(q) + abs(r) + abs(s) <= 2 * max_distance:
                    coord = HexCoord(
                        center.coord.x + q,
                        center.coord.y + r,
                        center.coord.z + s
                    )
                    if coord in self.cells:
                        result.append(self.cells[coord])
        return result