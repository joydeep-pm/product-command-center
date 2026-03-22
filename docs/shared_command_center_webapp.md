# Shared Command Center Web App

## Objective

Turn the current static dashboard into an internal shared command center:
- Product team edits
- All other internal stakeholders view
- Live status, not browser-local status
- Manual updates in v1
- Internal-only access

## Why The Current HTML Is Not Enough

The current dashboard stores state in browser `localStorage`. That makes it:
- device-local
- browser-local
- non-auditable across users
- unsuitable as a shared source of truth

The UI is useful. The persistence model is not.

## V1 Architecture

### Frontend
- Reuse `/Users/joy/autoresearch/app/dashboard.html`
- Keep the current JavaScript-driven filtering, charts, and drilldowns
- Add shared-state support when the dashboard is served through the shared server

### Backend
- Local development server: `/Users/joy/autoresearch/webapp/server.js`
- Vercel deployment APIs: `/Users/joy/autoresearch/api/*.js`
- The UI contract stays the same: `/api/dashboard-state`, `/api/audit-log`, `/api/editor-check`

### Persistence
- Local fallback:
  - `/Users/joy/autoresearch/data/live_dashboard_state.json`
  - `/Users/joy/autoresearch/data/dashboard_audit_log.jsonl`
- Vercel deployment:
  - private Vercel Blob store `autoresearch-command-center`
  - state blob: `command-center/live_dashboard_state.json`
  - audit blob: `command-center/dashboard_audit_log.json`

This is intentionally simple. It is enough for low-write internal usage, but it is not a high-concurrency system.

## Shared State Model

Only business state is shared:
- `epicStatus`
- `epicNotes`
- `strStatus`
- `hireStatus`
- `decStatus`
- `galStatus`
- `customEpics`

Local viewer preferences remain browser-local:
- theme
- filter state
- editor key
- actor name
- one-shot pending reason

## API Contract

### `GET /api/dashboard-state`

Returns:
- `mode`
- `can_edit`
- `requires_editor_key`
- `storage_mode`
- `state`
- `meta.updated_at`
- `meta.updated_by`
- `meta.updated_reason`
- `meta.version`

### `POST /api/dashboard-state`

Request body:
```json
{
  "actor": "product-team",
  "note": "optional update note",
  "reason": "optional business reason",
  "state": {
    "epicStatus": {},
    "epicNotes": {},
    "strStatus": {},
    "hireStatus": {},
    "decStatus": [],
    "galStatus": {},
    "customEpics": []
  }
}
```

Behavior:
- validates editor access
- sanitizes to shared keys only
- writes the shared state envelope
- appends an audit event

### `GET /api/audit-log?limit=50`

Returns the most recent audit events.

### `GET /api/editor-check`

Returns whether the current request can edit.

## Write Access Model

For v1, read access is open to anyone with the deployed URL unless an additional network or access boundary is added.

Write access options:
1. Set `EDITOR_KEY`
2. Keep the app internal-only via company network, VPN, or reverse proxy

Without a network boundary, “no login” is not sufficient.

## Run Locally

Viewer mode only:
```bash
cd /Users/joy/autoresearch
node webapp/server.js
```

Editor mode with a shared key:
```bash
cd /Users/joy/autoresearch
EDITOR_KEY="replace-me" node webapp/server.js
```

Open:
- `http://127.0.0.1:8123/dashboard`

## Deployment Guidance

Current live deployment path:
- Vercel project `autoresearch`
- static dashboard rewrite via `/dashboard`
- serverless APIs backed by private Blob storage
- preview/production edits gated by `EDITOR_KEY`

Current limitation:
- the Vercel URL is public unless you add an external access boundary
- `EDITOR_KEY` protects writes, not reads

Do not treat this as truly internal-only until you add one of:
- company VPN / internal subnet
- reverse proxy / identity-aware proxy
- Vercel deployment protection or SSO-backed access control

## Next Step After V1

If usage sticks and edit volume increases:
- move from file-backed persistence to Postgres
- add SSO
- add entity-level audit diffs
- add snapshot history
- add upstream sync from Jira / Sheets
