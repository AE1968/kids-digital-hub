# 🗓️ PLAN DE LUCRU: SESIUNEA URMĂTOARE (KDH 2.0)

Acest document servește ca "foaie de parcurs" pentru următoarea dată când lucrăm împreună.

## 🔴 PRIORITATE MAXIMĂ (CRITIC PENTRU BANII TĂI)
1.  **Activare PayPal Live:**
    *   Înlocuirea `client-id` și `plan_id` în `payment.html` cu cele reale din contul tău PayPal Business.
    *   Testarea unei tranzacții reale de 1 GBP.

2.  **Activare Cloud Storage (10TB):**
    *   Configurarea Backblaze B2 (sau AWS S3 / Netlify Blob).
    *   Adăugarea cheilor secrete în Netlify Environment Variables (nu în cod!).
    *   Conectarea `js/storage_manager.js` la acest backend real.

## 🟠 ÎMBUNĂTĂȚIRI FUNCȚIONALE (URGENT PENTRU USERI)
3.  **Bază de Date Reală (Fără LocalStorage):**
    *   Migrarea datelor utilizatorilor (monede, progres) din browser în **Supabase** (gratuit, SQL real).
    *   Asta va preveni ca un copil să șteargă istoricul browserului și să piardă tot progresul.

4.  **Notificări Părinți:**
    *   Implementarea unui serviciu de email real (SendGrid / EmailJS) pentru a trimite raportul săptămânal părinților.

## 🟡 MARKETING & RELAȚII (PENTRU CREȘTERE)
5.  **SEO & Analytics:**
    *   Adăugarea Google Analytics 4 pentru a vedea câți copii intră zilnic.
    *   Optimizare meta-tags pentru cuvinte cheie: "jocuri educative", "safe kids chat".

6.  **Video Promoțional:**
    *   Finalizarea și integrarea videoului de prezentare pe prima pagină (acum e un placeholder).

## ✅ GATA DE LANSARE?
*   Dacă rezolvăm Punctele 1 și 2, site-ul poate fi considerat **PRODUS FINAL** și lansat oficial către publicul larg.

---
*Acest fișier a fost generat automat la finalul sesiunii de dezvoltare.*
