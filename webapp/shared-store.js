const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const { Readable } = require('node:stream');
const {
  defaultStateEnvelope,
  normalizeEnvelope,
} = require('./shared-model');

let blobSdk = null;
try {
  blobSdk = require('@vercel/blob');
} catch {
  blobSdk = null;
}

const ROOT = path.resolve(__dirname, '..');
const STATE_PATH = path.join(ROOT, 'data', 'live_dashboard_state.json');
const AUDIT_PATH = path.join(ROOT, 'data', 'dashboard_audit_log.jsonl');
const STATE_BLOB_PATH = 'command-center/live_dashboard_state.json';
const AUDIT_BLOB_PATH = 'command-center/dashboard_audit_log.json';
const MAX_AUDIT_ENTRIES = 250;

function nowIso() {
  return new Date().toISOString();
}

function useBlobStore() {
  return Boolean(process.env.BLOB_READ_WRITE_TOKEN && blobSdk);
}

function ensureLocalFiles() {
  if (!fs.existsSync(STATE_PATH)) {
    fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
    fs.writeFileSync(STATE_PATH, JSON.stringify(defaultStateEnvelope(), null, 2), 'utf8');
  }
  if (!fs.existsSync(AUDIT_PATH)) {
    fs.mkdirSync(path.dirname(AUDIT_PATH), { recursive: true });
    fs.writeFileSync(AUDIT_PATH, '', 'utf8');
  }
}

async function streamToString(stream) {
  if (!stream) return '';
  if (typeof stream.getReader === 'function') {
    const reader = stream.getReader();
    const chunks = [];
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      chunks.push(Buffer.from(value));
    }
    return Buffer.concat(chunks).toString('utf8');
  }
  return new Promise((resolve, reject) => {
    const chunks = [];
    Readable.from(stream)
      .on('data', (chunk) => chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk)))
      .on('end', () => resolve(Buffer.concat(chunks).toString('utf8')))
      .on('error', reject);
  });
}

async function readBlobJson(pathname, fallbackValue) {
  if (!useBlobStore()) return fallbackValue;
  const { get } = blobSdk;
  const result = await get(pathname, { access: 'private' });
  if (!result || result.statusCode !== 200 || !result.stream) return fallbackValue;
  const raw = await streamToString(result.stream);
  if (!raw) return fallbackValue;
  return JSON.parse(raw);
}

async function writeBlobJson(pathname, payload) {
  const { put } = blobSdk;
  await put(pathname, JSON.stringify(payload, null, 2), {
    access: 'private',
    addRandomSuffix: false,
    allowOverwrite: true,
    contentType: 'application/json',
    cacheControlMaxAge: 60,
  });
}

async function readStateEnvelope() {
  if (useBlobStore()) {
    try {
      const raw = await readBlobJson(STATE_BLOB_PATH, defaultStateEnvelope());
      return normalizeEnvelope(raw);
    } catch {
      return defaultStateEnvelope();
    }
  }
  ensureLocalFiles();
  try {
    const raw = await fsp.readFile(STATE_PATH, 'utf8');
    return normalizeEnvelope(JSON.parse(raw));
  } catch {
    return defaultStateEnvelope();
  }
}

async function writeStateEnvelope(envelope) {
  const next = normalizeEnvelope(envelope);
  if (useBlobStore()) {
    await writeBlobJson(STATE_BLOB_PATH, next);
    return;
  }
  ensureLocalFiles();
  const tmpPath = `${STATE_PATH}.tmp`;
  await fsp.writeFile(tmpPath, JSON.stringify(next, null, 2), 'utf8');
  await fsp.rename(tmpPath, STATE_PATH);
}

async function readAuditEntries(limit = 50) {
  const safeLimit = Math.max(1, Math.min(200, Number(limit || 50)));
  if (useBlobStore()) {
    try {
      const raw = await readBlobJson(AUDIT_BLOB_PATH, []);
      return Array.isArray(raw) ? raw.slice(0, safeLimit) : [];
    } catch {
      return [];
    }
  }
  ensureLocalFiles();
  const lines = (await fsp.readFile(AUDIT_PATH, 'utf8')).split('\n').filter(Boolean).slice(-safeLimit);
  return lines.map((line) => JSON.parse(line)).reverse();
}

async function appendAuditEvent(event) {
  const nextEvent = {
    at: event.at || nowIso(),
    actor: event.actor || 'product-team',
    note: event.note || '',
    reason: event.reason || null,
    version: Number(event.version || 1),
    shared_keys: Array.isArray(event.shared_keys) ? event.shared_keys : [],
  };
  if (useBlobStore()) {
    const current = await readAuditEntries(MAX_AUDIT_ENTRIES);
    current.unshift(nextEvent);
    await writeBlobJson(AUDIT_BLOB_PATH, current.slice(0, MAX_AUDIT_ENTRIES));
    return;
  }
  ensureLocalFiles();
  await fsp.appendFile(AUDIT_PATH, `${JSON.stringify(nextEvent)}\n`, 'utf8');
}

module.exports = {
  nowIso,
  useBlobStore,
  readStateEnvelope,
  writeStateEnvelope,
  readAuditEntries,
  appendAuditEvent,
};
