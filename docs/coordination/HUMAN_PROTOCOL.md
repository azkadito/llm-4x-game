# Human Developer Protocol

## Overview
This document outlines how to effectively coordinate between human developer actions and LLM instances working on the project.

## Options for Recording Human Changes

### Option 1: Dedicated Change Log
- Create changes in code/docs as needed
- Add entry to HUMAN_CHANGES.md:
  ```markdown
  ## [ISO Date]
  ### Changes Made
  - [Description of changes]
  - Files affected: [list]
  
  ### Context/Rationale
  [Explanation if needed]
  
  ### Follow-up Needed?
  [Yes/No - what needs to be done]
  ```

### Option 2: Git Commit Protocol
- Prefix all commits with [HUMAN]
- Use detailed commit messages:
  ```
  [HUMAN] type(scope): description
  
  - Detailed explanation if needed
  - Any follow-up tasks
  ```

### Option 3: GitHub Issues
- Create issue for each change
- Tag with 'human-change'
- Include:
  - What was changed
  - Why it was changed
  - Any follow-up needed

## Recommended Approach
For this project, we recommend using **Option 1 (Dedicated Change Log)** because:
- Keeps all human changes in one place
- Easy for LLMs to parse and understand
- Doesn't clutter git history
- Allows for detailed context

## Process for Making Changes

1. **Before Making Changes**
   - Check STATUS.md for any LOCKED components
   - Avoid changing LOCKED components without coordination
   - Create new HUMAN_CHANGES.md entry if needed

2. **During Changes**
   - Make changes as needed
   - Document immediately in HUMAN_CHANGES.md
   - If extensive changes, consider creating GitHub issue

3. **After Changes**
   - Update HUMAN_CHANGES.md
   - Mark any components that need review
   - Update STATUS.md if needed

## Examples

### Good Change Log Entry
```markdown
## 2025-01-20
### Changes Made
- Modified map generation parameters in src/generators/map.py
- Adjusted hex grid size calculations
- Files: src/generators/map.py, src/config/map_config.py

### Context/Rationale
Performance testing showed slower generation with original parameters.
New values improve generation time by ~30%.

### Follow-up Needed?
Yes - LLM should update performance documentation and verify changes
don't impact map quality.
```

### Poor Change Log Entry
```markdown
## 2025-01-20
Changed some map stuff to make it faster.
```

## Guidelines for Different Types of Changes

### Code Changes
- Document specific files changed
- Note any performance implications
- Highlight changes to interfaces

### Configuration Changes
- List all changed parameters
- Explain rationale
- Note any testing needed

### Documentation Changes
- Note which docs were updated
- Explain why changes were needed
- Flag if LLM docs need updating

## When to Involve LLM

1. **Always Notify For**:
   - Architecture changes
   - Interface changes
   - Performance-critical changes
   - Documentation structure changes

2. **Optional Notification For**:
   - Minor bug fixes
   - Comment updates
   - Formatting changes
   - Documentation typos

## Emergency Protocol

If you need to make urgent changes without documentation:
1. Add [EMERGENCY] tag to commits
2. Create high-priority issue
3. Update docs as soon as possible afterward