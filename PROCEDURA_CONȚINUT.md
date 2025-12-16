# 📝 PROCEDURĂ STANDARD OPERAȚIONALĂ (SOP): GENERARE CONȚINUT "KIDS HUB"

Această procedură descrie pașii exacți pentru a popula categoriile goale (Jocuri, Povești) cu conținut digital de înaltă calitate, folosind AI.

## 🎯 OBIECTIV
Umplerea secțiunilor "Games" și "Stories" cu câte:
- 3 Produse Gratuite (pentru tracțiune)
- 1 Produs Premium (pentru monetizare)

---

## 🔹 FAZA 1: CATEGORIA "STORIES" (POVEȘTI)

### Pasul 1.1: Generare Concept & Text
Pentru fiecare poveste, definim:
- **Titlu:** (ex: "Aventura Ursulețului Martin")
- **Temă:** Educațională / Morala
- **Format:** PDF Ilustrat (Simulat pentru început prin Copertă)

### Pasul 1.2: Generare Copertă (AI Vision)
Folosim prompt-uri specifice pentru stilul "Kids Book Cover":
- *Prompt:* "Children's book cover, cute [personaj], magical forest background, title text placeholder, vibrant colors, disney style."

### Pasul 1.3: Adăugare în Bază de Date
Se adaugă în `products_data.js` cu `category: 'Stories'`.

---

## 🔹 FAZA 2: CATEGORIA "GAMES" (JOCURI)

### Pasul 2.1: Tipuri de Jocuri Digitale
Deoarece suntem pe web, jocurile pot fi:
1.  **Printable Games:** Labirinturi, "Găsește Diferențele" (PDF).
2.  **Browser Games:** Link-uri către jocuri simple HTML5 (sau placeholder pentru viitor).

*Decizie:* Vom merge pe **Printable Games** (Labirinturi, Puzzle-uri pe hârtie) pentru început, fiind cel mai ușor de livrat și produs.

### Pasul 2.2: Generare Asset-uri
- *Prompt Labirint:* "Simple black and white maze for kids, vector style, cute animal at start and food at end."
- *Prompt Puzzle:* "Find the differences puzzle illustration, cartoon style."

### Pasul 2.3: Adăugare în Bază de Date
Se adaugă în `products_data.js` cu `category: 'Games'`.

---

## 🔹 FAZA 3: EXECUTARE TEHNICĂ (AUTOMATIZARE)

### Lista de Comenzi pentru AI (Operator):
1.  `generate_image` pentru 3 coperți de povești.
2.  `generate_image` pentru 3 jocuri tip "Printable" (Labirint/Puzzle).
3.  `replace_file_content` în `js/products_data.js` pentru a insera noile obiecte JSON.
4.  `git push` pentru Live Deploy.

---

## 📋 LISTA DE CONȚINUT PROPUS (PENTRU APROBARE)

### 📚 Povești (Stories):
1.  **FREE:** "Noapte Bună, Luna!" (Poveste de somn)
2.  **FREE:** "Dino Învață să Împartă" (Educațională)
3.  **FREE:** "Mica Sirenă la Școală" (Aventură)
4.  **PREMIUM:** "Colecția de Aur: 50 Povești Audio + PDF" 🔒

### 🧩 Jocuri (Games - Printables):
1.  **FREE:** "Ajută-l pe Iepuraș!" (Labirint simplu)
2.  **FREE:** "Detectivul din Junglă" (Găsește obiectele ascunse)
3.  **FREE:** "Sudoku cu Fructe" (Logică simplă)
4.  **PREMIUM:** "Activity Book Gigant (200 Pagini)" 🔒
