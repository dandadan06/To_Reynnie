// script.js

let tulips = document.getElementById('tulips');

for (let i = 0; i < 100; i++) {
  let tulip = document.createElement('div');
  tulip.classList.add('tulip');

  let color = Math.random() < 0.3 ? 'red' : Math.random() < 0.6 ? 'pink' : 'yellow';
  tulip.classList.add(color);

  tulips.appendChild(tulip);

  tulip.style.left = Math.random() * 100 + '%';
}