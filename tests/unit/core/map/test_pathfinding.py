"""
Unit tests for the hex grid pathfinding system.
"""

import pytest
from src.core.map.hex_grid import HexGrid, HexCell, HexCoord, TerrainType
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

    def test_path_with_terrain(self, grid):
        """Test pathfinding with different terrain costs."""
        start = grid.get_cell(0, 0, 0)
        mid = grid.get_cell(1, -1, 0)
        end = grid.get_cell(2, -2, 0)
        
        # Make middle cell mountainous
        mid.terrain = TerrainType.MOUNTAINS
        
        path = grid.find_path(start, end)
        assert path is not None
        
        # Path should avoid mountains if possible
        assert mid not in path

    def test_path_with_max_cost(self, grid):
        """Test pathfinding with maximum cost limit."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(3, -3, 0)
        
        # Set a cost limit that's too low
        path = grid.find_path(start, end, max_cost=2.0)
        assert path is None

    def test_path_around_obstacles(self, grid):
        """Test pathfinding around impassable terrain."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -2, 0)
        
        # Create a line of mountains between start and end
        mid1 = grid.get_cell(1, -1, 0)
        mid2 = grid.get_cell(1, 0, -1)
        mid1.terrain = TerrainType.MOUNTAINS
        mid2.terrain = TerrainType.MOUNTAINS
        
        path = grid.find_path(start, end)
        assert path is not None
        assert mid1 not in path
        assert mid2 not in path

    def test_no_path_possible(self, grid):
        """Test when no path is possible."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -2, 0)
        
        # Surround start with mountains
        for neighbor in grid.get_neighbors(start):
            neighbor.terrain = TerrainType.MOUNTAINS
            
        path = grid.find_path(start, end)
        assert path is None

    def test_cells_in_range(self, grid):
        """Test finding all cells within a range."""
        center = grid.get_cell(0, 0, 0)
        
        # Test range 1
        cells = grid.cells_in_range(center, 1)
        assert len(cells) == 7  # Center + 6 neighbors
        
        # Test range 2
        cells = grid.cells_in_range(center, 2)
        assert len(cells) == 19  # Previous 7 + 12 cells in second ring