# K I N E T I K
**Procedural WebGL Architecture**

[LIVE DEPLOYMENT](https://kinetik-generative-sculpture.vercel.app)

---

## DE // Systemkonzept (Arbeitsprobe zeit:raum)
Kinetik demonstriert moderne Headless-Architektur durch die Verschmelzung von serverseitiger Kryptografie und clientseitigem WebGL-Rendering. Ein FastAPI-Backend übersetzt Texteingaben deterministisch in Vektordaten (MD5-Hashing). Das Vue-Frontend konsumiert diese API asynchron und berechnet in Echtzeit physikalische Rotationswerte und PBR-Materialeigenschaften für eine Three.js-Skulptur.

## EN // System Concept
Kinetik demonstrates modern headless architecture by merging server-side cryptography with client-side WebGL rendering. A FastAPI backend deterministically translates text inputs into vector data via MD5 hashing. The Vue frontend asynchronously consumes this API, calculating real-time physical rotation values and PBR material properties for a Three.js sculpture.

---

## CORE STACK

**Frontend // Interface & WebGL**
- Framework: Vue 3 (Composition API), Vite
- Engine: Three.js (GLTFLoader, ACESFilmicToneMapping)
- UI: Native CSS3 (Flexbox, Backdrop-filters)

**Backend // Algorithmic Processing**
- Framework: Python 3, FastAPI, Uvicorn
- Logic: hashlib (MD5 Deterministic Generation)
- Network: REST API, strict CORS Middleware

---

## LOCAL INITIALIZATION

Execute backend and frontend concurrently in isolated terminal instances.

### 01. Backend Server

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload

# Target API URL: 127.0.0.1:8000
```
### 02. Frontend Interface

```bash
cd frontend
npm install
npm run dev

# Target Interface URL: localhost:5173
```