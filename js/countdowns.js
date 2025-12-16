/**
 * 🎄 FESTIVE COUNTDOWN CLOCKS 🎆
 * Displays two animated countdown clocks in the Hero section:
 * 1. Left: Countdown to Christmas (Dec 25)
 * 2. Right: Countdown to New Year (Jan 1)
 */

(function () {

    // --- CONFIGURATION ---
    const TARGET_YEAR = 2025; // Target year for next events

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

    // --- CREATE CLOCKS ---
    function createClocks() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        // Styles
        const clockStyle = `
            position: absolute;
            top: 20px;
            width: 100px;
            height: 100px;
            background: rgba(0, 137, 123, 0.2); /* Very transparent like footer */
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-radius: 50%;
            border: 1px solid rgba(255, 255, 255, 0.4);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
            font-family: 'Fredoka', sans-serif;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            z-index: 5;
            transition: transform 0.3s ease;
            cursor: default;
        `;

        // Left Clock (Christmas)
        const leftClock = document.createElement('div');
        leftClock.id = 'clock-christmas';
        leftClock.style.cssText = clockStyle + 'left: 20px;';
        // Add hover effect
        leftClock.onmouseenter = () => leftClock.style.transform = 'scale(1.1)';
        leftClock.onmouseleave = () => leftClock.style.transform = 'scale(1)';

        // Right Clock (New Year)
        const rightClock = document.createElement('div');
        rightClock.id = 'clock-newyear';
        rightClock.style.cssText = clockStyle + 'right: 20px;';
        // Add hover effect
        rightClock.onmouseenter = () => rightClock.style.transform = 'scale(1.1)';
        rightClock.onmouseleave = () => rightClock.style.transform = 'scale(1)';

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
        const currentMonth = now.getMonth(); // 0-11 (Dec is 11)

        // Only show clocks if it's December OR early January (for NY) OR November (anticipation)
        // We want them to reappear every December.
        const isFestiveSeason = (currentMonth === 11) || (currentMonth === 10); // Nov & Dec

        const leftClock = document.getElementById('clock-christmas');
        const rightClock = document.getElementById('clock-newyear');

        if (!leftClock || !rightClock) return;

        // Auto-hide if not festive season
        if (!isFestiveSeason) {
            leftClock.style.display = 'none';
            rightClock.style.display = 'none';
            return;
        } else {
            leftClock.style.display = 'flex';
            rightClock.style.display = 'flex';
        }

        // Dynamic Target Calculation (Always look for THIS year's Dec or NEXT year's Jan)
        let xmasTarget = new Date(`December 25, ${currentYear} 00:00:00`).getTime();
        // If passed Dec 25, target NEXT year (though we hide it anyway until next Nov)
        if (currentTime > xmasTarget + (1000 * 60 * 60 * 24)) { // +1 day buffer
            xmasTarget = new Date(`December 25, ${currentYear + 1} 00:00:00`).getTime();
        }

        let nyTarget = new Date(`January 1, ${currentYear + 1} 00:00:00`).getTime();

        const currentLang = localStorage.getItem('selectedLanguage') || 'en';
        const t = TRANSLATIONS[currentLang] || TRANSLATIONS['en'];

        // Update Left (Christmas)
        if (currentTime > xmasTarget && currentTime < xmasTarget + (1000 * 60 * 60 * 24)) {
            // It is Christmas Day!
            updateClockContent('clock-christmas', -1, t.christmas, t, '🎄');
        } else if (currentTime > xmasTarget) {
            leftClock.style.display = 'none'; // Hide if passed
        } else {
            const xmasDiff = xmasTarget - currentTime;
            updateClockContent('clock-christmas', xmasDiff, t.christmas, t, '🎄');
        }

        // Update Right (New Year)
        if (currentTime > nyTarget) {
            // Passed New Year
            rightClock.style.display = 'none';
        } else {
            const nyDiff = nyTarget - currentTime;
            updateClockContent('clock-newyear', nyDiff, t.newyear.replace('2026', currentYear + 1), t, '🎆');
        }
    }

    function updateClockContent(id, diff, label, t, icon) {
        const el = document.getElementById(id);
        if (!el) return;

        if (diff < 0) {
            el.innerHTML = `<div style="font-size: 2rem;">${icon}</div><div style="font-size: 0.8rem;">${label}!</div>`;
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        el.innerHTML = `
            <div style="font-size: 0.7rem; font-weight: bold; margin-bottom: 2px;">${label}</div>
            <div style="font-size: 0.9rem; font-weight: 800; line-height: 1.1;">
                ${days}${t.days} ${hours}${t.hours}<br>
                ${minutes}${t.mins} ${seconds}${t.secs}
            </div>
            <div style="font-size: 0.8rem; margin-top: 2px;">${icon}</div>
        `;
    }

    // --- INIT ---
    document.addEventListener('DOMContentLoaded', createClocks);
    window.addEventListener('languageChanged', updateClocks);

})();
