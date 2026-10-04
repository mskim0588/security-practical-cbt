/**
 * Information Security CBT Exam Controller
 * Goal 4B: Exam Navigation, Progress Tracking, Practical Selection, ScrollSpy,
 * Mobile Bottom Action Bar & Accessible Question Sheet
 */
document.addEventListener("DOMContentLoaded", function () {
  const practicalRadios = document.querySelectorAll('input[name="selected_practical_id"]');
  const practicalCards = document.querySelectorAll('.practical-card');
  const allCards = document.querySelectorAll('.question-card');

  // --------------------------------------------------------------------------
  // 1. Practical Question Selection & State Management
  // --------------------------------------------------------------------------
  function getSelectedPracticalId() {
    const checked = document.querySelector('input[name="selected_practical_id"]:checked');
    return checked ? checked.value : null;
  }

  function updatePracticalSelection(selectedId) {
    practicalCards.forEach(card => {
      const qId = card.getAttribute('data-qid');
      const isSelected = (qId === selectedId);
      const pill = document.getElementById(`prac-pill-${qId}`);

      if (isSelected) {
        card.classList.add('is-selected');
        card.classList.remove('is-unselected');
        if (pill) {
          pill.textContent = '선택 문항 · 16점 채점';
          pill.className = 'practical-status-pill selected';
        }
      } else {
        card.classList.add('is-unselected');
        card.classList.remove('is-selected');
        if (pill) {
          pill.textContent = '미선택 · 채점 제외';
          pill.className = 'practical-status-pill unselected';
        }
      }
    });

    // Re-evaluate all questions & update overall progress
    updateAllProgress();
  }

  practicalRadios.forEach(radio => {
    radio.addEventListener('change', function () {
      if (this.checked) {
        updatePracticalSelection(this.value);
      }
    });
  });

  // --------------------------------------------------------------------------
  // 2. Real-time Status Evaluation & Navigation Sync
  // --------------------------------------------------------------------------
  function evaluateCard(card) {
    const qId = card.getAttribute('data-qid');
    const qType = card.getAttribute('data-qtype');
    const isPractical = (qType === 'practical');
    const selectedPracId = getSelectedPracticalId();
    const isSelectedPrac = (isPractical && qId === selectedPracId);

    // If unselected practical, status is 'unselected'
    if (isPractical && !isSelectedPrac) {
      applyCardStatus(qId, 'unselected', '- 채점 제외', '-');
      return { status: 'unselected', isRequired: false };
    }

    const inputs = card.querySelectorAll('input[type="text"], textarea');
    let totalInputs = inputs.length;
    let filledInputs = 0;

    inputs.forEach(input => {
      if (input.value.trim().length > 0) {
        filledInputs++;
      }
    });

    let status = 'empty';
    let label = '○ 미작성';
    let icon = '○';

    if (filledInputs === totalInputs && totalInputs > 0) {
      status = 'complete';
      label = '✓ 작성 완료';
      icon = '✓';
    } else if (filledInputs > 0) {
      status = 'partial';
      label = `△ 일부 작성 (${filledInputs}/${totalInputs})`;
      icon = '△';
    }

    applyCardStatus(qId, status, label, icon);
    return { status, isRequired: true };
  }

  function applyCardStatus(qId, status, labelText, iconSymbol) {
    // 1. Status badge on the card header
    const badge = document.getElementById(`status-badge-${qId}`);
    if (badge) {
      badge.className = `q-status-badge badge-${status}`;
      badge.textContent = labelText;
    }

    // 2. Desktop Navigator button
    const navBtn = document.getElementById(`nav-btn-${qId}`);
    const navIcon = document.getElementById(`nav-icon-${qId}`);
    if (navBtn) {
      navBtn.classList.remove('completed', 'partial', 'unselected');
      if (status === 'complete') navBtn.classList.add('completed');
      else if (status === 'partial') navBtn.classList.add('partial');
      else if (status === 'unselected') navBtn.classList.add('unselected');
    }
    if (navIcon) {
      navIcon.textContent = iconSymbol;
    }

    // 3. Mobile Sheet button
    const sheetBtn = document.getElementById(`sheet-btn-${qId}`);
    const sheetIcon = document.getElementById(`sheet-icon-${qId}`);
    if (sheetBtn) {
      sheetBtn.classList.remove('completed', 'partial', 'unselected');
      if (status === 'complete') sheetBtn.classList.add('completed');
      else if (status === 'partial') sheetBtn.classList.add('partial');
      else if (status === 'unselected') sheetBtn.classList.add('unselected');
    }
    if (sheetIcon) {
      sheetIcon.textContent = iconSymbol;
    }
  }

  function updateAllProgress() {
    let completedCount = 0;
    let partialCount = 0;
    let emptyCount = 0;

    allCards.forEach(card => {
      const res = evaluateCard(card);
      if (res.isRequired) {
        if (res.status === 'complete') completedCount++;
        else if (res.status === 'partial') partialCount++;
        else emptyCount++;
      }
    });

    const totalRequired = 17; // 12 short + 4 desc + 1 selected practical
    const percent = Math.min(100, Math.round((completedCount / totalRequired) * 100));

    // Update Desktop Navigator
    const desktopProgressText = document.getElementById('desktop-progress-text');
    const desktopProgressFill = document.getElementById('desktop-progress-fill');
    if (desktopProgressText) {
      desktopProgressText.innerHTML = `<strong>${completedCount}</strong> / ${totalRequired} 완료`;
    }
    if (desktopProgressFill) {
      desktopProgressFill.style.width = `${percent}%`;
    }

    // Update Mobile Action Bar
    const mobileCount = document.getElementById('mobile-progress-count');
    const mobileUnanswered = document.getElementById('mobile-unanswered-count');
    if (mobileCount) {
      mobileCount.textContent = completedCount;
    }
    if (mobileUnanswered) {
      mobileUnanswered.textContent = (totalRequired - completedCount);
    }

    // Update Mobile Sheet Summary
    const sheetComplete = document.getElementById('sheet-summary-complete');
    const sheetPartial = document.getElementById('sheet-summary-partial');
    const sheetEmpty = document.getElementById('sheet-summary-empty');
    if (sheetComplete) sheetComplete.textContent = completedCount;
    if (sheetPartial) sheetPartial.textContent = partialCount;
    if (sheetEmpty) sheetEmpty.textContent = emptyCount;
  }

  // Bind input listeners to all text inputs and textareas
  allCards.forEach(card => {
    const inputs = card.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(input => {
      input.addEventListener('input', () => {
        evaluateCard(card);
        updateAllProgress();
      });
    });
  });

  // Initial evaluation
  updatePracticalSelection(getSelectedPracticalId());

  // --------------------------------------------------------------------------
  // 3. ScrollSpy (IntersectionObserver)
  // --------------------------------------------------------------------------
  if ('IntersectionObserver' in window) {
    try {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const qId = entry.target.getAttribute('data-qid');
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('is-active-view'));
            const currentNav = document.getElementById(`nav-btn-${qId}`);
            if (currentNav) {
              currentNav.classList.add('is-active-view');
            }
          }
        });
      }, {
        rootMargin: '-10% 0px -70% 0px',
        threshold: 0
      });

      allCards.forEach(card => observer.observe(card));
    } catch (e) {
      console.warn("IntersectionObserver initialization skipped:", e);
    }
  }

  // --------------------------------------------------------------------------
  // 4. Smooth Scroll to Target Question
  // --------------------------------------------------------------------------
  function scrollToQuestion(targetId) {
    const targetCard = document.getElementById(`q-${targetId}`);
    if (targetCard) {
      targetCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Brief visual flash/highlight for clarity
      targetCard.style.transition = 'box-shadow 0.3s ease';
      const origShadow = targetCard.style.boxShadow;
      targetCard.style.boxShadow = '0 0 0 3px rgba(37, 99, 235, 0.35)';
      setTimeout(() => {
        targetCard.style.boxShadow = origShadow;
      }, 1000);
    }
  }

  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('data-target');
      scrollToQuestion(targetId);
    });
  });

  // --------------------------------------------------------------------------
  // 5. Mobile Question Sheet (Drawer) Controller & Accessibility
  // --------------------------------------------------------------------------
  const sheet = document.getElementById('mobile-question-sheet');
  const btnOpenSheet = document.getElementById('btn-mobile-sheet-open');
  const btnCloseSheet = document.getElementById('btn-mobile-sheet-close');
  const sheetBackdrop = document.getElementById('sheet-backdrop');

  function openSheet() {
    if (!sheet) return;
    sheet.classList.add('is-open');
    sheet.setAttribute('aria-hidden', 'false');
    if (btnOpenSheet) btnOpenSheet.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    if (btnCloseSheet) btnCloseSheet.focus();
  }

  function closeSheet() {
    if (!sheet) return;
    sheet.classList.remove('is-open');
    sheet.setAttribute('aria-hidden', 'true');
    if (btnOpenSheet) {
      btnOpenSheet.setAttribute('aria-expanded', 'false');
      btnOpenSheet.focus();
    }
    document.body.style.overflow = '';
  }

  if (btnOpenSheet) btnOpenSheet.addEventListener('click', openSheet);
  if (btnCloseSheet) btnCloseSheet.addEventListener('click', closeSheet);
  if (sheetBackdrop) sheetBackdrop.addEventListener('click', closeSheet);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sheet && sheet.classList.contains('is-open')) {
      closeSheet();
    }
  });

  document.querySelectorAll('.sheet-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const targetId = this.getAttribute('data-target');
      closeSheet();
      setTimeout(() => {
        scrollToQuestion(targetId);
      }, 150);
    });
  });

  // --------------------------------------------------------------------------
  // 6. Progressive Code / Log Block Enhancer
  // --------------------------------------------------------------------------
  function enhanceQuestionCodeBlocks() {
    const qTexts = document.querySelectorAll('.question-text');
    qTexts.forEach(el => {
      const raw = el.innerHTML;
      // Convert bracketed log/config/script sections into clean .code-terminal blocks
      const enhanced = raw.replace(
        /(\[(?:IPTables|Snort|HTTP|DHCP|access\.log|아파치|로그|규칙|스크립트|설정|Rule|Request|백업).*?\])\n([\s\S]*?)(?=\n\d+\)|\n\[|\n$|$)/gi,
        function (match, header, code) {
          const trimmedCode = code.trim();
          if (trimmedCode.length > 0) {
            return `\n<div class="code-terminal"><strong style="color: #93c5fd; display: block; margin-bottom: 4px;">${header}</strong>${trimmedCode}</div>\n`;
          }
          return match;
        }
      );
      if (enhanced !== raw) {
        el.innerHTML = enhanced;
      }
    });
  }

  enhanceQuestionCodeBlocks();
});
