"""
Hex Grid System Implementation

This module implements the core hex grid system using cube coordinates.
"""

from typing import Dict, List, Optional
from .types import HexCoord, HexCell
from .pathfinding import PathFinder

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
            # Lerp coordinates
            x = start.coord.x + (end.coord.x - start.coord.x) * t
            y = start.coord.y + (end.coord.y - start.coord.y) * t
            z = start.coord.z + (end.coord.z - start.coord.z) * t
            
            # Round to nearest hex
            rx = round(x)
            ry = round(y)
            rz = round(z)
            
            # Fix rounding errors
            x_diff = abs(rx - x)
            y_diff = abs(ry - y)
            z_diff = abs(rz - z)
            
            if x_diff > y_diff and x_diff > z_diff:
                rx = -ry - rz
            elif y_diff > z_diff:
                ry = -rx - rz
            else:
                rz = -rx - ry
            
            coord = HexCoord(rx, ry, rz)
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
        return result  # Added return statement here