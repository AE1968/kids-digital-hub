// ============================================
// Kids Digital Hub - Internationalization System
// ============================================

class I18n {
  constructor() {
    this.currentLang = 'en';
    this.translations = {};
    this.supportedLanguages = [
      { code: 'en', name: 'English (US)', flag: '🇺🇸' },
      { code: 'en-GB', name: 'English (UK)', flag: '🇬🇧' },
      { code: 'ro', name: 'Română', flag: '🇷🇴' },
      { code: 'es', name: 'Español', flag: '🇪🇸' },
      { code: 'fr', name: 'Français', flag: '🇫🇷' },
      { code: 'de', name: 'Deutsch', flag: '🇩🇪' }
    ];
  }

  async init() {
    // Load translations
    try {
      const response = await fetch('data/translations.json');
      this.translations = await response.json();

      // Get saved language or detect browser language
      const savedLang = localStorage.getItem('preferredLanguage');
      const browserLang = navigator.language.split('-')[0];

      if (savedLang && this.translations[savedLang]) {
        this.currentLang = savedLang;
      } else if (this.translations[browserLang]) {
        this.currentLang = browserLang;
      }

      this.applyTranslations();
      this.updateLanguageSelector();
    } catch (error) {
      console.error('Failed to load translations:', error);
    }
  }

  t(key, lang = null) {
    const language = lang || this.currentLang;
    const keys = key.split('.');
    let value = this.translations[language];

    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        return key; // Return key if translation not found
      }
    }

    return value || key;
  }

  setLanguage(langCode) {
    if (this.translations[langCode]) {
      this.currentLang = langCode;
      localStorage.setItem('preferredLanguage', langCode);
      this.applyTranslations();
      this.updateLanguageSelector();

      // Trigger custom event for language change
      window.dispatchEvent(new CustomEvent('languageChanged', {
        detail: { language: langCode }
      }));
    }
  }

  applyTranslations() {
    // Translate all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const key = element.getAttribute('data-i18n');
      const translation = this.t(key);

      if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
        element.placeholder = translation;
      } else {
        element.textContent = translation;
      }
    });

    // Translate elements with data-i18n-html (allows HTML content)
    document.querySelectorAll('[data-i18n-html]').forEach(element => {
      const key = element.getAttribute('data-i18n-html');
      element.innerHTML = this.t(key);
    });

    // Update page title
    const titleKey = document.querySelector('meta[name="title-key"]');
    if (titleKey) {
      document.title = this.t(titleKey.content);
    }
  }

  updateLanguageSelector() {
    const selector = document.getElementById('languageSelector');
    if (selector) {
      const currentLangData = this.supportedLanguages.find(l => l.code === this.currentLang);
      const button = selector.querySelector('.lang-current');
      if (button && currentLangData) {
        button.innerHTML = `${currentLangData.flag} ${currentLangData.name}`;
      }
    }
  }

  getCurrentLanguage() {
    return this.currentLang;
  }

  getSupportedLanguages() {
    return this.supportedLanguages;
  }
}

// Create global instance
const i18n = new I18n();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
  i18n.init();
}
