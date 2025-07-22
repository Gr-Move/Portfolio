document.addEventListener('DOMContentLoaded', () => {
  // Загружаем конфиг
  fetch('config.json')
    .then(response => response.json())
    .then(config => {

      // Загружаем компоненты согласно конфигу
      if (config.components.header) {
        fetch('components/header.html')
          .then(r => r.text())
          .then(html => {
            document.getElementById('header-placeholder').innerHTML = html;
          });
      }

      if (config.components.footer) {
        fetch('components/footer.html')
          .then(r => r.text())
          .then(html => {
            document.getElementById('footer-placeholder').innerHTML = html;
          });
      }

      if (config.components.button) {
        fetch('components/button.html')
          .then(r => r.text())
          .then(html => {
            document.getElementById('button-placeholder').innerHTML = html;
          });
      }

      // Аналогично для других компонентов
    });
});