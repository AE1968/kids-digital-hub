# 🚨 LISTA DE URGENȚĂ: IMPLEMENTĂRI CRITICE RĂMASE
*Acest document detaliază funcționalitățile parțial implementate sau simulate care necesită dezvoltare backend urgentă pentru a transforma platforma într-un produs comercial sigur și scalabil.*

## 1. ☁️ STOCARE REALĂ (10TB) - CRITIC
*   **Status Actual:** Există doar secțiunea UI "Partners" pentru negociere. Fișierele sunt încă locale sau pe GitHub (limitat).
*   **De Implementat Urgent:**
    *   Conectare API Backblaze B2 sau AWS S3.
    *   Script de upload automat pentru videourile și desenele utilizatorilor.
    *   **CDN:** Configurare Cloudflare pentru livrarea rapidă a conținutului media (desene, jocuri).

## 2. 🔐 SECURITATE BACKEND ("CHILD-PROOF") - CRITIC
*   **Status Actual:** Toate permisiunile (Admin, Premium, Oră de culcare, Monede) sunt salvate în `localStorage`.
    *   *Risc:* Un copil inteligent poate da "Inspect Element" și șterge limita de timp sau își poate da monede infinite.
*   **De Implementat Urgent:**
    *   **Netlify Identity / Supabase:** Autentificare reală user/parolă criptată.
    *   **Validare Server-Side:** Verificarea orei și a monedelor să se facă pe server, nu doar în browser.

## 3. 💳 PLĂȚI REALE & VALIDARE AUTOMATĂ
*   **Status Actual:** Butoanele duc la PayPal de test sau linkuri statice. Flag-ul "Premium" este setat manual sau simulat.
*   **De Implementat Urgent:**
    *   **Webhook PayPal/Stripe:** Când părintele plătește, serverul trebuie să primească confirmarea și să activeze automat contul "Premium" în baza de date securizată.

## 4. 🎮 MULTIPLAYER WEBRTC (REAL-TIME)
*   **Status Actual:** Simulat prin parametri URL (`?mode=multi&opponent=Dad`). Nu există conexiune reală live între două dispozitive.
*   **De Implementat Urgent:**
    *   **PeerJS / Socket.io:** Implementare server de semnalizare pentru ca utilizatorii să se vadă și să joace *cu adevărat* în timp real, pe dispozitive diferite.

## 5. 🤖 AUTOMATIZARE ZILNICĂ (AI CONTENT)
*   **Status Actual:** Scriptul `daily_content_manager.py` este funcțional dar trebuie rulat manual de Adrian.
*   **De Implementat Urgent:**
    *   **GitHub Actions:** Configurare "Cron Job" care să ruleze scriptul în fiecare noapte la 4:00 AM, să genereze conținut nou și să facă Push automat pe site.

## 6. 📧 SISTEM DE NOTIFICĂRI
*   **Status Actual:** Inexistent.
*   **De Implementat Urgent:**
    *   Emailuri automate către părinți: "Raport Săptămânal - Ce a creat copilul tău".
    *   Alertă email dacă se încearcă accesarea site-ului după ora de culcare (opțional).

---
**RECOMANDARE PENTRU URMĂTOAREA SESIUNE:**
Începe cu **Punctul 5 (Automatizarea Zilnică)** pentru a asigura un site viu, care se schimbă singur, apoi treci la **Punctul 2 (Securitatea)**.
