// Mini Calendar Widget for Footer - Auto-scaling to fit footer height
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

  // DETECT BODY ZOOM (for responsive scaling)
  const bodyStyle = window.getComputedStyle(document.body);
  const bodyZoom = parseFloat(bodyStyle.zoom) || 1; // Get zoom value, default to 1

  // CALCULATE FOOTER HEIGHT AND AVAILABLE SPACE
  const footer = document.querySelector('footer');
  let footerHeight = footer ? footer.offsetHeight : 80; // Default 80px if not found

  // Adjust for body zoom - if body is zoomed, footer appears smaller
  footerHeight = footerHeight * bodyZoom;

  const margin = 7; // 2mm ≈ 7-8px margin
  const availableHeight = footerHeight - (margin * 2); // Height minus top and bottom margins

  // CALCULATE OPTIMAL CALENDAR SIZE
  // Calendar needs: header + weekdays + ~5 rows of days
  // Let's calculate scale factor
  const baseHeight = 180; // Base calendar height at normal size
  const scaleFactor = Math.min(1, availableHeight / baseHeight); // Don't scale up, only down

  // Apply scale to all dimensions
  const calendarWidth = Math.floor(150 * scaleFactor);
  const padding = Math.max(3, Math.floor(5 * scaleFactor));
  const headerFontSize = Math.max(0.6, 0.75 * scaleFactor);
  const dayFontSize = Math.max(0.5, 0.6 * scaleFactor);
  const todayFontSize = Math.max(0.7, 0.85 * scaleFactor);
  const gap = Math.max(1, Math.floor(2 * scaleFactor));

  // Create calendar widget - auto-scaled
  const calendarWidget = document.createElement('div');
  calendarWidget.id = 'mini-calendar-widget';
  calendarWidget.style.cssText = `
    position: absolute;
    top: 50%;
    left: ${margin}px;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.95);
    border-radius: ${Math.max(5, Math.floor(8 * scaleFactor))}px;
    padding: ${padding}px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    z-index: 10;
    backdrop-filter: blur(10px);
    border: ${Math.max(1, Math.floor(2 * scaleFactor))}px solid #667eea;
    font-family: 'Fredoka', sans-serif;
    width: ${calendarWidth}px;
    max-height: ${availableHeight}px;
    overflow: hidden;
  `;

  // Calendar header
  const header = document.createElement('div');
  header.style.cssText = `
    text-align: center;
    font-size: ${headerFontSize}rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: ${Math.max(2, Math.floor(3 * scaleFactor))}px;
    padding-bottom: ${Math.max(2, Math.floor(3 * scaleFactor))}px;
    border-bottom: ${Math.max(1, Math.floor(2 * scaleFactor))}px solid #667eea;
  `;
  header.textContent = `${monthName} ${currentYear}`;
  calendarWidget.appendChild(header);

  // Weekday headers
  const weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  const weekdayRow = document.createElement('div');
  weekdayRow.style.cssText = `
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: ${gap}px;
    margin-bottom: ${Math.max(1, Math.floor(2 * scaleFactor))}px;
  `;

  weekdays.forEach(day => {
    const dayHeader = document.createElement('div');
    dayHeader.style.cssText = `
      text-align: center;
      font-size: ${Math.max(0.5, 0.6 * scaleFactor)}rem;
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
    gap: ${gap}px;
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
      border-radius: ${Math.max(2, Math.floor(4 * scaleFactor))}px;
      font-size: ${isToday ? todayFontSize : dayFontSize}rem;
      font-weight: ${isToday ? '900' : '500'};
      color: ${isToday ? 'white' : '#333'};
      background: ${isToday ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'transparent'};
      cursor: pointer;
      transition: all 0.3s ease;
      transform: ${isToday ? 'scale(1.1)' : 'scale(1)'};
      box-shadow: ${isToday ? '0 2px 8px rgba(102, 126, 234, 0.5)' : 'none'};
      z-index: ${isToday ? '10' : '1'};
      position: relative;
    `;

    dayCell.textContent = day;

    // Add hover effect (except for today)
    if (!isToday) {
      dayCell.addEventListener('mouseenter', () => {
        dayCell.style.background = '#e8f0fe';
        dayCell.style.transform = 'scale(1.05)';
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
          0%, 100% { transform: scale(1.1); }
          50% { transform: scale(1.15); }
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

  // Add to footer (not body) so it's inside the green bar
  if (footer) {
    footer.appendChild(calendarWidget);
  } else {
    document.body.appendChild(calendarWidget);
  }

  // Log scaling info for debugging
  console.log('Calendar auto-scaled:', {
    footerHeight,
    availableHeight,
    scaleFactor: scaleFactor.toFixed(2),
    calendarWidth,
    margin
  });
}

// Initialize mini calendar on page load
document.addEventListener('DOMContentLoaded', () => {
  // Wait for footer to be rendered
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

// Recreate calendar on window resize to adjust to new footer size
window.addEventListener('resize', () => {
  const existingCalendar = document.getElementById('mini-calendar-widget');
  if (existingCalendar) {
    existingCalendar.remove();
  }
  setTimeout(createMiniCalendar, 100);
});
