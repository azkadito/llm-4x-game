"""
Unit tests for the hex grid system.
"""

import pytest
from src.core.map.types import HexCell, HexCoord
from src.core.map.hex_grid import HexGrid

class TestHexCoord:
    """Test hex coordinate functionality."""

    def test_valid_coordinates(self):
        """Test creation of valid hex coordinates."""
        coord = HexCoord(1, -2, 1)
        assert coord.x == 1
        assert coord.y == -2
        assert coord.z == 1

    def test_invalid_coordinates(self):
        """Test that invalid coordinates raise ValueError."""
        with pytest.raises(ValueError):
            HexCoord(1, 1, 1)  # Sum != 0

    def test_coordinate_hash(self):
        """Test that coordinates can be used as dictionary keys."""
        coord1 = HexCoord(1, -1, 0)
        coord2 = HexCoord(1, -1, 0)
        coord_dict = {coord1: "test"}
        assert coord_dict[coord2] == "test"

class TestHexCell:
    """Test hex cell functionality."""

    @pytest.fixture
    def cell(self):
        """Create a test cell."""
        return HexCell(HexCoord(0, 0, 0))

    def test_initial_state(self, cell):
        """Test initial cell state."""
        assert cell.data == {}
        assert cell.movement_cost == 1.0

    def test_custom_movement_cost(self, cell):
        """Test custom movement cost."""
        cell.data['movement_cost'] = 2.0
        assert cell.movement_cost == 2.0

    def test_cell_comparison_with_non_cell(self, cell):
        """Test comparing cell with non-cell types."""
        assert cell != "not a cell"
        assert cell != 42
        assert cell != None

class TestHexGrid:
    """Test hex grid functionality."""

    @pytest.fixture
    def grid(self):
        """Create a test grid."""
        return HexGrid(2)  # Radius 2 grid

    def test_grid_initialization(self, grid):
        """Test that grid is created with correct number of cells."""
        # For radius 2, should have 19 cells
        assert len(grid.cells) == 19

    def test_get_cell(self, grid):
        """Test cell retrieval."""
        # Test getting existing cell
        cell = grid.get_cell(0, 0, 0)
        assert isinstance(cell, HexCell)
        assert cell.coord.x == 0
        assert cell.coord.y == 0
        assert cell.coord.z == 0
        
        # Test getting non-existent cell
        assert grid.get_cell(5, -2, -3) is None
        
        # Test getting cells at grid boundary
        assert grid.get_cell(2, -2, 0) is not None  # Should exist
        assert grid.get_cell(3, -3, 0) is None     # Should not exist
        
        # Test getting cells with invalid coordinates
        assert grid.get_cell(1, 1, 1) is None  # Sum != 0

    def test_get_nonexistent_cell(self, grid):
        """Test retrieving a cell that doesn't exist."""
        # Try to get a cell outside the grid's radius
        cell = grid.get_cell(5, -2, -3)
        assert cell is None

    def test_get_neighbors(self, grid):
        """Test neighbor retrieval."""
        center = grid.get_cell(0, 0, 0)
        neighbors = grid.get_neighbors(center)
        assert len(neighbors) == 6
        # Check each neighbor is distance 1 from center
        for neighbor in neighbors:
            assert grid.distance(center, neighbor) == 1

    def test_distance_calculation(self, grid):
        """Test distance calculations."""
        cell1 = grid.get_cell(0, 0, 0)
        cell2 = grid.get_cell(2, -1, -1)
        assert grid.distance(cell1, cell2) == 2

    def test_get_line(self, grid):
        """Test line drawing between cells."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -1, -1)
        line = grid.get_line(start, end)
        assert len(line) == 3  # Should include start, end, and one cell between
        assert line[0] == start
        assert line[-1] == end
        # Each cell should be adjacent to the next
        for i in range(len(line) - 1):
            assert grid.distance(line[i], line[i + 1]) == 1
            
        # Test edge cases for get_line
        # Line that would go outside grid
        far_end = grid.get_cell(2, -2, 0)
        line = grid.get_line(start, far_end)
        # Each cell in line should be in grid
        assert all(isinstance(c, HexCell) for c in line)
        assert all(abs(c.coord.x) <= grid.radius for c in line)
        assert all(abs(c.coord.y) <= grid.radius for c in line)
        assert all(abs(c.coord.z) <= grid.radius for c in line)

    def test_find_path(self, grid):
        """Test pathfinding between cells."""
        start = grid.get_cell(0, 0, 0)
        end = grid.get_cell(2, -1, -1)
        
        # Default path with base costs
        path = grid.find_path(start, end)
        assert path is not None
        assert len(path) >= 3  # Should include start, end, and at least one cell between
        assert path[0] == start
        assert path[-1] == end
        
        # Path with custom movement costs
        mid_cell = grid.get_cell(1, -1, 0)
        mid_cell.data['movement_cost'] = 10.0  # Make middle cell expensive
        
        path = grid.find_path(start, end)
        assert path is not None
        assert mid_cell not in path  # Path should avoid expensive cell

    def test_cells_in_range(self, grid):
        """Test finding all cells within a range."""
        center = grid.get_cell(0, 0, 0)
        
        # Test range 1
        cells = grid.cells_in_range(center, 1)
        assert len(cells) == 7  # Center + 6 neighbors
        
        # Test range 2
        cells = grid.cells_in_range(center, 2)
        assert len(cells) == 19  # Previous 7 + 12 cells in second ring

        # Verify distances
        for cell in cells:
            assert grid.distance(center, cell) <= 2