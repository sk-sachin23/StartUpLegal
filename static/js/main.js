document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button');
    const spinner = form.querySelector('.spinner-border');

    // disable & show spinner
    btn.disabled = true;
    spinner.classList.remove('d-none');
  });
});

// select all checkboxes for scraping
const selectAll = document.getElementById('select-all');
if (selectAll) {
  selectAll.addEventListener('change', () => {
    const checked = selectAll.checked;
    document.querySelectorAll('.body-checkbox').forEach(cb => {
      cb.checked = checked;
    });
  });
}
