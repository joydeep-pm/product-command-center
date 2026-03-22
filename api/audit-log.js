const { readAuditEntries } = require('../webapp/shared-store');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify({ error: 'method_not_allowed' }, null, 2));
    return;
  }
  const limit = Math.max(1, Math.min(200, Number(req.query?.limit || 50)));
  const entries = await readAuditEntries(limit);
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify({ entries }, null, 2));
};
