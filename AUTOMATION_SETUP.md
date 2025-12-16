# 🤖 Automatizare Generare Produse - GitHub Actions

## 📋 Ce face acest sistem?

Acest sistem automatizat:
- ✅ Rulează **automat în fiecare zi la ora 11:00 AM** (ora României)
- ✅ Generează **5 produse noi** cu design-uri AI
- ✅ Le sincronizează automat cu **Printful**
- ✅ Actualizează **site-ul pe Netlify**
- ✅ Poate fi rulat și **manual** când vrei tu

## 🚀 Configurare (Pași simpli)

### Pasul 1: Creează un repository pe GitHub

1. Mergi pe [github.com](https://github.com) și loghează-te
2. Click pe "New repository" (butonul verde)
3. Nume repository: `kids-digital-hub`
4. Setează ca **Public** (pentru GitHub Actions gratuit)
5. Click "Create repository"

### Pasul 2: Încarcă codul pe GitHub

Rulează aceste comenzi în terminal:

```bash
# Inițializează git (dacă nu e deja)
git init

# Adaugă toate fișierele
git add .

# Creează primul commit
git commit -m "Initial commit - Kids Digital Hub"

# Conectează la repository-ul tău GitHub (înlocuiește USERNAME cu username-ul tău)
git remote add origin https://github.com/USERNAME/kids-digital-hub.git

# Încarcă codul
git branch -M main
git push -u origin main
```

### Pasul 3: Configurează Secretele (API Keys)

În repository-ul tău GitHub:

1. Click pe **Settings** (tab-ul de sus)
2. În meniul stâng, click pe **Secrets and variables** → **Actions**
3. Click pe **New repository secret**

Adaugă următoarele secrete (unul câte unul):

#### Secret 1: PRINTFUL_API_KEY
- **Name:** `PRINTFUL_API_KEY`
- **Value:** Cheia ta Printful API (din Printful Dashboard → Settings → API)

#### Secret 2: GOOGLE_AI_API_KEY
- **Name:** `GOOGLE_AI_API_KEY`
- **Value:** Cheia ta Google AI API (din Google AI Studio)

#### Secret 3: NETLIFY_AUTH_TOKEN
- **Name:** `NETLIFY_AUTH_TOKEN`
- **Value:** Token-ul Netlify (vezi mai jos cum îl obții)

#### Secret 4: NETLIFY_SITE_ID
- **Name:** `NETLIFY_SITE_ID`
- **Value:** ID-ul site-ului tău Netlify (vezi mai jos)

### Cum obții NETLIFY_AUTH_TOKEN:

1. Mergi pe [app.netlify.com](https://app.netlify.com)
2. Click pe avatar-ul tău (dreapta sus) → **User settings**
3. Click pe **Applications** în meniul stâng
4. Scroll până la **Personal access tokens**
5. Click **New access token**
6. Nume: `GitHub Actions`
7. Copiază token-ul generat (ATENȚIE: apare o singură dată!)

### Cum obții NETLIFY_SITE_ID:

1. Mergi pe [app.netlify.com](https://app.netlify.com)
2. Click pe site-ul tău (`friendly-sawine-0d5dd4`)
3. Click pe **Site settings**
4. Copiază **Site ID** (sub numele site-ului)

## ✅ Testare

### Rulare manuală (pentru test):

1. În repository-ul GitHub, mergi la tab-ul **Actions**
2. Click pe workflow-ul **Daily Product Generation**
3. Click pe **Run workflow** (butonul albastru)
4. Alege câte produse vrei să generezi (default: 5)
5. Click **Run workflow**

### Monitorizare:

- Poți vedea progresul în timp real în tab-ul **Actions**
- Vei primi email dacă ceva nu merge
- Log-urile complete sunt disponibile pentru debugging

## 📅 Programare automată

Workflow-ul este configurat să ruleze automat:
- **Când:** În fiecare zi la **09:00 UTC** (11:00 AM ora României)
- **Ce face:** Generează 5 produse noi și le sincronizează

### Modificare programare:

Editează fișierul `.github/workflows/daily-product-generation.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Zilnic la 09:00 UTC
  # Exemple:
  # - cron: '0 */6 * * *'  # La fiecare 6 ore
  # - cron: '0 9 * * 1'    # Doar Luni la 09:00
  # - cron: '0 9 * * 1,3,5' # Luni, Miercuri, Vineri la 09:00
```

## 🎨 Personalizare

### Schimbă numărul de produse generate:

Editează `generate_demo_products.py` și modifică:
```python
NUM_PRODUCTS = 5  # Schimbă cu câte vrei
```

### Adaugă notificări:

Poți adăuga notificări prin:
- **Email** (GitHub trimite automat)
- **Slack** (adaugă webhook)
- **Discord** (adaugă webhook)
- **Telegram** (adaugă bot token)

## 💰 Costuri

- **GitHub Actions:** GRATUIT (2000 minute/lună pentru repository-uri publice)
- **Netlify:** GRATUIT (plan actual)
- **Printful:** Plătești doar când vinzi produse
- **Google AI API:** GRATUIT (până la limita lunară)

**Total cost lunar: $0** (până când începi să vinzi) 🎉

## 🔧 Troubleshooting

### Workflow-ul nu rulează:
- Verifică că repository-ul este **public**
- Verifică că toate secretele sunt configurate corect
- Verifică log-urile în tab-ul Actions

### Produsele nu apar pe Printful:
- Verifică `PRINTFUL_API_KEY` în Secrets
- Verifică log-urile pentru erori API
- Asigură-te că ai permisiuni de scriere în Printful

### Site-ul nu se actualizează:
- Verifică `NETLIFY_AUTH_TOKEN` și `NETLIFY_SITE_ID`
- Verifică că token-ul are permisiuni de deploy

## 📞 Suport

Dacă întâmpini probleme:
1. Verifică log-urile în GitHub Actions
2. Verifică că toate secretele sunt configurate
3. Testează script-urile local mai întâi

---

**Succes! 🚀 Acum ai un sistem complet automatizat care lucrează pentru tine 24/7!**
