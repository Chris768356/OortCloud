const starfield = document.getElementById('starfield');
let shadows = [];

for (let i = 0; i < 550; i++) {
    const x = Math.floor(Math.random() * 2000);
    const y = Math.floor(Math.random() * 2000);
    
    const colors = ['var(--text-main)', 'var(--text-muted)', 'var(--primary-color)'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    
    shadows.push(`${x}px ${y}px 0.5px ${randomColor}`);
}
starfield.style.boxShadow = shadows.join(', ');