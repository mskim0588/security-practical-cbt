/* Goal 8D: manual question bookmarks, stored as canonical IDs on this device. */
(() => {
  "use strict";

  const script = document.querySelector("script[data-bookmark-scope]");
  const scope = script && script.dataset.bookmarkScope === "owner" ? "owner" : "guest";
  const key = `goal8d.question_bookmarks.v1.${scope}`;
  const page = document.getElementById("bookmark-page");
  if (!page && !document.querySelector("[data-bookmark-id]")) return;

  const status = document.getElementById("bookmark-status");
  const list = document.getElementById("bookmark-list");
  const empty = document.getElementById("bookmark-empty");
  let catalog = [];
  let byId = new Map();
  let saved = [];
  let filter = "all";

  function message(text) {
    if (status) status.textContent = text;
  }

  function persist(ids) {
    try {
      localStorage.setItem(key, JSON.stringify(ids));
      return true;
    } catch (_error) {
      message("이 브라우저에서 저장할 수 없습니다. 저장소 설정을 확인해 주세요.");
      return false;
    }
  }

  function read() {
    let raw;
    try {
      raw = localStorage.getItem(key);
    } catch (_error) {
      message("이 브라우저의 저장된 문제에 접근할 수 없습니다.");
      return [];
    }
    if (raw === null) return [];
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (_error) {
      parsed = [];
    }
    const valid = Array.isArray(parsed) ? [...new Set(parsed.filter(id => typeof id === "string" && byId.has(id)))] : [];
    if (raw !== JSON.stringify(valid)) persist(valid);
    return valid;
  }

  function syncButtons() {
    const set = new Set(saved);
    document.querySelectorAll("[data-bookmark-id]").forEach(button => {
      const id = button.dataset.bookmarkId;
      if (!byId.has(id)) return;
      const active = set.has(id);
      button.hidden = false;
      button.classList.toggle("is-saved", active);
      button.setAttribute("aria-pressed", String(active));
      button.setAttribute("aria-label", id + (active ? " 다시 볼 문제에서 제거" : " 다시 볼 문제에 추가"));
      button.textContent = active ? "★ 저장됨 · 제거" : "☆ 다시 볼 문제에 추가";
    });
  }

  function element(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  }

  function renderPage() {
    if (!page) return;
    const set = new Set(saved);
    const visible = catalog.filter(item => set.has(item.id) && (filter === "all" || item.type === filter));
    list.replaceChildren();
    visible.forEach(item => {
      const card = element("article", "card bookmark-card");
      const meta = element("div", "bookmark-card-meta", `${item.id} · ${item.type_label} · ${item.category}`);
      const title = element("h2", "bookmark-card-title", `Parent Concept: ${item.concept}`);
      const topic = element("p", "bookmark-card-topic", `Topic: ${item.topic}`);
      const preview = element("p", "bookmark-card-preview", item.preview);
      const actions = element("div", "bookmark-card-actions");
      const open = element("a", "btn btn-primary", "문제 열기");
      open.href = item.url;
      const remove = element("button", "bookmark-toggle is-saved", "★ 저장됨 · 제거");
      remove.type = "button";
      remove.dataset.bookmarkId = item.id;
      remove.setAttribute("aria-pressed", "true");
      remove.setAttribute("aria-label", `${item.id} 다시 볼 문제에서 제거`);
      actions.append(open, remove);
      card.append(meta, title, topic, preview, actions);
      list.append(card);
    });
    empty.hidden = visible.length !== 0;
    empty.textContent = saved.length
      ? "선택한 유형의 저장한 문제가 없습니다. 다른 유형이나 전체를 선택해 주세요."
      : "아직 저장한 문제가 없습니다. 학습 화면에서 원하는 문제를 직접 저장해 다시 확인할 수 있습니다.";
    message(saved.length ? `저장한 문제 ${saved.length}개 · 현재 ${visible.length}개 표시` : "저장한 문제 0개");
    document.querySelectorAll("[data-bookmark-filter]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.bookmarkFilter === filter));
    });
  }

  document.addEventListener("click", event => {
    const filterButton = event.target.closest("[data-bookmark-filter]");
    if (filterButton && page) {
      filter = filterButton.dataset.bookmarkFilter;
      renderPage();
      return;
    }
    const button = event.target.closest("[data-bookmark-id]");
    if (!button || !byId.has(button.dataset.bookmarkId)) return;
    const id = button.dataset.bookmarkId;
    const next = saved.includes(id) ? saved.filter(item => item !== id) : [...saved, id];
    if (!persist(next)) return;
    saved = next;
    renderPage();
    syncButtons();
  });

  window.addEventListener("storage", event => {
    if (event.key !== key) return;
    saved = read();
    renderPage();
    syncButtons();
  });

  fetch("/bookmarks/catalog", { credentials: "same-origin", cache: "no-store" })
    .then(response => {
      if (!response.ok) throw new Error("catalog unavailable");
      return response.json();
    })
    .then(items => {
      if (!Array.isArray(items)) throw new Error("invalid catalog");
      catalog = items;
      byId = new Map(items.map(item => [item.id, item]));
      saved = read();
      renderPage();
      syncButtons();
    })
    .catch(() => message("저장한 문제 목록을 불러오지 못했습니다. 새로고침해 주세요."));
})();
