/* 动态显示时间 */
function updateTime() {
    const now = new Date();
    document.getElementById('current-time').textContent = now.toLocaleTimeString();
}
setInterval(updateTime, 1000);
updateTime();

/* 轮播图 */
const imgs = [
    '/static/img/1.jpg',
    '/static/img/2.jpg',
    '/static/img/3.jpg',
    '/static/img/4.jpg'
];
let index = 0;
const imgEl   = document.getElementById('img');
const dots    = document.querySelectorAll('.pageicon li');

function rotate() {
    index = (index + 1) % imgs.length;
    imgEl.src = imgs[index];
    dots.forEach((li, i) => li.className = i === index ? 'yellow' : 'orange');
}
setInterval(rotate, 3000);