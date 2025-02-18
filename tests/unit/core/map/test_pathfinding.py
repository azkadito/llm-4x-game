"""
Unit tests for the hex grid pathfinding system.
"""

import pytest
from src.core.map.types import HexCell, HexCoord
from src.core.map.hex_grid import HexGrid
from src.core.map.pathfinding import PathFinder, PathNode

class TestPathNode:
    """Test pathfinding node functionality."""

    def test_node_comparison(self):
        """Test node comparison for priority queue."""
        cell = HexCell(HexCoord(0, 0, 0))
        
        # Node with lower f_cost should be chosen first
        node1 = PathNode(cell, g_cost=1, h_cost=2)  # f_cost = 3
        node2 = PathNode(cell, g_cost=2, h_cost=2)  # f_cost = 4
        assert node1 < node2

        # With equal f_costs, lower h_cost should be chosen
        node3 = PathNode(cell, g_cost=2, h_cost=1)  # f_cost = 3
        assert node3 < node1

    def test_node_costs(self):
        """Test node cost calculations."""
        cell = HexCell(HexCoord(0, 0, 0))
        node = PathNode(cell, g_cost=5, h_cost=3)
        assert node.f_cost == 8

    def test_node_comparison_different_f_costs(self):
        """Test node comparison with different f_costs."""
        cell = HexCell(HexCoord(0, 0, 0))
        
        # Create nodes with very different f_costs
        node1 = PathNode(cell, g_cost=1, h_cost=1)  # f_cost = 2
        node2 = PathNode(cell, g_cost=10, h_cost=10)  # f_cost = 20
        
        assert node1 < node2  # Lower f_cost should be chosen first
        assert not (node2 < node1)  # Higher f_cost should not be chosen first

class TestPathFinder:
    """Test pathfinding functionality."""

    @pytest.fixture
    def grid(self):
        """Create a test grid."""
        return HexGrid(3)  # Radius 3 for more complex paths

    def test_simple_path(self, grid):
        """Test pathfinding between adjacent cells."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(1, -1, 0)
        
        path = grid.find_path(start, end)
        assert path is not None
        assert len(path) == 2
        assert path[0] == start
        assert path[-1] == end

    def test_complex_path(self, grid):
        """Test pathfinding across multiple cells."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -2, 0)
        
        path = grid.find_path(start, end)
        assert path is not None
        assert len(path) > 2
        assert path[0] == start
        assert path[-1] == end
        
        # Check path continuity
        for i in range(len(path) - 1):
            assert grid.distance(path[i], path[i + 1]) == 1

    def test_path_with_costs(self, grid):
        """Test pathfinding with different movement costs."""
        start = grid.get_cell(0, 0, 0)
        mid = grid.get_cell(1, -1, 0)
        end = grid.get_cell(2, -2, 0)
        
        # Make middle cell expensive
        mid.data['movement_cost'] = 5.0
        
        path = grid.find_path(start, end)
        assert path is not None
        
        # Path should avoid expensive cell if possible
        assert mid not in path

    def test_path_with_max_cost(self, grid):
        """Test pathfinding with maximum cost limit."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(3, -3, 0)
        
        # Set a cost limit that's too low
        path = grid.find_path(start, end, max_cost=2.0)
        assert path is None

    def test_path_around_obstacles(self, grid):
        """Test pathfinding around high-cost areas."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -2, 0)
        
        # Create a line of expensive cells between start and end
        mid1 = grid.get_cell(1, -1, 0)
        mid2 = grid.get_cell(1, 0, -1)
        mid1.data['movement_cost'] = 10.0
        mid2.data['movement_cost'] = 10.0
        
        path = grid.find_path(start, end)
        assert path is not None
        assert mid1 not in path
        assert mid2 not in path

    def test_no_path_possible(self, grid):
        """Test when no path is possible."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -2, 0)
        
        # Surround start with infinite cost cells
        for neighbor in grid.get_neighbors(start):
            neighbor.data['movement_cost'] = float('inf')
            
        path = grid.find_path(start, end)
        assert path is None

    def test_path_reevaluation(self, grid):
        """Test path reevaluation when a better path is found."""
        start = grid.get_cell(0, 0, 0)  # (0,0,0)
        mid1 = grid.get_cell(1, -1, 0)  # Direct route
        mid2 = grid.get_cell(1, 0, -1)  # Alternative route
        mid3 = grid.get_cell(2, -1, -1) # Common point
        end = grid.get_cell(2, -2, 0)   # Destination

        # Set up movement costs to force reevaluation
        # Make direct route look good initially but be expensive overall
        mid1.data['movement_cost'] = 1.0  # Looks good...
        mid3.data['movement_cost'] = 5.0  # ...but then gets expensive

        # Make alternative route look worse initially but be better overall
        mid2.data['movement_cost'] = 2.0  # Looks worse...
        # ...but then uses common path with default cost 1.0

        path = grid.find_path(start, end)
        assert path is not None

        # Calculate total costs of both potential paths
        direct_cost = sum(cell.movement_cost for cell in [mid1, mid3])
        alternative_cost = sum(cell.movement_cost for cell in [mid2])

        print(f"\nDebug path info:")
        print(f"Path found: {[(c.coord.x, c.coord.y, c.coord.z) for c in path]}")
        print(f"Direct route cost: {direct_cost}")
        print(f"Alternative route cost: {alternative_cost}")

        # Should choose the cheaper path
        assert mid2 in path