/**
 * 🎄 QUANTUM & CHRONO COUNTDOWNS 🎆
 * Left: Quantum Monolith (Christmas)
 * Right: Chrono Capsule (New Year)
 * + Fireworks Logic at Midnight!
 */

(function () {

    // --- CONFIGURATION ---
    const TARGET_YEAR = 2025;

    const TARGETS = {
        christmas: new Date(`December 25, ${TARGET_YEAR} 00:00:00`).getTime(),
        newyear: new Date(`January 1, ${TARGET_YEAR + 1} 00:00:00`).getTime() // Jan 1, 2026
    };

    const TRANSLATIONS = {
        en: { christmas: 'Christmas', newyear: 'New Year 2026', days: 'd', hours: 'h', mins: 'm', secs: 's' },
        ro: { christmas: 'Crăciun', newyear: 'Anul Nou 2026', days: 'z', hours: 'o', mins: 'm', secs: 's' },
        fr: { christmas: 'Noël', newyear: 'Nouvel An 2026', days: 'j', hours: 'h', mins: 'm', secs: 's' },
        de: { christmas: 'Weihnachten', newyear: 'Neujahr 2026', days: 't', hours: 's', mins: 'm', secs: 's' },
        es: { christmas: 'Navidad', newyear: 'Año Nuevo 2026', days: 'd', hours: 'h', mins: 'm', secs: 's' }
    };

    // --- FIREWORKS SYSTEM ---
    let fireworksInterval = null;
    function startFireworks() {
        if (fireworksInterval) return; // Already running

        // Create Canvas Overlay
        const canvas = document.createElement('canvas');
        canvas.id = 'fireworks-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0'; canvas.style.left = '0';
        canvas.style.width = '100vw'; canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];

        function Particle(x, y, color) {
            this.x = x; this.y = y; this.color = color;
            this.velocity = { x: (Math.random() - 0.5) * 8, y: (Math.random() - 0.5) * 8 };
            this.alpha = 1; this.friction = 0.95;
        }

        Particle.prototype.draw = function () {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
            ctx.restore();
        }

        Particle.prototype.update = function () {
            this.velocity.x *= this.friction;
            this.velocity.y *= this.friction;
            this.x += this.velocity.x;
            this.y += this.velocity.y;
            this.alpha -= 0.01;
        }

        function createFirework(x, y) {
            const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#ffffff'];
            const color = colors[Math.floor(Math.random() * colors.length)];
            for (let i = 0; i < 30; i++) {
                particles.push(new Particle(x, y, color));
            }
        }

        const animate = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, index) => {
                if (p.alpha > 0) { p.update(); p.draw(); } else { particles.splice(index, 1); }
            });
        };

        fireworksInterval = setInterval(() => {
            createFirework(Math.random() * canvas.width, Math.random() * canvas.height * 0.5);
            requestAnimationFrame(animate);
        }, 500); // New firework every 0.5s

        // Stop after 1 minute (60000ms)
        setTimeout(() => {
            clearInterval(fireworksInterval);
            fireworksInterval = null;
            canvas.remove();
        }, 60000);
    }


    // --- CREATE CLOCKS ---
    function createClocks() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        const styleSheet = document.createElement("style");
        styleSheet.innerText = `
            /* --- QUANTUM MONOLITH (Left) --- */
            @keyframes shimmer-line { 0% { transform: translateY(-120%); } 100% { transform: translateY(120%); } }
            @keyframes pulse-mono { 0% { box-shadow: 0 0 10px rgba(0,0,0,0.5); } 50% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); } 100% { box-shadow: 0 0 10px rgba(0,0,0,0.5); } }

            .monolith-clock {
                position: absolute; top: 10px; width: 90px; height: 140px;
                background: linear-gradient(135deg, #1a1a1a, #000000);
                border: 1px solid #333; border-radius: 4px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                box-shadow: 5px 5px 15px rgba(0,0,0,0.6);
                overflow: hidden; z-index: 5;
                font-family: 'Share Tech Mono', monospace;
                animation: pulse-mono 4s infinite;
            }
            .mono-screen {
                z-index: 2; width: 100%; text-align: center;
            }
            .mono-text { color: #d4af37; text-shadow: 0 0 5px #d4af37; font-size: 0.8rem; letter-spacing: 1px; margin: 4px 0; }
            .mono-label { color: #888; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 2px; }
            
            /* Scanning Laser */
            .mono-laser {
                position: absolute; top: 0; left: 0; right: 0; height: 100%;
                background: linear-gradient(to bottom, transparent, rgba(212, 175, 55, 0.4), transparent);
                animation: shimmer-line 3s linear infinite;
                z-index: 1; pointer-events: none;
            }

            /* --- CHRONO CAPSULE (Right) --- */
            @keyframes float-capsule { 0% { transform: translateY(0); } 50% { transform: translateY(-8px); } 100% { transform: translateY(0); } }
            @keyframes rotate-rings { 0% { transform: rotateX(70deg) rotateZ(0deg); } 100% { transform: rotateX(70deg) rotateZ(360deg); } }
            @keyframes pulse-core-energy { 0% { transform: scale(0.9); box-shadow: 0 0 15px #00e5ff; } 50% { transform: scale(1.1); box-shadow: 0 0 30px #00e5ff, 0 0 60px #00e5ff; } 100% { transform: scale(0.9); box-shadow: 0 0 15px #00e5ff; } }
            
            .capsule-clock {
                position: absolute; top: 10px; width: 90px; height: 140px;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(0, 229, 255, 0.3); border-radius: 45px / 20px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                backdrop-filter: blur(4px);
                box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
                z-index: 5;
                animation: float-capsule 5s ease-in-out infinite;
                font-family: 'Rajdhani', sans-serif;
            }
            .capsule-cap { position: absolute; width: 100%; height: 20px; border-radius: 50%; background: rgba(255,255,255,0.2); border: 1px solid rgba(0,229,255,0.5); }
            .cap-top { top: 0; } .cap-bottom { bottom: 0; }
            
            .energy-core {
                width: 40px; height: 40px; border-radius: 50%;
                background: radial-gradient(circle, #ffffff, #00e5ff);
                animation: pulse-core-energy 1.5s infinite alternate;
                position: relative; margin-bottom: 10px; z-index: 2;
            }
            
            /* Orbiting Ring */
            .orbital-ring {
                position: absolute; top: 40%; left: -10%; width: 120%; height: 30px;
                border: 2px dashed rgba(0, 229, 255, 0.6); border-radius: 50%;
                transform-style: preserve-3d;
                animation: rotate-rings 8s linear infinite;
                z-index: 1;
            }

            .capsule-text { color: #fff; font-weight: 800; font-size: 0.85rem; z-index: 3; text-shadow: 0 0 5px #00e5ff; }
            .capsule-label { color: rgba(255,255,255,0.7); font-size: 0.6rem; text-transform: uppercase; z-index: 3; margin-bottom: 5px;}
        `;
        document.head.appendChild(styleSheet);


        // --- CHRISTMAS: QUANTUM MONOLITH (Black & Gold) ---
        const leftClock = document.createElement('div');
        leftClock.id = 'clock-christmas';
        leftClock.className = 'monolith-clock';
        leftClock.style.left = '30px';
        leftClock.innerHTML = `
            <div class="mono-laser"></div>
            <div class="mono-screen">
                <div class="mono-label">TARGET:</div>
                <div class="mono-label" style="color: #d4af37; font-weight:bold;">X-MAS</div>
                <div style="font-size:1.5rem; margin:5px 0;">🎄</div>
                <div class="mono-text" id="content-christmas">--:--:--</div>
            </div>
        `;

        // --- NEW YEAR: CHRONO CAPSULE (Ice Blue/Energy) ---
        const rightClock = document.createElement('div');
        rightClock.id = 'clock-newyear';
        rightClock.className = 'capsule-clock';
        rightClock.style.right = '30px';
        rightClock.innerHTML = `
            <div class="capsule-cap cap-top"></div>
            <div class="capsule-cap cap-bottom"></div>
            <div class="orbital-ring"></div>
            
            <div class="energy-core"></div>
            <div class="capsule-label">INITIATING</div>
            <div class="capsule-text" id="content-newyear">--:--:--</div>
        `;

        // Append
        hero.appendChild(leftClock);
        hero.appendChild(rightClock);

        // Initial Update
        updateClocks();
        setInterval(updateClocks, 1000);
    }

    // --- UPDATE LOGIC ---
    function updateClocks() {
        const now = new Date();
        const currentTime = now.getTime();
        const currentYear = now.getFullYear();
        const currentMonth = now.getMonth();

        const isFestiveSeason = (currentMonth === 11) || (currentMonth === 10);

        const leftClock = document.getElementById('clock-christmas');
        const rightClock = document.getElementById('clock-newyear');

        if (!leftClock || !rightClock) return;

        if (!isFestiveSeason) {
            leftClock.style.display = 'none';
            rightClock.style.display = 'none';
            return;
        } else {
            leftClock.style.display = 'flex';
            rightClock.style.display = 'flex';
        }

        // --- TARGET CALCULATIONS ---
        const xmasTarget = new Date(`December 25, ${currentYear} 00:00:00`).getTime();
        const nyTarget = new Date(`January 1, ${currentYear + 1} 00:00:00`).getTime();

        const currentLang = localStorage.getItem('selectedLanguage') || 'en';
        const t = TRANSLATIONS[currentLang] || TRANSLATIONS['en'];

        // --- UPDATE CHRISTMAS (Left) ---
        if (currentTime > xmasTarget && currentTime < xmasTarget + (1000 * 60 * 60 * 24)) {
            // Is Christmas Day
            document.getElementById('content-christmas').innerHTML = "DEPLOYED";
        } else if (currentTime > xmasTarget) {
            leftClock.style.display = 'none';
        } else {
            const xmasDiff = xmasTarget - currentTime;
            updateClockContent('content-christmas', xmasDiff, t, false);
        }

        // --- UPDATE NEW YEAR (Right) ---
        const nyDiff = nyTarget - currentTime;

        // FIREWORKS TRIGGER
        if (nyDiff <= 0 && nyDiff > -60000) {
            // 00:00 to 00:01 -> FIREWORKS!
            rightClock.style.display = 'none'; // Hide clock during fireworks? Or keep it showing 00:00?
            // Requirement: "foc de artificii ... dupa care dezactivezi ceasul"
            // Let's hide clock and boom.
            rightClock.style.display = 'none';
            if (!fireworksInterval) startFireworks();
        } else if (nyDiff <= -60000) {
            // After 1 minute
            rightClock.style.display = 'none';
        } else {
            // Counting down
            updateClockContent('content-newyear', nyDiff, t, true);
        }
    }

    function updateClockContent(elementId, diff, t, isNewYear) {
        const el = document.getElementById(elementId);
        if (!el) return;

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Standard formatting
        el.innerHTML = `
            ${days}${t.days} ${hours}${t.hours}<br>
            ${minutes}${t.mins} ${seconds}${t.secs}
        `;

        // Dynamic Label for New Year
        if (isNewYear) {
            const label = document.querySelector('#clock-newyear .capsule-label');
            if (label) label.innerText = t.newyear.split(' ')[0] + ' ' + (new Date().getFullYear() + 1);
        }
    }

    document.addEventListener('DOMContentLoaded', createClocks);
    window.addEventListener('languageChanged', updateClocks);

})();
