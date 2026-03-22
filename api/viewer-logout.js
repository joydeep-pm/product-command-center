const { clearViewerCookieHeader } = require('../webapp/access-node');

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
  res.setHeader('Set-Cookie', clearViewerCookieHeader(req));
  send(res, 200, { ok: true });
};
