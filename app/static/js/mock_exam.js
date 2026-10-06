(function () {
  "use strict";

  const timer = document.getElementById("mock-timer");
  const expiryForm = document.getElementById("mock-expiry-form");
  if (!timer || !expiryForm) return;

  const expiryMs = Date.parse(timer.dataset.expiry || "");
  let expirySubmitted = false;

  function formatRemaining(totalSeconds) {
    const safe = Math.max(0, totalSeconds);
    const hours = Math.floor(safe / 3600);
    const minutes = Math.floor((safe % 3600) / 60);
    const seconds = safe % 60;
    return [hours, minutes, seconds].map(value => String(value).padStart(2, "0")).join(":");
  }

  function submitExpired() {
    if (expirySubmitted) return;
    expirySubmitted = true;
    document.querySelectorAll("button, input, textarea, select").forEach(control => {
      if (!expiryForm.contains(control)) control.disabled = true;
    });
    expiryForm.submit();
  }

  function refreshTimer() {
    if (!Number.isFinite(expiryMs)) return;
    const remaining = Math.max(0, Math.ceil((expiryMs - Date.now()) / 1000));
    timer.textContent = formatRemaining(remaining);
    timer.setAttribute("aria-label", `남은 시간 ${timer.textContent}`);
    timer.classList.toggle("is-warning", remaining <= 30 * 60 && remaining > 5 * 60);
    timer.classList.toggle("is-critical", remaining <= 5 * 60);
    if (remaining === 0) submitExpired();
  }

  refreshTimer();
  window.setInterval(refreshTimer, 1000);
  document.addEventListener("visibilitychange", refreshTimer);
  window.addEventListener("focus", refreshTimer);
  window.addEventListener("pageshow", refreshTimer);
})();
