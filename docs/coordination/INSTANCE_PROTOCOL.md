# LLM Instance Coordination Protocol

## Overview
This document defines how different LLM instances should coordinate their work on the project. Following this protocol is mandatory for all LLM instances.

## Instance Initialization Process

1. **Read Order**
   ```
   1. /docs/coordination/INSTANCE_PROTOCOL.md (this file)
   2. /docs/project/PROJECT_CONTEXT.md
   3. /docs/progress/STATUS.md
   4. Relevant component docs based on planned work
   ```

2. **Before Starting Work**
   - Check STATUS.md for any LOCKED components
   - Update STATUS.md with your session ID and intentions
   - Mark relevant components as LOCKED
   - Create git branch if needed: `feature/session_[ID]`

3. **During Work**
   - Regularly commit with prefix `[SESSION_ID]`
   - Update documentation in-line with work
   - Keep STATUS.md current
   - If hitting context limits, document state clearly before stopping

4. **After Completing Work**
   - Update all relevant documentation
   - Mark components as READY or REVIEW_NEEDED
   - Create summary of changes in DEVELOPMENT_LOG.md
   - Remove LOCKED status

## Documentation Standards

1. **Commit Messages**
   ```
   [SESSION_ID] type(scope): description
   
   - type: feat|fix|docs|style|refactor
   - scope: component affected
   - description: clear, present tense
   ```

2. **Status Updates**
   ```markdown
   ## Component: [Name]
   Status: [LOCKED|READY|REVIEW_NEEDED]
   Last Updated: [ISO datetime]
   Last Instance: [SESSION_ID]
   Current Work: [Brief description]
   Next Steps: [List of TODOs]
   ```

3. **Development Log Entries**
   ```markdown
   ### [ISO Date] - Session [ID]
   - Work completed: [Description]
   - Files changed: [List]
   - Decisions made: [List]
   - Next steps: [List]
   ```

## Context Management
- Maximum context to use: 150k tokens (leaving buffer)
- If approaching limit:
  1. Document current state
  2. Create clear "continuation point"
  3. Notify human
  4. New instance can pick up from continuation point

## Error Recovery
If an instance encounters errors or confusion:
1. Document the issue in ROADBLOCKS.md
2. Mark affected components as REVIEW_NEEDED
3. Document what was attempted and why it failed
4. Request human intervention if needed

## Coordination with Human Developer

1. **Reading Human Changes**
   - Check for [HUMAN] commit prefixes
   - Read HUMAN_CHANGES.md if exists
   - Validate changes against project goals

2. **Responding to Human Input**
   - Acknowledge understanding of changes
   - Update documentation to reflect changes
   - Flag any concerns or inconsistencies

3. **Requesting Human Input**
   - Create clear, specific questions
   - Document context of request
   - Provide options if applicable