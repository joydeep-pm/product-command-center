const EDITOR_KEY = process.env.EDITOR_KEY || '';
const ALLOW_OPEN_EDIT = process.env.ALLOW_OPEN_EDIT === '1';
const { viewerAuthorized } = require('../webapp/access-node');

function editorAuthorized(req) {
  if (ALLOW_OPEN_EDIT) return true;
  if (!EDITOR_KEY) return false;
  return req.headers['x-editor-key'] === EDITOR_KEY;
}

module.exports = async (req, res) => {
  if (!viewerAuthorized(req) && !editorAuthorized(req)) {
    res.statusCode = 401;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.end(JSON.stringify({ error: 'viewer_access_required' }, null, 2));
    return;
  }
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify({
    can_edit: editorAuthorized(req),
    requires_editor_key: !ALLOW_OPEN_EDIT,
  }, null, 2));
};
