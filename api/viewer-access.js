const {
  protectionEnabled,
  viewerKey,
  viewerCookieHeader,
} = require('../webapp/access-node');

function send(res, code, payload) {
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(payload, null, 2));
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    send(res, 405, { error: 'method_not_allowed' });
    return;
  }

  if (!protectionEnabled()) {
    send(res, 200, { ok: true, protection_enabled: false });
    return;
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const key = String(body.key || '').trim();
    const next = String(body.next || '/dashboard').trim() || '/dashboard';
    if (!key || key !== viewerKey()) {
      send(res, 403, {
        ok: false,
        error: 'viewer_key_invalid',
        message: 'Viewer access key rejected.',
      });
      return;
    }
    res.setHeader('Set-Cookie', viewerCookieHeader(req));
    send(res, 200, {
      ok: true,
      protection_enabled: true,
      next: next.startsWith('/') ? next : '/dashboard',
    });
  } catch (error) {
    send(res, 400, {
      ok: false,
      error: 'invalid_request',
      message: error.message,
    });
  }
};
