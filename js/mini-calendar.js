// Mini Calendar Widget - Auto-scaling to fit footer
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

  const currentLang = localStorage.getItem('selectedLanguage') || 'en';
  const monthName = monthNames[currentLang]?.[currentMonth] || monthNames['en'][currentMonth];

  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDay = new Date(currentYear, currentMonth, 1).getDay();

  // DETECT BODY ZOOM
  const bodyStyle = window.getComputedStyle(document.body);
  const bodyZoom = parseFloat(bodyStyle.zoom) || 1;

  // GET FOOTER AND CALCULATE AVAILABLE SPACE
  const footer = document.querySelector('footer');
  let footerHeight = footer ? footer.offsetHeight : 80;
  footerHeight = footerHeight * bodyZoom;

  const margin = 7;
  const availableHeight = footerHeight - (margin * 2);
  const availableWidth = 200; // Max width we want

  // PRECISE SCALE CALCULATION
  // Calculate exact height needed at base scale
  const basePadding = 5;
  const baseGap = 2;
  const baseWidth = 150;

  // Component heights at base scale (in pixels)
  const baseHeaderHeight = 18;  // Header text + padding
  const baseWeekdayHeight = 12; // Weekday row
  const baseCellSize = (baseWidth - (basePadding * 2) - (6 * baseGap)) / 7; // Square cells
  const baseGridHeight = (baseCellSize * 6) + (5 * baseGap); // 6 rows, 5 gaps
  const baseExtraMargin = 6; // Extra spacing

  const baseTotalHeight = baseHeaderHeight + baseWeekdayHeight + baseGridHeight + (basePadding * 2) + baseExtraMargin;

  // Calculate scale factor to fit in available height
  // Add 20% safety margin to GUARANTEE it fits on ANY screen
  let scale = (availableHeight * 0.80) / baseTotalHeight;

  // Additional check: if screen is very small, scale even more
  if (availableHeight < 60) {
    scale = scale * 0.8; // Extra 20% reduction for tiny screens
  }

  // Clamp between 0.3 and 1 (allow very small if absolutely necessary)
  scale = Math.max(0.3, Math.min(1, scale));

  // Apply scale to all dimensions
  const width = Math.floor(baseWidth * scale);
  const padding = Math.max(3, Math.floor(basePadding * scale));
  const borderRadius = Math.max(4, Math.floor(8 * scale));
  const borderWidth = Math.max(1, Math.floor(2 * scale));
  const gap = Math.max(1, Math.floor(baseGap * scale));

  // Font sizes with minimums
  const headerFont = `${Math.max(0.6, 0.75 * scale)}rem`;
  const weekdayFont = `${Math.max(0.5, 0.6 * scale)}rem`;
  const dayFont = `${Math.max(0.5, 0.6 * scale)}rem`;
  const todayFont = `${Math.max(0.65, 0.85 * scale)}rem`;

  // Create calendar
  const calendar = document.createElement('div');
  calendar.id = 'mini-calendar-widget';
  calendar.style.cssText = `
    position: absolute;
    top: 50%;
    left: ${margin}px;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.95);
    border-radius: ${borderRadius}px;
    padding: ${padding}px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    z-index: 10;
    backdrop-filter: blur(10px);
    border: ${borderWidth}px solid #667eea;
    font-family: 'Fredoka', sans-serif;
    width: ${width}px;
  `;

  // Header
  const header = document.createElement('div');
  header.style.cssText = `
    text-align: center;
    font-size: ${headerFont};
    font-weight: 700;
    color: #667eea;
    margin-bottom: ${Math.floor(3 * scale)}px;
    padding-bottom: ${Math.floor(3 * scale)}px;
    border-bottom: ${borderWidth}px solid #667eea;
  `;
  header.textContent = `${monthName} ${currentYear}`;
  calendar.appendChild(header);

  // Weekdays
  const weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  const weekdayRow = document.createElement('div');
  weekdayRow.style.cssText = `
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: ${gap}px;
    margin-bottom: ${Math.floor(2 * scale)}px;
  `;

  weekdays.forEach(day => {
    const cell = document.createElement('div');
    cell.style.cssText = `
      text-align: center;
      font-size: ${weekdayFont};
      font-weight: 600;
      color: #999;
    `;
    cell.textContent = day;
    weekdayRow.appendChild(cell);
  });
  calendar.appendChild(weekdayRow);

  // Days grid
  const daysGrid = document.createElement('div');
  daysGrid.style.cssText = `
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: ${gap}px;
  `;

  // Empty cells
  for (let i = 0; i < firstDay; i++) {
    const empty = document.createElement('div');
    empty.style.cssText = 'aspect-ratio: 1;';
    daysGrid.appendChild(empty);
  }

  // Days
  for (let day = 1; day <= daysInMonth; day++) {
    const isToday = day === currentDay;
    const cell = document.createElement('div');

    cell.style.cssText = `
      aspect-ratio: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: ${Math.floor(4 * scale)}px;
      font-size: ${isToday ? todayFont : dayFont};
      font-weight: ${isToday ? '900' : '500'};
      color: ${isToday ? 'white' : '#333'};
      background: ${isToday ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'transparent'};
      cursor: pointer;
      transition: all 0.3s ease;
      transform: ${isToday ? 'scale(1.1)' : 'scale(1)'};
      box-shadow: ${isToday ? '0 2px 8px rgba(102, 126, 234, 0.5)' : 'none'};
    `;

    cell.textContent = day;

    if (!isToday) {
      cell.addEventListener('mouseenter', () => {
        cell.style.background = '#e8f0fe';
        cell.style.transform = 'scale(1.05)';
      });
      cell.addEventListener('mouseleave', () => {
        cell.style.background = 'transparent';
        cell.style.transform = 'scale(1)';
      });
    }

    if (isToday) {
      const style = document.createElement('style');
      style.textContent = `
        @keyframes pulse {
          0%, 100% { transform: scale(1.1); }
          50% { transform: scale(1.15); }
        }
      `;
      if (!document.getElementById('calendar-pulse')) {
        style.id = 'calendar-pulse';
        document.head.appendChild(style);
      }
      cell.style.animation = 'pulse 2s ease-in-out infinite';
    }

    daysGrid.appendChild(cell);
  }

  calendar.appendChild(daysGrid);

  // Add to footer
  if (footer) {
    footer.appendChild(calendar);
  }

  // Detailed logging for debugging
  console.log('=== CALENDAR AUTO-SCALING ===');
  console.log('Footer height (raw):', footer ? footer.offsetHeight : 'N/A');
  console.log('Body zoom:', bodyZoom);
  console.log('Footer height (adjusted):', footerHeight);
  console.log('Available height:', availableHeight);
  console.log('Base total height:', baseTotalHeight.toFixed(2));
  console.log('Scale factor:', scale.toFixed(3));
  console.log('Final calendar width:', width);
  console.log('Final calendar estimated height:', (baseTotalHeight * scale).toFixed(2));
  console.log('Fits in footer?', (baseTotalHeight * scale) <= availableHeight ? 'YES ✓' : 'NO ✗');
  console.log('============================');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(createMiniCalendar, 500);
});

// Update on language change
window.addEventListener('languageChanged', () => {
  const existing = document.getElementById('mini-calendar-widget');
  if (existing) existing.remove();
  createMiniCalendar();
});

// Recreate on resize
window.addEventListener('resize', () => {
  const existing = document.getElementById('mini-calendar-widget');
  if (existing) existing.remove();
  setTimeout(createMiniCalendar, 100);
});
