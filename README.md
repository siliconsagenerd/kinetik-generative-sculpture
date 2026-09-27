# K I N E T I K – Procedural WebGL Sculpture System

[Deutsch](#deutsch) | [English](#english)

---

## English

### Overview

Kinetik is a deterministic procedural art system that bridges server-side algorithmic generation with real-time WebGL rendering. A FastAPI backend translates text seeds into Physically Based Rendering (PBR) material physics via MD5 hashing—extracting metalness, roughness, and topology data. The Vue 3 frontend consumes this API asynchronously, renders an interactive Three.js sculpture, and exposes material properties and physics vectors via a live telemetry HUD. Built for portfolio demonstration and architectural clarity.

**Live Deployment:** [kinetik-generative-sculpture.vercel.app](https://kinetik-generative-sculpture.vercel.app)

### Tech Stack

**Backend:**
- FastAPI (Python 3.10)
- hashlib (MD5 deterministic generation)
- CORS middleware
- REST API architecture

**Frontend:**
- Vue 3 (Composition API)
- Three.js (GLTFLoader, OrbitControls, Raycaster)
- Vite (build tooling)
- CSS3 (Flexbox, backdrop filters, responsive layout)

**Infrastructure:**
- Vercel (frontend deployment, SPA routing)
- Uvicorn (backend development server)
- Docker & Docker Compose (containerized local development)

### Installation & Setup

#### Prerequisites
- Node.js 18+ & npm
- Python 3.10+
- Docker & Docker Compose (optional, for containerized workflow)

#### Quick Start (Local Development)

**Option 1: Manual Setup**

1. Clone/download the project
   ```bash
   cd Kinetik
   ```

2. Backend initialization
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Backend runs at `http://localhost:8000`

3. Frontend initialization (new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs at `http://localhost:5173`

4. Access the application
   - Interface: `http://localhost:5173`
   - Backend: `http://localhost:8000`

**Option 2: Docker Compose**

```bash
docker compose up --build
```
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

### Project Structure

```
Kinetik/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── style.css
│   │   └── index.html
│   ├── public/
│   │   └── model.glb
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── serve.json
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

### API Endpoints

| Method | Endpoint | Input | Output | Description |
|--------|----------|-------|--------|-------------|
| GET | `/generate/{seed_text}` | `seed_text` (string) | JSON payload | Deterministic PBR generation from MD5 hash |

#### Response Structure

```json
{
  "concept": "zeitraum",
  "hash_signature": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "physics": {
    "speed_x": 0.667,
    "speed_y": 0.392
  },
  "material": {
    "metalness": 0.824,
    "roughness": 0.451,
    "wireframe": false
  }
}
```

#### Hash Mapping Logic

The MD5 hash is sliced deterministically to extract material physics:

| Hash Slice | Range | Target Property | Formula |
|------------|-------|-----------------|---------|
| `[12:14]` | 2 hex chars | `physics.speed_x` | `int(hex, 16) / 255.0` |
| `[14:16]` | 2 hex chars | `physics.speed_y` | `int(hex, 16) / 255.0` |
| `[16:18]` | 2 hex chars | `material.metalness` | `int(hex, 16) / 255.0` |
| `[18:20]` | 2 hex chars | `material.roughness` | `int(hex, 16) / 255.0` |
| `[20:22]` | 2 hex chars | `material.wireframe` | `value > 0.85 → true` (15% probability) |

#### Example Request

```bash
curl http://localhost:8000/generate/kinetik
```

#### Example Response

```json
{
  "concept": "kinetik",
  "hash_signature": "3e9c2f1a8b7d4c6e5a2b9f1d3c8a7e4b",
  "physics": {
    "speed_x": 0.545,
    "speed_y": 0.733
  },
  "material": {
    "metalness": 0.212,
    "roughness": 0.667,
    "wireframe": true
  }
}
```

### Telemetry HUD

The frontend renders a live telemetry overlay (bottom-right) displaying real-time material and physics data:

```
MD5 SIG: a1b2c3d4e5f6...
MTL: 0.824 RGH: 0.451
ROT_X: 0.054 ROT_Y: 0.039
TOPOLOGY: SOLID_SURFACE
```

- **MTL (Metalness):** 0.0–1.0 (0 = matte, 1 = mirror-like)
- **RGH (Roughness):** 0.0–1.0 (0 = polished, 1 = diffuse)
- **ROT_X, ROT_Y:** Rotation speed vectors in radians/frame
- **TOPOLOGY:** `SOLID_SURFACE` (standard mesh) or `WIREFRAME` (edge-only rendering)

### Development

#### Adding a Feature

1. **Backend endpoint** – Modify `backend/main.py`, add Pydantic validation if needed
2. **Hash mapping** – Update slice indices in `/generate/{seed_text}` to extract new properties
3. **Frontend consumption** – Update `frontend/src/App.vue` to read and apply new material properties via Three.js traversal
4. **Test via browser** – Navigate to `http://localhost:5173`, enter seed text, observe telemetry HUD

#### Testing the API

```bash
# Direct endpoint test
curl http://localhost:8000/generate/test-seed

# With verbose output
curl -v http://localhost:8000/generate/my-concept
```

#### Hot Reload

Both backend and frontend support hot reload during development:

- **Backend:** Uvicorn reloads on `main.py` changes (`--reload` flag)
- **Frontend:** Vite hot-module replacement (HMR) on `.vue` and `.css` changes

### Performance Considerations

**WebGL Rendering:**
- **Frame rate:** Target 60 FPS via `requestAnimationFrame` loop
- **Tone mapping:** ACESFilmicToneMapping applied for cinematic color grading
- **Draw calls:** Single GLB model with material traversal (no instancing)
- **Raycasting:** Click-to-pulse interaction uses Three.js Raycaster with negligible overhead

**Three.js Memory Footprint:**
- Model geometry buffering: ~2–5 MB (depends on GLB complexity)
- Texture atlasing: Not used; materials are procedural (metalness/roughness)
- Camera/light setup: 3 lights (1 ambient, 2 directional) with minimal overhead

**API Latency:**
- MD5 hash computation: <1 ms
- CORS middleware: <1 ms
- Network round-trip (local): ~5–10 ms
- Network round-trip (production): ~50–200 ms depending on Vercel edge location

**Optimization Wins:**
- No texture downloads (purely procedural materials)
- Single-model architecture (no asset loading after init)
- Efficient Material instantiation (Three.js MeshStandardMaterial pooling)

### Configuration

**Environment Variables:**

Backend `.env` (optional, currently none required):
```
# No secrets or API keys needed
```

**CORS Configuration:**

Backend allows requests from:
```
https://kinetik-generative-sculpture.vercel.app
http://localhost:5173
```

Modify in `backend/main.py` if deploying to new domains.

**Docker Compose Config:**
- Backend service: `http://localhost:8000`
- Frontend service: `http://localhost:5173`
- Network: `kinetik-network` (bridge)
- Volumes: None (stateless design)

### Deployment

**Current Setup (Portfolio):**
- Frontend: Vercel (automatic SPA routing via `vercel.json`)
- Backend: Local/development only (not currently deployed)

**To Deploy Backend to Production:**

1. Choose hosting (Heroku, Railway, Fly.io, AWS Lambda)
2. Update CORS origins in `backend/main.py`
3. Pin Python version in `requirements.txt`
4. Use gunicorn instead of Uvicorn:
   ```bash
   pip install gunicorn
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```
5. Set backend URL in frontend API calls (currently hardcoded to `https://kinetik-generative-sculpture.vercel.app/generate/...`)

**CI/CD Pipeline (Recommended):**
- GitHub Actions: Auto-deploy frontend to Vercel on push
- Manual backend deployment until traffic justifies hosting cost

### Known Limitations

- **Single model asset:** Only one GLB model rendered; no multi-model support
- **Hash space exhaustion:** MD5 is cryptographically broken; use SHA-256 for production
- **Determinism caveat:** Same seed always produces identical physics/material; no randomization
- **Wireframe opacity:** Wireframe mode renders all edges; no selective topology masking
- **Raycasting simplicity:** Click detection is AABB-based; no per-polygon collision
- **Backend scalability:** Single FastAPI instance; no horizontal scaling without load balancer
- **Material precision:** Metalness/roughness limited to 255 discrete levels (0.0–1.0 mapped to hex pairs)
- **German language support:** Documentation is English-primary; German expansion pending

### Error Handling

**Frontend:**
- Invalid seed text (empty string) → Button disabled, no API call
- Network failure → Console error logged; UI remains static

**Backend:**
- Malformed request → FastAPI returns 422 Unprocessable Entity
- Invalid seed characters → Handled gracefully by hashlib (accepts any UTF-8)

### Future Enhancements

- [ ] Implement SHA-256 hash for cryptographic stability
- [ ] Add batch `/generate` endpoint for multi-seed generation
- [ ] Support custom GLB model uploads
- [ ] Implement WebGL post-processing (bloom, DoF, motion blur)
- [ ] Add WebSocket telemetry streaming for real-time metrics
- [ ] Deploy backend to Railway or Fly.io
- [ ] Expand German language documentation

---

## Deutsch

### Übersicht

Kinetik ist ein deterministisches prozedurales Kunstsystem, das serverseitige algorithmische Generierung mit echtzeitlichem WebGL-Rendering verbindet. Ein FastAPI-Backend übersetzt Texteingaben in physikalisch basierte Rendering-Materialphysik (PBR) mittels MD5-Hashing – extrahiert Metallizität, Rauheit und Topologiedaten. Das Vue-3-Frontend konsumiert diese API asynchron, rendert eine interaktive Three.js-Skulptur und stellt Materialeigenschaften sowie Physik-Vektoren über ein Live-Telemetrie-HUD dar. Entwickelt für Portfolio-Demonstration und Architektur-Klarheit.

**Live-Deployment:** [kinetik-generative-sculpture.vercel.app](https://kinetik-generative-sculpture.vercel.app)

### Tech-Stack

**Backend:**
- FastAPI (Python 3.10)
- hashlib (MD5 deterministische Generierung)
- CORS Middleware
- REST-API-Architektur

**Frontend:**
- Vue 3 (Composition API)
- Three.js (GLTFLoader, OrbitControls, Raycaster)
- Vite (Build-Tooling)
- CSS3 (Flexbox, Backdrop-Filter, responsive Layout)

**Infrastruktur:**
- Vercel (Frontend-Deployment, SPA-Routing)
- Uvicorn (Backend-Entwicklungsserver)
- Docker & Docker Compose (containerisierte lokale Entwicklung)

### Installation & Setup

#### Voraussetzungen
- Node.js 18+ & npm
- Python 3.10+
- Docker & Docker Compose (optional, für containerisierten Workflow)

#### Schnellstart (Lokale Entwicklung)

**Option 1: Manuelle Einrichtung**

1. Projekt klonen/herunterladen
   ```bash
   cd Kinetik
   ```

2. Backend-Initialisierung
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   pip install fastapi uvicorn
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Backend läuft unter `http://localhost:8000`

3. Frontend-Initialisierung (neues Terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend läuft unter `http://localhost:5173`

4. Anwendung aufrufen
   - Interface: `http://localhost:5173`
   - Backend: `http://localhost:8000`

**Option 2: Docker Compose**

```bash
docker compose up --build
```
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

### Projektstruktur

```
Kinetik/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── style.css
│   │   └── index.html
│   ├── public/
│   │   └── model.glb
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── serve.json
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

### API-Endpoints

| Methode | Endpoint | Input | Output | Beschreibung |
|---------|----------|-------|--------|-------------|
| GET | `/generate/{seed_text}` | `seed_text` (String) | JSON-Payload | Deterministische PBR-Generierung aus MD5-Hash |

#### Response-Struktur

```json
{
  "concept": "zeitraum",
  "hash_signature": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "physics": {
    "speed_x": 0.667,
    "speed_y": 0.392
  },
  "material": {
    "metalness": 0.824,
    "roughness": 0.451,
    "wireframe": false
  }
}
```

#### Hash-Mapping-Logik

Der MD5-Hash wird deterministisch segmentiert, um Materialphysik zu extrahieren:

| Hash-Segment | Bereich | Ziel-Eigenschaft | Formel |
|--------------|---------|-----------------|---------|
| `[12:14]` | 2 Hex-Zeichen | `physics.speed_x` | `int(hex, 16) / 255.0` |
| `[14:16]` | 2 Hex-Zeichen | `physics.speed_y` | `int(hex, 16) / 255.0` |
| `[16:18]` | 2 Hex-Zeichen | `material.metalness` | `int(hex, 16) / 255.0` |
| `[18:20]` | 2 Hex-Zeichen | `material.roughness` | `int(hex, 16) / 255.0` |
| `[20:22]` | 2 Hex-Zeichen | `material.wireframe` | `Wert > 0.85 → wahr` (15% Wahrscheinlichkeit) |

#### Beispiel-Request

```bash
curl http://localhost:8000/generate/kinetik
```

#### Beispiel-Response

```json
{
  "concept": "kinetik",
  "hash_signature": "3e9c2f1a8b7d4c6e5a2b9f1d3c8a7e4b",
  "physics": {
    "speed_x": 0.545,
    "speed_y": 0.733
  },
  "material": {
    "metalness": 0.212,
    "roughness": 0.667,
    "wireframe": true
  }
}
```

### Telemetrie-HUD

Das Frontend rendert ein Live-Telemetrie-Overlay (unten rechts) mit Echtzeit-Material- und Physikdaten:

```
MD5 SIG: a1b2c3d4e5f6...
MTL: 0.824 RGH: 0.451
ROT_X: 0.054 ROT_Y: 0.039
TOPOLOGY: SOLID_SURFACE
```

- **MTL (Metallizität):** 0.0–1.0 (0 = matt, 1 = spiegelnd)
- **RGH (Rauheit):** 0.0–1.0 (0 = poliert, 1 = diffus)
- **ROT_X, ROT_Y:** Rotationsgeschwindigkeit-Vektoren in Radiant/Frame
- **TOPOLOGY:** `SOLID_SURFACE` (Standard-Mesh) oder `WIREFRAME` (nur Kanten-Rendering)

### Entwicklung

#### Feature hinzufügen

1. **Backend-Endpoint** – Modifiziere `backend/main.py`, füge Pydantic-Validierung bei Bedarf hinzu
2. **Hash-Mapping** – Aktualisiere Segmentindizes in `/generate/{seed_text}` zum Extrahieren neuer Eigenschaften
3. **Frontend-Konsumption** – Aktualisiere `frontend/src/App.vue`, um neue Materialeigenschaften via Three.js-Traversal zu lesen und anzuwenden
4. **Test im Browser** – Navigiere zu `http://localhost:5173`, gib Seed-Text ein, beobachte Telemetrie-HUD

#### API testen

```bash
# Direkter Endpoint-Test
curl http://localhost:8000/generate/test-seed

# Mit ausführlichem Output
curl -v http://localhost:8000/generate/mein-konzept
```

#### Hot Reload

Sowohl Backend als auch Frontend unterstützen Hot Reload während der Entwicklung:

- **Backend:** Uvicorn lädt bei `main.py`-Änderungen neu (`--reload`-Flag)
- **Frontend:** Vite Hot-Module-Replacement (HMR) bei `.vue`- und `.css`-Änderungen

### Leistungsaspekte

**WebGL-Rendering:**
- **Frame-Rate:** Ziel 60 FPS via `requestAnimationFrame`-Loop
- **Tone Mapping:** ACESFilmicToneMapping für filmische Farbkorrektur
- **Draw Calls:** Einzelnes GLB-Modell mit Material-Traversal (kein Instancing)
- **Raycasting:** Click-to-Pulse-Interaktion nutzt Three.js Raycaster mit vernachlässigbarem Overhead

**Three.js-Speicherfußabdruck:**
- Modell-Geometrie-Pufferung: ~2–5 MB (abhängig von GLB-Komplexität)
- Textur-Atlasing: Nicht verwendet; Materialien sind prozedural (Metallizität/Rauheit)
- Kamera/Licht-Setup: 3 Lichter (1 Ambient, 2 Directional) mit minimalem Overhead

**API-Latenz:**
- MD5-Hash-Berechnung: <1 ms
- CORS-Middleware: <1 ms
- Netzwerk-Roundtrip (lokal): ~5–10 ms
- Netzwerk-Roundtrip (Produktion): ~50–200 ms je nach Vercel-Edge-Location

**Optimierungsgewinne:**
- Keine Textur-Downloads (rein prozedurale Materialien)
- Single-Model-Architektur (kein Asset-Laden nach Initialisierung)
- Effiziente Material-Instanziierung (Three.js MeshStandardMaterial-Pooling)

### Konfiguration

**Umgebungsvariablen:**

Backend `.env` (optional, derzeit keine erforderlich):
```
# Keine Secrets oder API-Schlüssel erforderlich
```

**CORS-Konfiguration:**

Backend erlaubt Anfragen von:
```
https://kinetik-generative-sculpture.vercel.app
http://localhost:5173
```

Modifiziere in `backend/main.py` bei Deployment auf neue Domains.

**Docker Compose Konfiguration:**
- Backend-Service: `http://localhost:8000`
- Frontend-Service: `http://localhost:5173`
- Netzwerk: `kinetik-network` (bridge)
- Volumes: Keine (zustandsloses Design)

### Deployment

**Aktuelle Einrichtung (Portfolio):**
- Frontend: Vercel (automatisches SPA-Routing via `vercel.json`)
- Backend: Lokal/Entwicklung nur (derzeit nicht deployed)

**Backend in Produktion deployen:**

1. Hosting wählen (Heroku, Railway, Fly.io, AWS Lambda)
2. CORS-Origins in `backend/main.py` aktualisieren
3. Python-Version in `requirements.txt` fixieren
4. Gunicorn statt Uvicorn verwenden:
   ```bash
   pip install gunicorn
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```
5. Backend-URL in Frontend-API-Aufrufen setzen (derzeit hardcodiert auf `https://kinetik-generative-sculpture.vercel.app/generate/...`)

**CI/CD-Pipeline (Empfohlen):**
- GitHub Actions: Auto-Deploy Frontend zu Vercel bei Push
- Manuelles Backend-Deployment bis der Traffic Hosting-Kosten rechtfertigt

### Bekannte Einschränkungen

- **Single-Model-Asset:** Nur ein GLB-Modell gerendert; keine Multi-Model-Unterstützung
- **Hash-Raum-Erschöpfung:** MD5 ist kryptographisch gebrochen; nutze SHA-256 für Produktion
- **Determinismus-Caveat:** Gleicher Seed produziert immer identische Physik/Materialien; keine Randomisierung
- **Wireframe-Deckkraft:** Wireframe-Modus rendert alle Kanten; keine selektive Topologie-Maskierung
- **Raycasting-Einfachheit:** Click-Detection ist AABB-basiert; keine Pro-Polygon-Kollision
- **Backend-Skalierbarkeit:** Single FastAPI-Instanz; kein horizontales Skalieren ohne Load Balancer
- **Material-Präzision:** Metallizität/Rauheit begrenzt auf 255 diskrete Ebenen (0.0–1.0 auf Hex-Paare)
- **Deutschsprachige Unterstützung:** Dokumentation ist englisch-dominant; Deutsche Ausweitung ausstehend

### Fehlerbehandlung

**Frontend:**
- Ungültiger Seed-Text (leerer String) → Button deaktiviert, kein API-Call
- Netzwerkfehler → Fehler in Konsole geloggt; UI bleibt statisch

**Backend:**
- Malformierter Request → FastAPI gibt 422 Unprocessable Entity zurück
- Ungültige Seed-Zeichen → Gracefully von hashlib verarbeitet (akzeptiert jedes UTF-8)

### Zukünftige Verbesserungen

- [ ] SHA-256-Hash für kryptographische Stabilität implementieren
- [ ] Batch-`/generate`-Endpoint für Multi-Seed-Generierung hinzufügen
- [ ] Unterstützung für benutzerdefinierte GLB-Modell-Uploads
- [ ] WebGL-Post-Processing implementieren (Bloom, DoF, Motion Blur)
- [ ] WebSocket-Telemetrie-Streaming für Echtzeit-Metriken hinzufügen
- [ ] Backend zu Railway oder Fly.io deployen
- [ ] Deutsche Sprachdokumentation erweitern
