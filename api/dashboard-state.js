const { SHARED_KEYS, sanitizeSharedState } = require('../webapp/shared-model');
const { nowIso, readStateEnvelope, writeStateEnvelope, appendAuditEvent } = require('../webapp/shared-store');

const EDITOR_KEY = process.env.EDITOR_KEY || '';
const ALLOW_OPEN_EDIT = process.env.ALLOW_OPEN_EDIT === '1';

function editorAuthorized(req) {
  if (ALLOW_OPEN_EDIT) return true;
  if (!EDITOR_KEY) return false;
  return req.headers['x-editor-key'] === EDITOR_KEY;
}

function send(res, code, payload) {
  res.status(code).setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(payload, null, 2));
}

module.exports = async (req, res) => {
  if (req.method === 'GET') {
    const envelope = await readStateEnvelope();
    send(res, 200, {
      mode: 'shared',
      can_edit: editorAuthorized(req),
      requires_editor_key: !ALLOW_OPEN_EDIT,
      state: envelope.state,
      meta: envelope.meta,
      storage_mode: process.env.BLOB_READ_WRITE_TOKEN ? 'vercel-blob' : 'local-file',
    });
    return;
  }

  if (req.method !== 'POST') {
    send(res, 405, { error: 'method_not_allowed' });
    return;
  }

  if (!editorAuthorized(req)) {
    send(res, 403, {
      error: 'editor_key_required',
      message: 'Write access requires the configured editor key.',
    });
    return;
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const actor = String(body.actor || 'product-team').trim() || 'product-team';
    const note = String(body.note || '').trim();
    const reason = String(body.reason || '').trim();
    const previous = await readStateEnvelope();
    const envelope = {
      state: sanitizeSharedState(body.state),
      meta: {
        updated_at: nowIso(),
        updated_by: actor,
        updated_reason: reason || null,
        version: previous.meta.version + 1,
      },
    };
    await writeStateEnvelope(envelope);
    await appendAuditEvent({
      at: envelope.meta.updated_at,
      actor,
      note,
      reason: reason || null,
      version: envelope.meta.version,
      shared_keys: SHARED_KEYS,
    });
    send(res, 200, {
      ok: true,
      state: envelope.state,
      meta: envelope.meta,
    });
  } catch (error) {
    send(res, 400, {
      error: 'invalid_request',
      message: error.message,
    });
  }
};
