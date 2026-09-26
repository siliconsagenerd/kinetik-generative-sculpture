# K I N E T I K
**Procedural WebGL Architecture**

[LIVE DEPLOYMENT](https://kinetik-generative-sculpture.vercel.app)

---

## DE // Systemkonzept (Arbeitsprobe zeit:raum)
Kinetik demonstriert moderne Headless-Architektur durch die Verschmelzung von serverseitiger Logik und clientseitigem WebGL-Rendering. Ein FastAPI-Backend übersetzt Texteingaben deterministisch in physikalische Rotationsvektoren (MD5-Hashing). Das Vue-Frontend konsumiert diese API asynchron, verarbeitet Orbit-Controls sowie Raycasting-Interaktionen und rendert eine Three.js-Skulptur, deren visuelles Profil strikt an die Corporate Identity der zeit:raum Gruppe angepasst ist.

## EN // System Concept
Kinetik demonstrates modern headless architecture by merging server-side logic with client-side WebGL rendering. A FastAPI backend deterministically translates text inputs into physical rotation vectors via MD5 hashing. The Vue frontend asynchronously consumes this API, handles orbit controls and raycasting interactions, and renders a Three.js sculpture strictly aligned with the zeit:raum corporate identity.

---

## CORE STACK

**Frontend // Interface & WebGL**
- Framework: Vue 3 (Composition API), Vite
- Engine: Three.js (GLTFLoader, Raycaster, OrbitControls)
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