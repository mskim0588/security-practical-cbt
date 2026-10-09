(() => {
  const menus = [...document.querySelectorAll('.nav-menu')];
  if (!menus.length) return;

  const close = (menu, restoreFocus = false) => {
    if (!menu.open) return;
    menu.open = false;
    if (restoreFocus) menu.querySelector('summary').focus();
  };

  menus.forEach((menu) => {
    const summary = menu.querySelector('summary');
    summary.setAttribute('aria-expanded', String(menu.open));
    menu.addEventListener('toggle', () => {
      summary.setAttribute('aria-expanded', String(menu.open));
      if (menu.open) menus.forEach((other) => { if (other !== menu) close(other); });
    });
    menu.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        close(menu, true);
      }
    });
  });

  document.addEventListener('pointerdown', (event) => {
    menus.forEach((menu) => { if (!menu.contains(event.target)) close(menu); });
  });
})();
