# Hex Grid System Technical Specification

## Overview
This document specifies the technical implementation of the hex grid system that forms the foundation of our game map.

## Core Components

### 1. Coordinate System
- Using cube coordinates (x, y, z) where x + y + z = 0
- Benefits:
  - Simple arithmetic for movement
  - Easy rotation and reflection
  - Straightforward distance calculations
  - Natural neighbor calculations

### 2. Storage Structure
```python
class HexCell:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.terrain_type = None
        self.resources = []
        self.owner = None
        self.improvements = []
        self.units = []

class HexGrid:
    def __init__(self, radius: int):
        self.radius = radius
        self.cells = {}  # Dictionary with (x,y,z) tuple keys
        self.generate_grid()
```

### 3. Core Operations

#### Distance Calculation
```python
def hex_distance(a: HexCell, b: HexCell) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z))
```

#### Neighbor Calculation
```python
DIRECTIONS = [
    (1, -1, 0), (1, 0, -1), (0, 1, -1),
    (-1, 1, 0), (-1, 0, 1), (0, -1, 1)
]

def get_neighbors(cell: HexCell) -> List[HexCell]:
    return [
        HexCell(cell.x + dx, cell.y + dy, cell.z + dz)
        for dx, dy, dz in DIRECTIONS
    ]
```

### 4. Pathfinding
- Using A* algorithm optimized for hex grids
- Movement cost calculations based on:
  - Terrain type
  - Improvements
  - Unit type
  - Diplomatic status

## Performance Considerations

### 1. Memory Usage
- Estimated memory per cell: ~100 bytes
- For 200x200 map: ~4MB base memory
- Additional memory for units and improvements
- Target: <16MB total map memory

### 2. Processing Targets
- Pathfinding: <10ms for typical paths
- Visibility updates: <5ms
- Unit movement: <1ms
- Map generation: <1s for full map

### 3. Optimization Strategies
- Chunked loading for large maps
- Cached pathfinding results
- Spatial hashing for unit queries
- Lazy evaluation of visibility

## Implementation Phases

### Phase 1: Basic Structure
- Core HexCell and HexGrid classes
- Basic coordinate system
- Simple terrain generation
- Unit tests for core functionality

### Phase 2: Pathfinding
- A* implementation
- Movement cost calculations
- Path caching system
- Performance benchmarks

### Phase 3: Game Integration
- Resource system integration
- Unit movement system
- Visibility calculations
- Territory control

### Phase 4: Optimization
- Chunk loading system
- Memory optimization
- Performance tuning
- Extended testing

## Testing Strategy

### Unit Tests
- Coordinate calculations
- Distance measurements
- Neighbor identification
- Path validation
- Terrain generation

### Performance Tests
- Large map generation
- Pathfinding benchmarks
- Memory usage monitoring
- CPU profiling

### Integration Tests
- Unit movement
- Combat calculations
- Resource management
- Save/load functionality

## Usage Examples

### Basic Grid Creation
```python
# Create a hex grid with radius 10
grid = HexGrid(10)

# Add a unit to a cell
cell = grid.get_cell(0, 0, 0)
unit = Unit(unit_type="warrior")
cell.units.append(unit)

# Calculate path
start = grid.get_cell(0, 0, 0)
end = grid.get_cell(5, -2, -3)
path = grid.find_path(start, end)
```

### Terrain Generation
```python
# Generate basic terrain
grid.generate_terrain(seed=12345)

# Add resources
grid.distribute_resources()

# Calculate initial visibility
grid.update_visibility()
```