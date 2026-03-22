const crypto = require('node:crypto');

const VIEW_COOKIE = 'command_center_view';
const VIEWER_SESSION_SALT = 'product-command-center-view-v1';
const VIEWER_COOKIE_MAX_AGE = 60 * 60 * 12;

function viewerKey() {
  return String(process.env.VIEWER_KEY || '').trim();
}

function editorKey() {
  return String(process.env.EDITOR_KEY || '').trim();
}

function protectionEnabled() {
  return Boolean(viewerKey());
}

function viewerToken() {
  if (!protectionEnabled()) return '';
  return crypto
    .createHash('sha256')
    .update(`${viewerKey()}|${VIEWER_SESSION_SALT}`)
    .digest('hex');
}

function parseCookies(req) {
  const raw = req?.headers?.cookie || '';
  return raw.split(';').reduce((acc, pair) => {
    const [name, ...rest] = pair.trim().split('=');
    if (!name) return acc;
    acc[name] = decodeURIComponent(rest.join('=') || '');
    return acc;
  }, {});
}

function viewerAuthorized(req) {
  if (!protectionEnabled()) return true;
  const cookies = parseCookies(req);
  const token = viewerToken();
  return (
    cookies[VIEW_COOKIE] === token
    || req.headers['x-viewer-key'] === viewerKey()
    || (editorKey() && req.headers['x-editor-key'] === editorKey())
  );
}

function cookieIsSecure(req) {
  const forwardedProto = String(req?.headers?.['x-forwarded-proto'] || '').trim();
  const host = String(req?.headers?.host || '').trim();
  return forwardedProto === 'https' || (!/^(localhost|127\.0\.0\.1)(:\d+)?$/i.test(host) && Boolean(host));
}

function buildCookieHeader(req, value, maxAge) {
  const parts = [
    `${VIEW_COOKIE}=${value}`,
    'Path=/',
    `Max-Age=${maxAge}`,
    'HttpOnly',
    'SameSite=Lax',
  ];
  if (cookieIsSecure(req)) parts.push('Secure');
  return parts.join('; ');
}

function viewerCookieHeader(req) {
  return buildCookieHeader(req, viewerToken(), VIEWER_COOKIE_MAX_AGE);
}

function clearViewerCookieHeader(req) {
  return buildCookieHeader(req, '', 0);
}

module.exports = {
  VIEW_COOKIE,
  VIEWER_COOKIE_MAX_AGE,
  protectionEnabled,
  viewerKey,
  viewerToken,
  viewerAuthorized,
  viewerCookieHeader,
  clearViewerCookieHeader,
};
