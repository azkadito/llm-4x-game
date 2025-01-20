# Startup Prompt for New Sessions

Use this prompt when starting a new chat session with an LLM:

```
You are helping me develop a 4X strategy game. The project repository is at https://github.com/azkadito/llm-4x-game. 

Before we begin, please read these documents in order:

1. Coordination Protocols:
   - /docs/coordination/INSTANCE_PROTOCOL.md (How to coordinate with other LLMs)
   - /docs/coordination/HUMAN_PROTOCOL.md (How to handle human interactions)

2. Project Overview:
   - /docs/project/PROJECT_CONTEXT.md (Project background and vision)
   - /docs/progress/STATUS.md (Current status and next steps)
   - /docs/progress/DEVELOPMENT_LOG.md (Recent history)

3. Design Documentation:
   - /docs/design/game/MECHANICS.md (Core game systems)
   - /docs/design/game/NARRATIVE.md (Storytelling systems)
   - /docs/design/technical/ARCHITECTURE.md (Technical design)

4. Decision Context:
   - /docs/decisions/DECISIONS_LOG.md (Major decisions and rationales)

After reading, please:
1. Generate and declare a new session ID following the format LLM_YYYYMMDD_XXX
2. Update STATUS.md with your session ID and intended work
3. Confirm your understanding by summarizing:
   - Current project state
   - Major decisions made so far
   - Game design vision
   - Immediate next steps
4. Wait for my confirmation before proceeding

For reference:
- My changes will be documented in HUMAN_CHANGES.md
- Technical decisions should be logged in DECISIONS_LOG.md
- Development progress should be logged in DEVELOPMENT_LOG.md
- New game design considerations should be discussed and documented appropriately

Note: If any files are missing or you need additional context, please let me know.
```

## Usage Instructions

1. **When to Use**
   - Starting new chat sessions
   - Switching to a new LLM instance
   - After long breaks in development

2. **Follow-up**
   - Verify the LLM has read and understood all documents
   - Confirm their summary is accurate
   - Provide any missing context or corrections

3. **Maintenance**
   - Keep document paths updated
   - Add new critical documents to reading list
   - Update reference section as needed