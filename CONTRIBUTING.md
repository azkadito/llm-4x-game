# Contributing Guidelines

## Overview
This document outlines the process for contributing to the LLM-powered 4X strategy game project, whether you're a human developer or an LLM instance.

## Getting Started

### Prerequisites
- Python 3.10+
- Godot 4.x
- See requirements.txt for additional dependencies

### Development Environment Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install Godot 4.x
4. Review documentation in /docs

## Development Process

### 1. Coordination
- Check STATUS.md for component status
- Review INSTANCE_PROTOCOL.md (LLMs) or HUMAN_PROTOCOL.md (humans)
- Update status before beginning work
- Document all changes

### 2. Branching Strategy
- Main branch: stable releases
- Development branch: integration
- Feature branches: `feature/[description]`
- Fix branches: `fix/[description]`

### 3. Commit Standards
```
[SESSION_ID] type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Testing
- chore: Maintenance

Example:
[LLM_20250120_002] feat(hex): Add hex grid implementation
```

### 4. Code Style
- Follow PEP 8 for Python code
- Use GDScript style guide for Godot
- Maximum line length: 100 characters
- Clear, descriptive variable names
- Document all public functions/methods

### 5. Testing Requirements
- Unit tests for all new features
- Integration tests for system interactions
- Performance tests for critical operations
- See TESTING.md for details

## Documentation

### Required Documentation
1. Technical Documentation
   - Architecture overview
   - System specifications
   - API documentation
   - Performance considerations

2. Game Design Documentation
   - Mechanics descriptions
   - Content guidelines
   - Balance considerations
   - Feature specifications

3. Implementation Notes
   - Development decisions
   - Technical tradeoffs
   - Performance optimizations
   - Known limitations

### Documentation Style
- Clear, concise language
- Code examples where appropriate
- Diagrams for complex systems
- Regular updates as systems evolve

## Review Process

### Code Review Guidelines
1. Performance
   - Meets performance targets
   - Efficient algorithms
   - Resource management
   - Memory usage

2. Code Quality
   - Clean, readable code
   - Proper error handling
   - Good separation of concerns
   - Appropriate use of design patterns

3. Testing
   - Comprehensive test coverage
   - Edge case handling
   - Performance benchmarks
   - Integration testing

4. Documentation
   - Clear inline comments
   - Updated technical docs
   - API documentation
   - Usage examples

### Review Checklist
```markdown
## Code Review Checklist

### Functionality
- [ ] Implements specified requirements
- [ ] Handles edge cases
- [ ] Error handling is appropriate
- [ ] Performance meets targets

### Code Quality
- [ ] Follows style guide
- [ ] No unnecessary complexity
- [ ] DRY principles followed
- [ ] Clear variable/function names

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests if needed
- [ ] Performance tests if critical
- [ ] All tests pass

### Documentation
- [ ] Code is documented
- [ ] Technical docs updated
- [ ] Examples provided
- [ ] Changes logged
```

## Performance Guidelines

### Targets
- Frame rate: 60 FPS minimum
- Memory usage: <500MB
- Load times: <5 seconds
- Map generation: <1 second
- AI response: <100ms

### Optimization Guidelines
1. Early Optimization
   - Data structure selection
   - Algorithm efficiency
   - Memory management
   - Resource loading

2. Profiling
   - Regular performance testing
   - Memory profiling
   - CPU profiling
   - Loading time analysis

3. Optimization Areas
   - Critical game loops
   - Resource management
   - AI systems
   - Rendering pipeline

## Issue Management

### Bug Reports
- Use bug report template
- Include reproduction steps
- Attach relevant logs
- Note system configuration

### Feature Requests
- Clear problem statement
- Use case description
- Implementation suggestions
- Consider alternatives

### Issue Labels
- bug: Bug reports
- enhancement: Feature requests
- documentation: Doc updates
- performance: Performance issues
- ai: AI/LLM related

## Release Process

### Version Numbering
- Major.Minor.Patch
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Release Checklist
1. Preparation
   - All tests pass
   - Documentation updated
   - Performance verified
   - Release notes prepared

2. Testing
   - Full test suite
   - Performance benchmarks
   - Integration testing
   - Manual testing

3. Release
   - Version bump
   - Change log update
   - Tag creation
   - Binary creation

4. Post-Release
   - Deployment verification
   - Monitor for issues
   - Update documentation
   - Plan next release