const fs = require('node:fs/promises');
const path = require('node:path');

const DASHBOARD_PATH = path.join(process.cwd(), 'app', 'dashboard.html');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify({ error: 'method_not_allowed' }, null, 2));
    return;
  }
  const html = await fs.readFile(DASHBOARD_PATH, 'utf8');
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(html);
};
