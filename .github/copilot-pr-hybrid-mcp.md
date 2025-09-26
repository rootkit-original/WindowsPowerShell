# Copilot Task Instructions – Hybrid MCP Implementation

When tagging **@copilot** on GitHub for this repository, use these instructions to keep the automation focused on the new hybrid MCP architecture work.


## 🎯 Mission

Implement the hybrid MCP architecture described in `ROADMAP.md` and `MIGRATION_PLAN.md`, replacing the legacy clean-architecture-only layout.


## 🧱 Scope Checklist

1. **MCP Core** (`Scripts/xkit/mcp/`)
   - Implement `client.py`, `protocol.py`, and internal servers (core, ai, git).
   - Provide connection management (stdio/HTTP), discovery, and config wiring.
   - Add unit/integration tests covering tool listing and command execution paths.
2. **Plugin System** (`Scripts/xkit/plugins/`)
   - Create `base.py`, `manager.py`, `loader.py`, and migrate existing services into plugins under `plugins/core/`.
   - Support hot-reload, discovery, dependency declaration, and error isolation.
3. **Event-Driven Layer** (`Scripts/xkit/events/`)
   - Build `bus.py`, `events.py`, `handlers/`, and optional middleware.
   - Ensure async publishing/subscription, retries, and replay hooks.
4. **Hexagonal Core** (`Scripts/xkit/core/`)
   - Define domain entities, application services, and ports.
   - Move adapters into `adapters/cli`, `adapters/external`, etc., wiring them through ports.
5. **PowerShell Bridge** (`oh-my-xkit/`)
   - Keep wrappers minimal: delegate to Python entry points and ensure compatibility with new modules.
6. **Compatibility + Docs**
   - Maintain backward compatibility (`xkit_main.py`, public commands, error handling).
   - Update docs/tests referencing new modules; keep Conventional Commits.

## ✅ Acceptance Criteria

- All new modules follow the directory structure defined in `ROADMAP.md`.
- Automated tests cover MCP client/server interactions, plugin lifecycle, event publishing, and key use cases.
- Backwards compatibility validated via existing CLI flows (`xkit-minimal.ps1`, common commands).
- Documentation and changelog entries updated where behaviour changes.
- No orphaned legacy files (e.g., ensure removed scripts are replaced or adapters updated).


## 🧪 Validation

- Run targeted Python tests (pytest) and smoke-test the PowerShell wrapper.
- Document commands executed and their results in the PR summary.
- Provide migration notes for developers (breakdown of major refactors).


## 📌 Usage Tips

- Mention `@copilot` with a short summary plus a link to this file to activate the agent.
- Keep PRs scoped: prefer iterative merges (MCP core → plugins → events → integration) if work becomes too large.
- If blocking issues arise, open a discussion or issue before deviating from this plan.
