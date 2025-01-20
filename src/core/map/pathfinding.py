"""
A* Pathfinding implementation for hex grid.
"""

from typing import Dict, List, Set, Tuple, Optional, Callable
import heapq
from .types import HexCell

class PathNode:
    """Node used in pathfinding."""
    def __init__(self, cell: HexCell, g_cost: float = float('inf'),
                 h_cost: float = 0, parent: Optional['PathNode'] = None):
        self.cell = cell
        self.g_cost = g_cost  # Cost from start
        self.h_cost = h_cost  # Heuristic cost to end
        self.parent = parent
        
    @property
    def f_cost(self) -> float:
        """Total estimated cost (g_cost + h_cost)."""
        return self.g_cost + self.h_cost
    
    def __lt__(self, other: 'PathNode') -> bool:
        """Comparison for priority queue."""
        if self.f_cost == other.f_cost:
            return self.h_cost < other.h_cost
        return self.f_cost < other.f_cost

class PathFinder:
    """A* pathfinding implementation for hex grid."""
    
    def __init__(self, movement_cost_calculator: Optional[Callable[[HexCell], float]] = None):
        """Initialize pathfinder with optional custom movement cost calculator."""
        self.movement_cost_calculator = movement_cost_calculator or self._default_movement_cost

    def _default_movement_cost(self, cell: HexCell) -> float:
        """Default movement cost calculation."""
        return cell.movement_cost

    def _heuristic(self, current: HexCell, goal: HexCell) -> float:
        """Calculate heuristic cost (hex distance)."""
        return max(
            abs(current.coord.x - goal.coord.x),
            abs(current.coord.y - goal.coord.y),
            abs(current.coord.z - goal.coord.z)
        )

    def find_path(self, start: HexCell, end: HexCell,
                  get_neighbors: Callable[[HexCell], List[HexCell]],
                  max_cost: float = float('inf')) -> Optional[List[HexCell]]:
        """
        Find path between start and end cells using A* algorithm.
        
        Args:
            start: Starting hex cell
            end: Target hex cell
            get_neighbors: Function that returns valid neighbors for a cell
            max_cost: Maximum path cost (for limiting search)
            
        Returns:
            List of cells forming the path, or None if no path found
        """
        # Early exit if start or end has infinite cost
        if self._default_movement_cost(start) == float('inf') or \
           self._default_movement_cost(end) == float('inf'):
            return None

        # Initialize open and closed sets
        open_set: List[PathNode] = []
        closed_set: Set[HexCell] = set()
        
        # Create start node and add to open set
        start_node = PathNode(start, g_cost=0, h_cost=self._heuristic(start, end))
        heapq.heappush(open_set, start_node)
        
        # Track all nodes for backtracking
        all_nodes: Dict[HexCell, PathNode] = {start: start_node}
        
        while open_set:
            current_node = heapq.heappop(open_set)
            current_cell = current_node.cell
            
            if current_cell == end:
                return self._reconstruct_path(current_node)
                
            closed_set.add(current_cell)
            
            # Check all neighbors
            for neighbor in get_neighbors(current_cell):
                if neighbor in closed_set:
                    continue
                    
                movement_cost = self._default_movement_cost(neighbor)
                
                # Skip impassable cells
                if movement_cost == float('inf'):
                    continue
                    
                tentative_g_cost = current_node.g_cost + movement_cost
                
                if tentative_g_cost > max_cost:
                    continue
                
                if neighbor not in all_nodes:
                    neighbor_node = PathNode(
                        neighbor,
                        g_cost=tentative_g_cost,
                        h_cost=self._heuristic(neighbor, end),
                        parent=current_node
                    )
                    all_nodes[neighbor] = neighbor_node
                    heapq.heappush(open_set, neighbor_node)
                else:
                    neighbor_node = all_nodes[neighbor]
                    if tentative_g_cost < neighbor_node.g_cost:
                        neighbor_node.g_cost = tentative_g_cost
                        neighbor_node.parent = current_node
                        if neighbor_node not in open_set:
                            heapq.heappush(open_set, neighbor_node)
        
        return None  # No path found

    def _reconstruct_path(self, end_node: PathNode) -> List[HexCell]:
        """Reconstruct path from end node by following parent pointers."""
        path = []
        current = end_node
        while current is not None:
            path.append(current.cell)
            current = current.parent
        return list(reversed(path))