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
- Viewer-entry page: `/Users/joy/autoresearch/app/access.html`
- Protected Vercel routes:
  - `/api/dashboard-page`
  - `/api/command-center-data`
  - `/api/dashboard-state`
  - `/api/audit-log`
  - `/api/editor-check`
  - `/api/viewer-access`
  - `/api/viewer-logout`

### Persistence
- Local fallback:
  - `/Users/joy/autoresearch/data/live_dashboard_state.json`
  - `/Users/joy/autoresearch/data/dashboard_audit_log.jsonl`
- Vercel deployment:
  - private Vercel Blob store `autoresearch-command-center`
  - immutable state blobs under `command-center/state/*.json`
  - immutable audit blobs under `command-center/audit/*.json`

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

### `POST /api/viewer-access`

Request body:
```json
{
  "key": "shared-viewer-key",
  "next": "/dashboard"
}
```

Behavior:
- validates the shared viewer key
- sets the viewer cookie
- returns the next route to open

### `POST /api/viewer-logout`

Behavior:
- clears the viewer cookie
- returns `{ "ok": true }`

## Access Model

For v1, the live app now has a real shared-viewer boundary:
- viewers enter `VIEWER_KEY` on `/access`
- product editors separately enable edit mode with `EDITOR_KEY`
- protected routes reject requests without viewer access
- `/dashboard` is served through a guarded API route rather than a bare public page

Write access options:
1. Set `VIEWER_KEY` for shared internal viewing
2. Set `EDITOR_KEY` for product-team edits
3. Later replace the shared viewer key with SSO or an identity-aware proxy

This is still weaker than SSO. It is a pragmatic internal boundary, not a final identity model.

## Run Locally

Start the Vercel-shaped local runtime:
```bash
cd /Users/joy/autoresearch
vercel dev --listen 8141
```

Local access depends on `.env.local`:
- `VIEWER_KEY` for the access page
- optional `EDITOR_KEY` for local shared editing

Open:
- `http://127.0.0.1:8141/access`

## Deployment Guidance

Current live deployment path:
- Vercel project `autoresearch`
- guarded dashboard route via `/dashboard`
- serverless APIs backed by private Blob storage
- preview/production viewing gated by `VIEWER_KEY`
- preview/production edits gated by `EDITOR_KEY`

Current limitation:
- the shared viewer key is still a shared secret, not identity-backed access
- anyone with the live URL and the viewer key can view
- the GitHub repository and any committed source artifacts are outside this gate

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
