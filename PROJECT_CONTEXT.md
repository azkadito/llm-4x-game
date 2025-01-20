# Project Context and History

## Original Project Vision
- 2D 4X strategy game with LLM-powered dynamic storytelling
- Single player focused (multiplayer explicitly descoped for initial version)
- Key innovation: "zoom in" feature where players can experience different narrative perspectives within their empire:
  - Range from street vendor to prime minister perspectives
  - Both observational and interactive events
  - Could be brief events or extended dialogues/sequences
  - Narrative choices can affect gameplay
- LLMs will be used for:
  - Narrative generation
  - Enemy AI
  - Dynamic event creation
  - Must understand game context (resources, demographics, relationships, etc.)

## Development Context
- Developer background:
  - Python programming experience
  - Extensive 4X gaming experience (thousands of hours in Civilization titles and Humankind)
  - Student status, planning to work after graduation
- Time constraints:
  - Target development time: ~1 year
  - Part-time development

## Technical Exploration History
- Considered but ruled out:
  - Building upon FreeCiv (decided fresh start better aligns with goals)
  - 3D development (would require 2-3x development time)
  - Complex multiplayer features (focusing on core experience first)
- Explored LLM integration options:
  - Local model deployment
  - API-based integration
  - Hybrid approach (pre-generation + live generation)
- Investigated different game engines and frameworks

## Key Decisions Made

### Platform & Technology
1. **Dimensionality**: 2D over 3D
   - Rationale: 
     - Significantly reduced development complexity
     - Better suited for first game project
     - 3D would require 2-3x development time
     - Focus on core gameplay and AI innovation

2. **Game Engine**: Godot
   - Rationale:
     - Good 2D support
     - Python-like syntax (GDScript)
     - Free and open source
     - Active community
     - Easier learning curve than alternatives

3. **Map System**: Hex Grid
   - Rationale:
     - Good balance of complexity vs features
     - Better suited for storytelling (organic feel)
     - Modern feel while still being familiar
     - Not too complex for first project
     - Good community resources available

### Development Philosophy
- Focus on core systems first
- Keep extensibility in mind for future features
- Modular architecture with clear separation of concerns
- Test-driven development from the start
- Scalability considerations built into initial design
- Asynchronous LLM processing to handle generation latency

## Repository Structure
The project is organized into the following structure:
```
/src
  /core           # Core game mechanics and state management
  /engine         # Game engine integration and setup
  /generators     # Map and content generators
  /ai             # AI systems (both game AI and LLM integration)
  /ui             # User interface components
  /data           # Game data and assets
  /utils          # Utility functions and helpers
  /tests          # Test suite
```

## Current Status
- Repository initialized
- Basic documentation created
- First major decision (hex grid) made
- Ready to begin core system implementation

## Known Constraints
- Single player only for initial version
- Must consider performance implications of LLM integration
- Need to manage scope to fit one-year timeline
- Initial focus on core mechanics before advanced features

## Open Questions & Future Decisions
1. State Management System
   - Central vs Event-driven vs Hybrid
   - Impact on performance and complexity

2. Scaling Approach
   - Map size limits
   - Unit count optimization
   - Performance targets

3. LLM Integration Details
   - Local vs API vs Hybrid approach
   - Content caching strategy
   - Fallback mechanisms

## Resources & References
- README.md: Basic project information and setup
- DESIGN.md: Detailed technical decisions and architecture
- This document (PROJECT_CONTEXT.md): Historical context and vision