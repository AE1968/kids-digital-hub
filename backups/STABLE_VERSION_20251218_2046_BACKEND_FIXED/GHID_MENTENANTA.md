# 📘 Ghid de Conectare și Mentenanță - Kids Digital Hub

## 1. ✅ Status și Link-uri
Aplicația este **ACTIVĂ** și funcționează corect pe serverele Railway.

*   **Pagina Principală:** [https://web-production-b215.up.railway.app](https://web-production-b215.up.railway.app)
*   **Panou Admin:** [https://web-production-b215.up.railway.app/admin](https://web-production-b215.up.railway.app/admin)
*   **Webhook URL (pentru Stripe/WooCommerce):** `https://web-production-b215.up.railway.app/webhook/order`

---

## 2. 🔄 Cum se fac Update-uri (Modificări)
Pentru a actualiza site-ul sau codul în viitor, **vă recomand să păstrați folderul local**. Fluxul de lucru este foarte simplu:

1.  Faceți modificările dorite în fișierele de pe calculatorul dvs.
2.  Deschideți terminalul în folderul proiectului.
3.  Rulați comenzile de sincronizare cu GitHub:
    ```bash
    git add .
    git commit -m "Descrierea modificarii"
    git push origin main
    ```
4.  **Railway va detecta automat** noile fișiere și va actualiza site-ul live (durează 1-2 minute).

> **Notă:** Dacă ștergeți folderul local, va trebui să îl descărcați din nou (`git clone ...`) pentru a putea face modificări ușor.

---

## 3. 📦 Arhivă de Siguranță
Deși codul este salvat și pe GitHub, am creat o arhivă completă a versiunii curente de pe calculatorul dumneavoastră, așa cum ați solicitat.

*   **Locație Arhivă:** `C:\Users\adria\.gemini\antigravity\scratch\BACKUP\kids-digital-hub_backup_2025_12_17.zip`

Puteți muta această arhivă pe un stick USB sau în cloud pentru păstrare pe termen lung.

---

## 4. 🛠️ Verificare Funcționalitate
Am testat sistemul înainte de a scrie acest ghid:
*   ✅ Conexiunea la server: Activă.
*   ✅ Panoul de Admin: Accesibil.
*   ✅ Setările de Mediu (API Keys): Configurate corect.
*   ✅ Versiunea Python: 3.11.6 (Corectată).

Totul este pregătit pentru utilizare! 🚀
