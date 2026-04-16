# Wedding Photos App

App Streamlit per raccogliere e classificare le foto degli invitati al matrimonio.

## Stack
- **Frontend/Backend**: Streamlit
- **Storage foto**: Cloudflare R2 (free tier: 10GB, zero egress)
- **Database**: Supabase PostgreSQL (free tier)
- **Classificazione**: OpenAI CLIP via `open-clip-torch`
- **Deploy**: Railway o Render (free tier)

---

## Setup (15 minuti)

### 1. Supabase
1. Crea account su [supabase.com](https://supabase.com)
2. Nuovo progetto → copia `URL` e `anon key` da *Settings → API*
3. Vai su *SQL Editor* → incolla ed esegui `schema.sql`

### 2. Cloudflare R2
1. Crea account su [cloudflare.com](https://cloudflare.com)
2. Dashboard → R2 → *Create bucket* → nome `wedding-photos`
3. Abilita *Public Access* sul bucket → copia il dominio `pub-xxx.r2.dev`
4. *Manage R2 API Tokens* → crea token con permessi Read+Write → copia le credenziali
5. L'endpoint è `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`

### 3. Configurazione locale
```bash
git clone <repo>
cd wedding-photos

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edita .env con le tue credenziali
```

### 4. Avvio locale
```bash
streamlit run app.py
```

---

## Deploy su Railway

1. Crea account su [railway.app](https://railway.app)
2. *New Project → Deploy from GitHub repo*
3. Aggiungi tutte le variabili da `.env` in *Settings → Variables*
4. Railway rileva automaticamente Streamlit e fa il deploy

Costo stimato: **$0** sul free tier per uso occasionale (500 ore/mese).

> **Alternativa**: Render.com funziona in modo analogo e ha anch'esso free tier.

---

## Uso

### Giorno del matrimonio
- Stampa il QR code che punta all'URL del deploy
- Gli invitati scansionano → inseriscono la password da `GUEST_PASSWORD` → caricano foto

### Dopo il matrimonio
1. Accedi come Sposi con `ADMIN_PASSWORD`
2. Clicca **"Avvia classificazione CLIP"**
3. CLIP classifica ogni foto in: `cerimonia`, `cena`, `ricevimento`, `balli`, `altro`
4. Sfoglia la galleria filtrata per momento

---

## Struttura del progetto

```
wedding-photos/
├── app.py                      # Entry point, routing e autenticazione
├── pages/
│   ├── upload.py               # Pagina invitati: caricamento foto
│   └── gallery.py              # Pagina admin: galleria + trigger CLIP
├── pipeline/
│   ├── clip_classifier.py      # CLIP zero-shot classification
│   └── storage.py              # Wrapper R2 + Supabase
├── schema.sql                  # Schema PostgreSQL per Supabase
├── requirements.txt
└── .env.example
```

---

## Momenti riconosciuti da CLIP

| Label | Descrizione |
|-------|-------------|
| `cerimonia` | Scambi di voti, altare, chiesa |
| `cena` | Tavoli apparecchiati, banchetto |
| `ricevimento` | Aperitivo, cocktail, socializing |
| `balli` | Pista da ballo, primo ballo |
| `altro` | Candid, backstage, varie |

La classificazione è **zero-shot**: CLIP non richiede addestramento,
confronta direttamente l'immagine con descrizioni testuali dei momenti.
Per migliorare l'accuratezza puoi usare `ViT-L-14` (impostando `CLIP_MODEL` nel `.env`).
