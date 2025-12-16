/**
 * 🕰️ CLASSIC BIG BEN STYLE COUNTDOWN CLOCKS 🕰️
 * Displays two animated, vintage pendulum clocks in the Hero section.
 * - Victorian/Gothic design.
 * - Swinging pendulum.
 * - Auto-hiding logic.
 */

(function () {

    // --- CONFIGURATION ---
    const TARGET_YEAR = 2025;

    const TARGETS = {
        christmas: new Date(`December 25, ${TARGET_YEAR} 00:00:00`).getTime(),
        newyear: new Date(`January 1, ${TARGET_YEAR + 1} 00:00:00`).getTime()
    };

    const TRANSLATIONS = {
        en: { christmas: 'Christmas', newyear: 'New Year 2026', days: 'd', hours: 'h', mins: 'm', secs: 's' },
        ro: { christmas: 'Crăciun', newyear: 'Anul Nou 2026', days: 'z', hours: 'o', mins: 'm', secs: 's' },
        fr: { christmas: 'Noël', newyear: 'Nouvel An 2026', days: 'j', hours: 'h', mins: 'm', secs: 's' },
        de: { christmas: 'Weihnachten', newyear: 'Neujahr 2026', days: 't', hours: 's', mins: 'm', secs: 's' },
        es: { christmas: 'Navidad', newyear: 'Año Nuevo 2026', days: 'd', hours: 'h', mins: 'm', secs: 's' }
    };

    // --- CREATE CLOCKS (BIG BEN STYLE) ---
    function createClocks() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        // Inject CSS Animations & Styles
        const styleSheet = document.createElement("style");
        styleSheet.innerText = `
            @keyframes swing-pendulum { 
                0% { transform: rotate(10deg); } 
                50% { transform: rotate(-10deg); } 
                100% { transform: rotate(10deg); } 
            }
            
            .bigben-clock {
                position: absolute; top: 10px; width: 110px;
                display: flex; flex-direction: column; align-items: center;
                z-index: 5;
                font-family: 'Times New Roman', serif;
                filter: drop-shadow(0 5px 8px rgba(0,0,0,0.6));
                color: #2c3e50;
            }
            
            /* Roof / Top Ornament */
            .clock-top {
                width: 0; height: 0; 
                border-left: 50px solid transparent; border-right: 50px solid transparent;
                border-bottom: 35px solid #1a1a1a; /* Dark Gothic Roof */
                position: relative;
                margin-bottom: -2px;
                z-index: 2;
            }
            .clock-top::after { /* Spire */
                content: ''; position: absolute; top: 35px; left: -50px; width: 100px; height: 5px; background: #c5a059; /* Gold trim */
            }

            /* Clock Body/Face */
            .clock-face {
                width: 90px; height: 90px;
                background: radial-gradient(circle, #fffbe6 60%, #e6dcb8 100%); /* Creamy Clock Face */
                border: 6px solid #1a1a1a; /* Dark Iron Border */
                border-radius: 50%;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.4), 0 0 0 4px #c5a059; /* Gold outer ring */
                position: relative;
                z-index: 2;
            }
            
            /* Pendulum Housing */
            .pendulum-box {
                position: absolute; top: 70px; /* Behind face */
                width: 60px; height: 20px;
                display: flex; justify-content: center;
                z-index: 1;
            }
            
            .pendulum {
                width: 6px; height: 80px;
                background: linear-gradient(to right, #8B4513, #5d4037); /* Wood/Brass Rod */
                transform-origin: top center;
                animation: swing-pendulum 2s ease-in-out infinite;
                position: relative;
                top: 10px;
            }
            .pendulum-weight {
                width: 24px; height: 24px;
                background: radial-gradient(circle at 30% 30%, #ffd700, #b8860b); /* Gold Weight */
                border-radius: 50%;
                position: absolute; bottom: 0; left: -9px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                border: 1px solid #5d4037;
            }

            /* Content */
            .clock-label { font-size: 0.55rem; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 2px; color: #b71c1c; text-shadow: 0 1px 0 rgba(255,255,255,0.5); }
            .clock-time { font-size: 0.8rem; font-weight: bold; line-height: 1.1; text-align: center; color: #1a1a1a; }
            .small-text { font-size: 0.6em; color: #555; }
        `;
        document.head.appendChild(styleSheet);


        // Left Clock (Christmas)
        const leftClock = document.createElement('div');
        leftClock.id = 'clock-christmas';
        leftClock.className = 'bigben-clock';
        leftClock.style.left = '30px';
        leftClock.innerHTML = `
            <div class="clock-top"></div>
            <div class="clock-face">
                <div class="clock-label">CHRISTMAS</div>
                <div class="clock-time" id="content-christmas">Loading...</div>
            </div>
            <div class="pendulum-box">
                <div class="pendulum"><div class="pendulum-weight"></div></div>
            </div>
        `;

        // Right Clock (New Year)
        const rightClock = document.createElement('div');
        rightClock.id = 'clock-newyear';
        rightClock.className = 'bigben-clock';
        rightClock.style.right = '30px';
        rightClock.innerHTML = `
            <div class="clock-top"></div>
            <div class="clock-face">
                <div class="clock-label" style="color: #1a237e;">NEW YEAR</div>
                <div class="clock-time" id="content-newyear">Loading...</div>
            </div>
            <div class="pendulum-box">
                <div class="pendulum"><div class="pendulum-weight"></div></div>
            </div>
        `;

        // Append
        hero.appendChild(leftClock);
        hero.appendChild(rightClock);

        // Initial Update
        updateClocks();

        // Start Interval
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

        let xmasTarget = new Date(`December 25, ${currentYear} 00:00:00`).getTime();
        if (currentTime > xmasTarget + (1000 * 60 * 60 * 24)) {
            xmasTarget = new Date(`December 25, ${currentYear + 1} 00:00:00`).getTime();
        }

        let nyTarget = new Date(`January 1, ${currentYear + 1} 00:00:00`).getTime();

        const currentLang = localStorage.getItem('selectedLanguage') || 'en';
        const t = TRANSLATIONS[currentLang] || TRANSLATIONS['en'];

        if (currentTime > xmasTarget && currentTime < xmasTarget + (1000 * 60 * 60 * 24)) {
            updateClockContent('content-christmas', -1, t.christmas, t, '🎄');
        } else if (currentTime > xmasTarget) {
            leftClock.style.display = 'none';
        } else {
            const xmasDiff = xmasTarget - currentTime;
            updateClockContent('content-christmas', xmasDiff, t.christmas, t, '🎄');
        }

        if (currentTime > nyTarget) {
            rightClock.style.display = 'none';
        } else {
            const nyDiff = nyTarget - currentTime;
            updateClockContent('content-newyear', nyDiff, t.newyear.replace('2026', currentYear + 1), t, '🎆');
        }
    }

    function updateClockContent(elementId, diff, label, t, icon) {
        const el = document.getElementById(elementId);
        if (!el) return;

        if (diff < 0) {
            el.innerHTML = `<div style="font-size: 1.5rem;">${icon}</div><div style="font-size: 0.7rem;">${label}!</div>`;
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        el.innerHTML = `
            ${days}<span class="small-text">${t.days}</span> ${hours}<span class="small-text">${t.hours}</span><br>
            ${minutes}<span class="small-text">${t.mins}</span> ${seconds}<span class="small-text">${t.secs}</span>
        `;
    }

    document.addEventListener('DOMContentLoaded', createClocks);
    window.addEventListener('languageChanged', updateClocks);

})();
