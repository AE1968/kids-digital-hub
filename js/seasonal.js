// Seasonal Background System with Month Names in Selected Language
const seasonalBackgrounds = {
    months: {
        1: { image: 'january.png', theme: 'winter' },
        2: { image: 'february.png', theme: 'winter' },
        3: { image: 'march.png', theme: 'spring' },
        4: { image: 'april.png', theme: 'spring' },
        5: { image: 'may.png', theme: 'spring' },
        6: { image: 'june.png', theme: 'summer' },
        7: { image: 'july.png', theme: 'summer' },
        8: { image: 'august.png', theme: 'summer' },
        9: { image: 'september.png', theme: 'autumn' },
        10: { image: 'october.png', theme: 'autumn' },
        11: { image: 'november.png', theme: 'autumn' },
        12: { image: 'december.png', theme: 'winter' }
    },

    monthNames: {
        en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        ro: ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie'],
        fr: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
        de: ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
        es: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        zh: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
        ja: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        ko: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
    }
};

function setSeasonalBackground() {
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth() + 1; // 1-12
    const monthData = seasonalBackgrounds.months[currentMonth];

    if (!monthData) return;

    // Set background image
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        heroSection.style.backgroundImage = `url('assets/images/seasonal/${monthData.image}')`;
        heroSection.style.backgroundSize = 'cover';
        heroSection.style.backgroundPosition = 'center';
        heroSection.style.backgroundRepeat = 'no-repeat';
    }

    // Get current language
    const currentLang = localStorage.getItem('selectedLanguage') || 'en';
    const monthName = seasonalBackgrounds.monthNames[currentLang]?.[currentMonth - 1] ||
        seasonalBackgrounds.monthNames['en'][currentMonth - 1];

    // Create or update month display
    let monthDisplay = document.getElementById('current-month-display');
    if (!monthDisplay) {
        monthDisplay = document.createElement('div');
        monthDisplay.id = 'current-month-display';
        monthDisplay.style.cssText = `
      position: absolute;
      top: 20px;
      right: 20px;
      background: rgba(255, 255, 255, 0.9);
      padding: 15px 30px;
      border-radius: 25px;
      font-family: 'Fredoka', sans-serif;
      font-size: 1.5rem;
      font-weight: 700;
      color: #667eea;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
      z-index: 100;
      backdrop-filter: blur(10px);
      border: 3px solid #667eea;
      animation: fadeInSlide 0.5s ease-out;
    `;

        if (heroSection) {
            heroSection.style.position = 'relative';
            heroSection.appendChild(monthDisplay);
        }
    }

    monthDisplay.textContent = `📅 ${monthName}`;

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
    @keyframes fadeInSlide {
      from {
        opacity: 0;
        transform: translateX(50px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }
    
    #current-month-display:hover {
      transform: scale(1.05);
      transition: transform 0.3s ease;
    }
  `;
    if (!document.getElementById('seasonal-styles')) {
        style.id = 'seasonal-styles';
        document.head.appendChild(style);
    }
}

// Update month display when language changes
function updateMonthDisplay() {
    const monthDisplay = document.getElementById('current-month-display');
    if (monthDisplay) {
        const currentDate = new Date();
        const currentMonth = currentDate.getMonth() + 1;
        const currentLang = localStorage.getItem('selectedLanguage') || 'en';
        const monthName = seasonalBackgrounds.monthNames[currentLang]?.[currentMonth - 1] ||
            seasonalBackgrounds.monthNames['en'][currentMonth - 1];
        monthDisplay.textContent = `📅 ${monthName}`;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', setSeasonalBackground);

// Update when language changes
window.addEventListener('languageChanged', updateMonthDisplay);
