document.addEventListener("DOMContentLoaded", function () {
  // 실무형 택1 라디오 버튼 처리
  const practicalRadios = document.querySelectorAll('input[name="selected_practical_id"]');
  const practicalCards = document.querySelectorAll('.practical-card');

  function updatePracticalSelection(selectedId) {
    practicalCards.forEach(card => {
      const qId = card.getAttribute('data-qid');
      const isSelected = (qId === selectedId);
      const textareas = card.querySelectorAll('textarea');

      if (isSelected) {
        card.classList.remove('disabled-q');
        textareas.forEach(t => t.removeAttribute('disabled'));
      } else {
        card.classList.add('disabled-q');
        textareas.forEach(t => t.setAttribute('disabled', 'disabled'));
      }

      // 사이드바 버튼 상태 업데이트
      const navBtn = document.querySelector(`.nav-btn[data-target="${qId}"]`);
      if (navBtn) {
        if (isSelected) {
          navBtn.classList.remove('unselected');
        } else {
          navBtn.classList.add('unselected');
        }
      }
    });
  }

  practicalRadios.forEach(radio => {
    radio.addEventListener('change', function () {
      if (this.checked) {
        updatePracticalSelection(this.value);
      }
    });
  });

  // 초기 실무형 선택 상태 적용 (기본값: 첫 번째 실무형 선택)
  const checkedRadio = document.querySelector('input[name="selected_practical_id"]:checked');
  if (checkedRadio) {
    updatePracticalSelection(checkedRadio.value);
  }

  // 문항 작성 상태 감지 및 사이드바 버튼 색상 업데이트
  function checkQuestionCompletion(card) {
    const qId = card.getAttribute('data-qid');
    const navBtn = document.querySelector(`.nav-btn[data-target="${qId}"]`);
    if (!navBtn) return;

    const inputs = card.querySelectorAll('input[type="text"], textarea');
    let hasValue = false;
    inputs.forEach(input => {
      if (input.value.trim().length > 0) {
        hasValue = true;
      }
    });

    if (hasValue) {
      navBtn.classList.add('completed');
    } else {
      navBtn.classList.remove('completed');
    }
  }

  const allCards = document.querySelectorAll('.question-card');
  allCards.forEach(card => {
    const inputs = card.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(input => {
      input.addEventListener('input', () => checkQuestionCompletion(card));
    });
    checkQuestionCompletion(card);
  });
});
