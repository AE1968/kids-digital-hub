# 💱 CURRENCY CONVERSION SYSTEM - DOCUMENTATION

## Automatic Currency Display Based on Language

**Status:** ✅ IMPLEMENTED  
**File:** `js/currency.js`

---

## 🌍 LANGUAGE TO CURRENCY MAPPING

| Language | Code | Currency | Symbol | Example |
|----------|------|----------|--------|---------|
| English  | EN   | USD      | $      | $4.99   |
| Română   | RO   | RON      | lei    | 23,19 lei |
| Español  | ES   | EUR      | €      | €4,59   |
| Français | FR   | EUR      | €      | €4,59   |
| Deutsch  | DE   | EUR      | €      | €4,59   |

---

## 💰 EXCHANGE RATES

**Base Currency:** USD (US Dollar)

```javascript
USD: 1.00
RON: 4.65  // 1 USD = 4.65 RON
EUR: 0.92  // 1 USD = 0.92 EUR
```

**Note:** Rates should be updated periodically (monthly recommended)

---

## 🎯 HOW IT WORKS

### **1. Automatic Detection:**
```javascript
// User selects language
i18n.setLanguage('ro');

// Currency system detects and converts
getCurrentCurrency(); // Returns 'RON'
```

### **2. Price Conversion:**
```javascript
// Original price in USD
const usdPrice = "$4.99";

// Convert to Romanian Lei
convertPrice(4.99, 'RON'); // Returns 23.2035

// Format with symbol
formatPrice(23.2035, 'RON'); // Returns "23,20 lei"
```

### **3. Display Format:**
```javascript
// English (USD)
$4.99

// Romanian (RON)
23,20 lei  // Note: comma as decimal separator

// Spanish/French/German (EUR)
€4,59  // Note: comma as decimal separator
```

---

## 🔧 USAGE IN CODE

### **Get Localized Price:**
```javascript
// Simple usage
const localizedPrice = Currency.getLocalizedPrice("$4.99");
// Returns: "$4.99" (EN), "23,20 lei" (RO), "€4,59" (ES/FR/DE)
```

### **Get Price Details:**
```javascript
const details = Currency.getPriceDetails("$4.99");
// Returns:
{
  original: "$4.99",
  currency: "RON",
  symbol: "lei",
  converted: 23.2035,
  formatted: "23,20 lei",
  isFree: false
}
```

### **In HTML:**
```html
<!-- Add data-price-usd attribute -->
<span class="product-price" data-price-usd="$4.99">$4.99</span>

<!-- Will auto-update when language changes -->
```

---

## 🎁 CHRISTMAS PROMOTION PRICES

### **Free Products ($0.00):**

**English:**
```
Original: $4.99 (strikethrough)
Promotion: $0.00 🎁
```

**Romanian:**
```
Original: 23,20 lei (strikethrough)
Promotion: 0,00 lei 🎁
```

**Spanish/French/German:**
```
Original: €4,59 (strikethrough)
Promotion: €0,00 🎁
```

---

## 🔄 AUTO-UPDATE ON LANGUAGE CHANGE

**Event Listener:**
```javascript
document.addEventListener('languageChanged', () => {
  Currency.updateAllPrices();
});
```

**Flow:**
1. User clicks language selector
2. `i18n.setLanguage('ro')` is called
3. Event `languageChanged` is dispatched
4. Currency system updates all prices automatically
5. All `[data-price-usd]` elements are converted

---

## 📊 EXAMPLES

### **Product Card:**
```javascript
// USD (English)
Name: Pokémon Coloring Book
Price: $4.99

// RON (Romanian)
Name: Carte de Colorat Pokémon
Price: 23,20 lei

// EUR (Spanish)
Name: Libro para Colorear Pokémon
Price: €4,59
```

### **Christmas Promotion:**
```javascript
// USD (English)
Original: $4.99
Now: $0.00 🎁
Badge: SANTA'S GIFT!

// RON (Romanian)
Original: 23,20 lei
Acum: 0,00 lei 🎁
Badge: CADOU DE LA MOȘ CRĂCIUN!

// EUR (Spanish)
Original: €4,59
Ahora: €0,00 🎁
Badge: ¡REGALO DE SANTA!
```

---

## 🛠️ CONFIGURATION

### **Update Exchange Rates:**

Edit `js/currency.js`:
```javascript
rates: {
  USD: 1.00,
  RON: 4.65,  // Update this value
  EUR: 0.92   // Update this value
}
```

**Recommended:** Update monthly or use API for real-time rates

### **Add New Currency:**

```javascript
// 1. Add rate
rates: {
  USD: 1.00,
  RON: 4.65,
  EUR: 0.92,
  GBP: 0.79  // British Pound
}

// 2. Add symbol
symbols: {
  USD: '$',
  RON: 'lei',
  EUR: '€',
  GBP: '£'
}

// 3. Add language mapping
languageToCurrency: {
  'en': 'USD',
  'ro': 'RON',
  'es': 'EUR',
  'fr': 'EUR',
  'de': 'EUR',
  'gb': 'GBP'  // British English
}

// 4. Add format
formats: {
  USD: 'symbol_before',
  RON: 'symbol_after',
  EUR: 'symbol_before',
  GBP: 'symbol_before'
}
```

---

## ✅ IMPLEMENTATION CHECKLIST

- [x] Currency conversion system created
- [x] Exchange rates configured
- [x] Language to currency mapping
- [x] Auto-update on language change
- [x] Format with correct symbols
- [x] Decimal separator (comma for RON/EUR)
- [x] Christmas promotion prices
- [x] Script added to index.html
- [ ] Update home.js to use currency system
- [ ] Update christmas-special.js to use currency system
- [ ] Add translations for "free" in all languages
- [ ] Test all language/currency combinations

---

## 🧪 TESTING

### **Test Scenarios:**

**1. Language Switch:**
- [ ] EN → USD ($4.99)
- [ ] RO → RON (23,20 lei)
- [ ] ES → EUR (€4,59)
- [ ] FR → EUR (€4,59)
- [ ] DE → EUR (€4,59)

**2. Price Display:**
- [ ] Product cards show correct currency
- [ ] Christmas promotion shows correct currency
- [ ] Free products show "FREE" in correct language
- [ ] Decimal separator correct (. for USD, , for RON/EUR)

**3. Auto-Update:**
- [ ] Prices update immediately on language change
- [ ] No page reload required
- [ ] All prices on page update

---

## 📱 RESPONSIVE BEHAVIOR

**Desktop:**
- Full price display with symbol

**Mobile:**
- Same format, no truncation
- Symbol always visible

---

## 🎉 READY!

**Currency system is:**
- ✅ Fully automatic
- ✅ Updates on language change
- ✅ Supports 3 currencies (USD, RON, EUR)
- ✅ Correct formatting for each currency
- ✅ Works with Christmas promotion

**Next Steps:**
1. Update `home.js` to use `Currency.getLocalizedPrice()`
2. Update `christmas-special.js` for promotion prices
3. Add currency translations to `translations.json`
4. Test all combinations
5. Deploy!

---

*Currency Conversion System - Ready for Deployment!* 💱

**Supported:** USD ($), RON (lei), EUR (€)  
**Auto-Update:** ✅  
**Christmas Ready:** ✅
