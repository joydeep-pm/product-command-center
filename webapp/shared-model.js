const SHARED_KEYS = [
  'epicStatus',
  'epicNotes',
  'strStatus',
  'hireStatus',
  'decStatus',
  'galStatus',
  'customEpics',
];

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

function defaultStateEnvelope() {
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

function normalizeEnvelope(raw) {
  const parsed = raw && typeof raw === 'object' ? raw : {};
  return {
    state: sanitizeSharedState(parsed.state),
    meta: {
      updated_at: parsed.meta?.updated_at || null,
      updated_by: parsed.meta?.updated_by || null,
      updated_reason: parsed.meta?.updated_reason || null,
      version: Number(parsed.meta?.version || 1),
    },
  };
}

module.exports = {
  SHARED_KEYS,
  defaultSharedState,
  defaultStateEnvelope,
  sanitizeSharedState,
  normalizeEnvelope,
};
