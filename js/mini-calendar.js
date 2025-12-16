// Mini Calendar Widget for Footer
function createMiniCalendar() {
  const today = new Date();
  const currentDay = today.getDate();
  const currentMonth = today.getMonth();
  const currentYear = today.getFullYear();

  // Month names in multiple languages
  const monthNames = {
    en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    ro: ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec'],
    fr: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
    de: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
    es: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  };

  // Get current language
  const currentLang = localStorage.getItem('selectedLanguage') || 'en';
  const monthName = monthNames[currentLang]?.[currentMonth] || monthNames['en'][currentMonth];

  // Get days in month
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDay = new Date(currentYear, currentMonth, 1).getDay();

  // Create calendar widget
  const calendarWidget = document.createElement('div');
  calendarWidget.id = 'mini-calendar-widget';
  calendarWidget.style.cssText = `
    position: fixed;
    bottom: 10px;
    left: 10px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    z-index: 999;
    backdrop-filter: blur(10px);
    border: 2px solid #667eea;
    font-family: 'Fredoka', sans-serif;
    width: 220px;
  `;

  // Calendar header
  const header = document.createElement('div');
  header.style.cssText = `
    text-align: center;
    font-size: 1.2rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 2px solid #667eea;
  `;
  header.textContent = `${monthName} ${currentYear}`;
  calendarWidget.appendChild(header);

  // Weekday headers
  const weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  const weekdayRow = document.createElement('div');
  weekdayRow.style.cssText = `
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
    margin-bottom: 5px;
  `;

  weekdays.forEach(day => {
    const dayHeader = document.createElement('div');
    dayHeader.style.cssText = `
      text-align: center;
      font-size: 0.8rem;
      font-weight: 600;
      color: #999;
    `;
    dayHeader.textContent = day;
    weekdayRow.appendChild(dayHeader);
  });
  calendarWidget.appendChild(weekdayRow);

  // Days grid
  const daysGrid = document.createElement('div');
  daysGrid.style.cssText = `
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
  `;

  // Add empty cells for days before month starts
  for (let i = 0; i < firstDay; i++) {
    const emptyDay = document.createElement('div');
    emptyDay.style.cssText = `
      aspect-ratio: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    `;
    daysGrid.appendChild(emptyDay);
  }

  // Add days
  for (let day = 1; day <= daysInMonth; day++) {
    const dayCell = document.createElement('div');
    const isToday = day === currentDay;

    dayCell.style.cssText = `
      aspect-ratio: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      font-size: ${isToday ? '1.4rem' : '0.9rem'};
      font-weight: ${isToday ? '900' : '500'};
      color: ${isToday ? 'white' : '#333'};
      background: ${isToday ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'transparent'};
      cursor: pointer;
      transition: all 0.3s ease;
      transform: ${isToday ? 'scale(1.2)' : 'scale(1)'};
      box-shadow: ${isToday ? '0 5px 15px rgba(102, 126, 234, 0.5)' : 'none'};
      z-index: ${isToday ? '10' : '1'};
      position: relative;
    `;

    dayCell.textContent = day;

    // Add hover effect (except for today)
    if (!isToday) {
      dayCell.addEventListener('mouseenter', () => {
        dayCell.style.background = '#e8f0fe';
        dayCell.style.transform = 'scale(1.1)';
      });
      dayCell.addEventListener('mouseleave', () => {
        dayCell.style.background = 'transparent';
        dayCell.style.transform = 'scale(1)';
      });
    }

    // Add pulsing animation for today
    if (isToday) {
      const style = document.createElement('style');
      style.textContent = `
        @keyframes pulse {
          0%, 100% { transform: scale(1.2); }
          50% { transform: scale(1.3); }
        }
      `;
      if (!document.getElementById('calendar-pulse-animation')) {
        style.id = 'calendar-pulse-animation';
        document.head.appendChild(style);
      }
      dayCell.style.animation = 'pulse 2s ease-in-out infinite';
    }

    daysGrid.appendChild(dayCell);
  }

  calendarWidget.appendChild(daysGrid);

  // Add to page
  document.body.appendChild(calendarWidget);
}

// Initialize mini calendar on page load
document.addEventListener('DOMContentLoaded', () => {
  // Wait a bit to ensure page is fully loaded
  setTimeout(createMiniCalendar, 500);
});

// Update calendar when language changes
window.addEventListener('languageChanged', () => {
  const existingCalendar = document.getElementById('mini-calendar-widget');
  if (existingCalendar) {
    existingCalendar.remove();
  }
  createMiniCalendar();
});
