#!/usr/bin/env node

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { URL } = require('node:url');

const ROOT = path.resolve(__dirname, '..');
const HOST = process.env.HOST || '0.0.0.0';
const PORT = Number(process.env.PORT || 8123);
const EDITOR_KEY = process.env.EDITOR_KEY || '';
const ALLOW_OPEN_EDIT = process.env.ALLOW_OPEN_EDIT === '1';
const STATE_PATH = path.join(ROOT, 'data', 'live_dashboard_state.json');
const AUDIT_PATH = path.join(ROOT, 'data', 'dashboard_audit_log.jsonl');
const DASHBOARD_PATH = path.join(ROOT, 'app', 'dashboard.html');

const SHARED_KEYS = [
  'epicStatus',
  'epicNotes',
  'strStatus',
  'hireStatus',
  'decStatus',
  'galStatus',
  'customEpics',
];

function ensureFile(filePath, initialContent) {
  if (!fs.existsSync(filePath)) {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, initialContent, 'utf8');
  }
}

function nowIso() {
  return new Date().toISOString();
}

function defaultSharedState() {
  return {
    epicStatus: {},
    epicNotes: {},
    strStatus: {},
    hireStatus: {},
    decStatus: ['Not Started', 'Not Started', 'Not Started', 'Not Started', 'Not Started'],
    galStatus: {},
    customEpics: [],
  };
}

function sanitizeSharedState(input) {
  const base = defaultSharedState();
  if (!input || typeof input !== 'object') return base;
  SHARED_KEYS.forEach((key) => {
    if (input[key] === undefined) return;
    if (Array.isArray(base[key])) {
      base[key] = Array.isArray(input[key]) ? input[key] : base[key];
      return;
    }
    if (typeof base[key] === 'object') {
      base[key] = input[key] && typeof input[key] === 'object' && !Array.isArray(input[key]) ? input[key] : base[key];
    }
  });
  return base;
}

function readStateEnvelope() {
  ensureFile(
    STATE_PATH,
    JSON.stringify(
      {
        state: defaultSharedState(),
        meta: {
          updated_at: null,
          updated_by: null,
          updated_reason: null,
          version: 1,
        },
      },
      null,
      2,
    ),
  );
  try {
    const raw = fs.readFileSync(STATE_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    return {
      state: sanitizeSharedState(parsed.state),
      meta: {
        updated_at: parsed.meta?.updated_at || null,
        updated_by: parsed.meta?.updated_by || null,
        updated_reason: parsed.meta?.updated_reason || null,
        version: Number(parsed.meta?.version || 1),
      },
    };
  } catch {
    return {
      state: defaultSharedState(),
      meta: {
        updated_at: null,
        updated_by: null,
        updated_reason: null,
        version: 1,
      },
    };
  }
}

function writeStateEnvelope(envelope) {
  const tmpPath = `${STATE_PATH}.tmp`;
  fs.writeFileSync(tmpPath, JSON.stringify(envelope, null, 2), 'utf8');
  fs.renameSync(tmpPath, STATE_PATH);
}

function appendAuditEvent(event) {
  ensureFile(AUDIT_PATH, '');
  fs.appendFileSync(AUDIT_PATH, `${JSON.stringify(event)}\n`, 'utf8');
}

function editorAuthorized(req) {
  if (ALLOW_OPEN_EDIT) return true;
  if (!EDITOR_KEY) return false;
  return req.headers['x-editor-key'] === EDITOR_KEY;
}

function contentType(filePath) {
  if (filePath.endsWith('.html')) return 'text/html; charset=utf-8';
  if (filePath.endsWith('.json')) return 'application/json; charset=utf-8';
  if (filePath.endsWith('.js')) return 'application/javascript; charset=utf-8';
  if (filePath.endsWith('.css')) return 'text/css; charset=utf-8';
  if (filePath.endsWith('.md')) return 'text/markdown; charset=utf-8';
  if (filePath.endsWith('.svg')) return 'image/svg+xml';
  if (filePath.endsWith('.png')) return 'image/png';
  return 'application/octet-stream';
}

function sendJson(res, code, payload) {
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
  });
  res.end(JSON.stringify(payload, null, 2));
}

function sendText(res, code, text, type = 'text/plain; charset=utf-8') {
  res.writeHead(code, {
    'Content-Type': type,
    'Cache-Control': 'no-store',
  });
  res.end(text);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 5_000_000) {
        reject(new Error('request_too_large'));
        req.destroy();
      }
    });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

function serveFile(res, filePath) {
  if (!fs.existsSync(filePath)) {
    sendText(res, 404, 'Not found');
    return;
  }
  res.writeHead(200, {
    'Content-Type': contentType(filePath),
    'Cache-Control': 'no-store',
  });
  fs.createReadStream(filePath).pipe(res);
}

async function handleApi(req, res, url) {
  if (url.pathname === '/health') {
    sendJson(res, 200, { status: 'ok', time: nowIso() });
    return true;
  }

  if (url.pathname === '/api/dashboard-state' && req.method === 'GET') {
    const envelope = readStateEnvelope();
    sendJson(res, 200, {
      mode: 'shared',
      can_edit: editorAuthorized(req),
      requires_editor_key: !ALLOW_OPEN_EDIT,
      state: envelope.state,
      meta: envelope.meta,
    });
    return true;
  }

  if (url.pathname === '/api/dashboard-state' && req.method === 'POST') {
    if (!editorAuthorized(req)) {
      sendJson(res, 403, {
        error: 'editor_key_required',
        message: 'Write access requires the configured editor key.',
      });
      return true;
    }
    try {
      const body = JSON.parse(await readBody(req) || '{}');
      const actor = String(body.actor || 'product-team').trim() || 'product-team';
      const note = String(body.note || '').trim();
      const reason = String(body.reason || '').trim();
      const nextState = sanitizeSharedState(body.state);
      const previous = readStateEnvelope();
      const envelope = {
        state: nextState,
        meta: {
          updated_at: nowIso(),
          updated_by: actor,
          updated_reason: reason || null,
          version: previous.meta.version + 1,
        },
      };
      writeStateEnvelope(envelope);
      appendAuditEvent({
        at: envelope.meta.updated_at,
        actor,
        note,
        reason: reason || null,
        version: envelope.meta.version,
        shared_keys: SHARED_KEYS,
      });
      sendJson(res, 200, {
        ok: true,
        state: envelope.state,
        meta: envelope.meta,
      });
    } catch (error) {
      sendJson(res, 400, {
        error: 'invalid_request',
        message: error.message,
      });
    }
    return true;
  }

  if (url.pathname === '/api/audit-log' && req.method === 'GET') {
    ensureFile(AUDIT_PATH, '');
    const limit = Math.max(1, Math.min(200, Number(url.searchParams.get('limit') || 50)));
    const lines = fs.readFileSync(AUDIT_PATH, 'utf8').split('\n').filter(Boolean).slice(-limit);
    sendJson(res, 200, {
      entries: lines.map((line) => JSON.parse(line)).reverse(),
    });
    return true;
  }

  if (url.pathname === '/api/editor-check' && req.method === 'GET') {
    sendJson(res, 200, {
      can_edit: editorAuthorized(req),
      requires_editor_key: !ALLOW_OPEN_EDIT,
    });
    return true;
  }

  return false;
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    if (await handleApi(req, res, url)) return;

    if (url.pathname === '/' || url.pathname === '/dashboard') {
      serveFile(res, DASHBOARD_PATH);
      return;
    }

    const relativePath = path.normalize(url.pathname.replace(/^\/+/, ''));
    const resolved = path.resolve(ROOT, relativePath);
    if (!resolved.startsWith(ROOT)) {
      sendText(res, 403, 'Forbidden');
      return;
    }
    serveFile(res, resolved);
  } catch (error) {
    sendJson(res, 500, {
      error: 'server_error',
      message: error.message,
    });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`Shared command center listening on http://${HOST}:${PORT}`);
  console.log(`Dashboard: http://127.0.0.1:${PORT}/dashboard`);
  console.log(`Writes: ${ALLOW_OPEN_EDIT ? 'open (ALLOW_OPEN_EDIT=1)' : EDITOR_KEY ? 'editor key required' : 'disabled until EDITOR_KEY is set'}`);
});
