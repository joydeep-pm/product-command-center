const fs = require('node:fs/promises');
const path = require('node:path');
const { viewerAuthorized } = require('../webapp/access-node');

const DATA_PATH = path.join(process.cwd(), 'data', 'command_center_data.json');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify({ error: 'method_not_allowed' }, null, 2));
    return;
  }
  if (!viewerAuthorized(req)) {
    res.statusCode = 401;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.end(JSON.stringify({ error: 'viewer_access_required' }, null, 2));
    return;
  }
  const body = await fs.readFile(DATA_PATH, 'utf8');
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(body);
};
