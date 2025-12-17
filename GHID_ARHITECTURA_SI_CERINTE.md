# CARTA TEHNICĂ: KIDS DIGITAL HUB
## Ghid de Arhitectură și Cerințe Funcționale
**Versiunea:** 1.0
**Status:** Funcțional & Scalabil

---

## 1. VIZIUNEA GENERALĂ ȘI FILOZOFIA
Aplicația este un **Hub Educațional Digital** pentru copii, securizat și fără distrageri inutile.
*   **Ton:** Universitar, Cald, Bunicos (Blând dar Educat).
*   **Structura:** Dashboard central cu 3 module principale: Desene, Jocuri, Povești.
*   **Model de Business:** Freemium.
    *   **Free:** Sloturile 1-9 (conținut zilnic).
    *   **Premium:** Slotul 10+ (Software Profesional, Multiplayer, Audiobooks).
    *   Non-adminii NU văd sloturile Premium deloc. Adminul are acces deplin.

## 2. ARHITECTURA TEHNICĂ
*   **Frontend:** HTML5, CSS3 (Modern/Glassmorphism), JavaScript (Vanilla - fără framework-uri grele).
*   **Date:** `localStorage` pentru persistență ușoară (limbă, ștergeri, statistici).
*   **Configurație Dinamică:** Toate galeriile (Desene, Jocuri, Povești) sunt generate dinamic din fișiere JS (`drawingsConfig`, `gamesConfig`, `storiesConfig`), pregătite pentru a fi alimentate automat de un server în viitor.
*   **Multilingual:** Suport nativ pentru 6 limbi (RO, EN, IT, DE, FR, ES). Sistemul detectează limba și adaptează interfața + vocea naratorului.

## 3. MODULUL 1: DESENE (DRAWINGS)
**Fișier:** `gallery-drawings.html`
*   **Grilă:** Sloturi numerotate vizibil (1, 2, 3...).
*   **Logica:**
    *   Serverul va popula zilnic sloturile libere.
    *   Utilizatorul poate șterge ("Trash") un desen terminat pentru a face loc.
*   **Editor (Paint Pro):**
    *   Unelte: Pensulă, Marker, Creion, Radieră.
    *   Controale: Slider vertical pentru Mărime și Opacitate.
    *   Funcții: Print, Undo, Clear All.
    *   **FĂRĂ SAVE** (Doar Print & Exit).
*   **Premium (Slot 10):** "Mandala Expert" - va necesita un Paint Studio avansat (Layers, Effects).

## 4. MODULUL 2: JOCURI (GAMES)
**Fișier:** `gallery-games.html`
*   **Tipologie:**
    1.  **Worksheets (Fișe de Lucru):** Ex: Labirint (Maze), Connect Dots.
        *   Mecanică: Creion simplu + Cronometru (Start/Stop).
        *   Scop: Educativ, logică rapidă.
    2.  **Board Games (Premium):** Șah, Table, X și 0.
        *   Mecanică: Multiplayer Online (Server necesar pe viitor).
*   **Structură:** Carduri numerotate. Adminul vede tot, userii free văd doar Worksheets.

## 5. MODULUL 3: POVEȘTI (STORIES)
**Fișier:** `gallery-stories.html`
*   **Clasificare:** Filtre de vârstă (3-5, 6-9, 10+).
*   **Conținut:** 100% Original (fără copyright extern).
*   **Mod Dual:**
    1.  **Read (Citesc):** Text afișat curat.
    2.  **Listen (Ascult):** Narator AI (Text-to-Speech).
*   **Inteligență Lingvistică:**
    *   Textul poveștii se schimbă automat în funcție de limba aplicației.
    *   Naratorul AI vorbește automat limba textului (ex: Text Italian -> Voce Italiană).

## 6. REGULI DE AUR PENTRU DEZVOLTARE VIITOARE
1.  **Prioritate Zero:** Niciodată nu încălcați drepturile de autor. Folosiți doar conținut generat sau licențiat.
2.  **Numerotare:** Păstrați întotdeauna vizibil numărul slotului (colț stânga sus) în toate galeriile.
3.  **Acces:** Verificați mereu flag-ul `isAdmin` înainte de a randa conținutul marcat `premium: true`.
4.  **Simplitate:** Codul trebuie să rămână curat, comentat și ușor de înțeles pentru mentenanță.

## 7. JURNAL DE BORD & INSTRUCȚIUNI DE CONTINUITATE (PENTRU VIITORII AGENȚI AI)
*Acestă secțiune sumarizează contextul uman și deciziile strategice luate în sesiunea din 17 Decembrie 2025.*

### A. Tonul și Abordarea
*   **Persona:** Trebuie să vă comportați ca un **Profesor Universitar înțelept, dar cu căldura unui Bunic**. Explicațiile trebuie să fie riguroase, dar blânde și răbdătoare.
*   **Prioritate:** Siguranța codului și claritatea explicațiilor primează în fața vitezei.

### B. Decizii Strategice Cheie
1.  **"Fără Salvare" la Desene:** Am decis deliberat să nu implementăm un buton de "Save to Server" pentru desenele copiilor. Motivul este simplitatea și focalizarea pe moment (Zen). Desenul se printează sau se pierde.
2.  **Premium este Invizibil:** Utilizatorii care nu plătesc NU trebuie să vadă deloc conținutul Premium amestecat cu cel Free. Acesta este filtrat complet din cod (`if (!isAdmin && item.premium) return;`).
3.  **Automatizare Server-Side:** Toată structura actuală (arrays `config`) este un "placeholder" inteligent. În viitor, un script Python/Go de pe server va injecta aceste JSON-uri zilnic. Structura HTML nu trebuie să necesite modificări manuale.

### C. Atenționări Critice
*   **COPYRIGHT:** Este strict interzisă folosirea imaginilor sau textelor externe protejate. Tot ce am creat (Labirinturi, Povestea Robotului, Mandala) a fost generat AI pe loc. Orice conținut nou trebuie să respecte această regulă.
*   **Numerotarea Vizuală:** Utilizatorul ține foarte mult la **numerotarea clară a sloturilor** (1, 2, 3...). Aceasta ajută la organizarea mentală a "raftului" digital. Nu eliminați niciodată bulina cu numărul slotului.

### D. Următorii Pași Logici (Roadmap)
1.  **Backend:** Crearea acelui script care să genereze zilnic `drawingsConfig.json` și `gamesConfig.json`.
2.  **Multiplayer:** Implementarea unui server WebSocket pentru jocurile de Șah și Table.
3.  **Audio Pro:** Înlocuirea vocilor AI (Text-to-Speech) cu fișiere audio `.mp3` reale, înregistrate de actori, pentru secțiunea Premium.

### E. Actualizare Sesiune (Final înainte de Pauză)
*   **Landing Page (`index.html`):** Redesenat complet. Hero Section cu animație CSS, Buton "START ADVENTURE" gigant, Carduri Rapide (Draw, Play, Read) și Logo-ul AE centrat sub butonul de start.
*   **Promo Video (`promo_video.html`):** Textul final a fost modificat din "WWW.KIDSDIGITALHUB.COM" în "KIDSDIGITALHUB.COM" (fără www) pentru campania TikTok.
*   **Status:** Proiectul este stabil (v1.5.0) și pregătit pentru lansare.

---
*Document redactat de Antigravity AI - 17 Dec 2025*
