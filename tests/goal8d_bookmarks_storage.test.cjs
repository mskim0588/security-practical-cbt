/* Run with: node --test tests/goal8d_bookmarks_storage.test.cjs */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const script = fs.readFileSync(path.join(__dirname, "../app/static/js/bookmarks.js"), "utf8");
const key = "goal8d.question_bookmarks.v1.guest";

async function harness(initial, scope = "guest") {
  const values = new Map(Object.entries(initial));
  const listeners = {};
  const attrs = {};
  const button = {
    dataset: { bookmarkId: "Q-SHORT-001" },
    hidden: true,
    classList: { toggle() {} },
    setAttribute(name, value) { attrs[name] = value; },
    closest(selector) { return selector === "[data-bookmark-id]" ? this : null; },
  };
  const document = {
    getElementById() { return null; },
    querySelector(selector) {
      return selector === "script[data-bookmark-scope]" ? { dataset: { bookmarkScope: scope } } : button;
    },
    querySelectorAll(selector) { return selector === "[data-bookmark-id]" ? [button] : []; },
    addEventListener(name, handler) { listeners[name] = handler; },
  };
  const catalog = [{ id: "Q-SHORT-001", type: "short", url: "/topics/TOP-1#question-Q-SHORT-001" }];
  vm.runInNewContext(script, {
    document,
    window: { addEventListener(name, handler) { listeners[name] = handler; } },
    localStorage: {
      getItem(name) { return values.has(name) ? values.get(name) : null; },
      setItem(name, value) { values.set(name, value); },
    },
    fetch: async () => ({ ok: true, json: async () => catalog }),
  });
  await new Promise(resolve => setImmediate(resolve));
  return { values, listeners, button, attrs };
}

test("invalid and duplicate IDs are cleaned; add/remove persist IDs only", async () => {
  const state = await harness({
    [key]: JSON.stringify(["Q-SHORT-001", "Q-SHORT-001", "BOGUS"]),
    wrongNotes: "keep wrong notes",
    reviewFlags: "keep review flags",
    "goal8d.question_bookmarks.v1.owner": '["Q-SHORT-001"]',
  });
  assert.equal(state.values.get(key), '["Q-SHORT-001"]');
  assert.equal(state.attrs["aria-pressed"], "true");
  state.listeners.click({ target: state.button });
  assert.equal(state.values.get(key), "[]");
  state.listeners.click({ target: state.button });
  assert.equal(state.values.get(key), '["Q-SHORT-001"]');
  assert.equal(state.values.get("wrongNotes"), "keep wrong notes");
  assert.equal(state.values.get("reviewFlags"), "keep review flags");
  assert.equal(state.values.get("goal8d.question_bookmarks.v1.owner"), '["Q-SHORT-001"]');
  state.listeners.click({ target: { closest: () => ({ dataset: { bookmarkId: "BOGUS" } }) } });
  assert.equal(state.values.get(key), '["Q-SHORT-001"]');
});

test("malformed saved state is reset without crashing", async () => {
  const state = await harness({ [key]: "{broken" });
  assert.equal(state.values.get(key), "[]");
  assert.equal(state.attrs["aria-pressed"], "false");
});

test("owner bookmark key remains separate from guest bookmark key", async () => {
  const ownerKey = "goal8d.question_bookmarks.v1.owner";
  const state = await harness({ [key]: "[]", [ownerKey]: "[]" }, "owner");
  state.listeners.click({ target: state.button });
  assert.equal(state.values.get(ownerKey), '["Q-SHORT-001"]');
  assert.equal(state.values.get(key), "[]");
});
