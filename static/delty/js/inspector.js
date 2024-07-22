// document.addEventListener('DOMContentLoaded', () => {
//   let overlay = document.createElement('div');
//   overlay.className = 'highlight-overlay';
//   document.body.appendChild(overlay);
//
//   document.body.addEventListener('mouseover', (e) => {
//     let target = e.target;
//
//     if (target !== document.body && target !== overlay) {
//       let rect = target.getBoundingClientRect();
//       overlay.style.width = `${rect.width}px`;
//       overlay.style.height = `${rect.height}px`;
//       overlay.style.top = `${window.scrollY + rect.top}px`;
//       overlay.style.left = `${window.scrollX + rect.left}px`;
//       overlay.style.display = 'block';
//     }
//   });
//
//   document.body.addEventListener('mouseout', (e) => {
//     overlay.style.display = 'none';
//   });
// });
