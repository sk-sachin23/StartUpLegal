document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button');
    const spinner = form.querySelector('.spinner-border');

    // disable & show spinner
    btn.disabled = true;
    spinner.classList.remove('d-none');
  });
});
