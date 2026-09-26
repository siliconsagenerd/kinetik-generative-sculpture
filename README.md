# KINETIK // Procedural WebGL Sculpture & Headless Architecture

[LAUNCH LIVE DEPLOYMENT](https://kinetik-generative-sculpture.vercel.app)

---

## DE // Projektarchitektur (Arbeitsprobe zeit:raum)
Kinetik ist ein experimentelles System an der Schnittstelle von generativer Logik und WebGL-Rendering. Das Projekt implementiert eine entkoppelte Architektur zur Demonstration moderner Headless-Datenflüsse.

Ein Python-Backend fungiert als algorithmischer Prozessor. Texteingaben werden über MD5-Kryptografie in deterministische Physik- und Farbvektoren übersetzt. Eine asynchrone Vue 3-Applikation konsumiert diese REST-API und überführt die generierten Parameter in Echtzeit auf eine PBR-schattierte 3D-Skulptur.

## EN // System Architecture
Kinetik is an experimental system at the intersection of generative logic and WebGL rendering. The project implements a decoupled architecture to demonstrate modern headless data flows.

A Python backend acts as an algorithmic processor. Text inputs are translated via MD5 cryptography into deterministic physics and color vectors. An asynchronous Vue 3 application consumes this REST API, mapping the generated parameters in real-time onto a PBR-shaded 3D sculpture.

---

## Technical Stack

**Visual Interface (Frontend)**
* Framework: Vue 3 (Composition API), Vite
* WebGL Context: Three.js (GLTFLoader, ACESFilmicToneMapping)
* Styling: Native CSS3 (Flexbox, Backdrop-filters)

**Algorithmic Engine (Backend)**
* Framework: Python 3, FastAPI, Uvicorn
* Processing: hashlib (MD5 Deterministic Hashing)
* Architecture: RESTful API, CORS Middleware

---

## Local Execution Environment

Parallel execution of the backend and frontend is required.

### 1. Initialize API Server
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
Target: http://127.0.0.1:8000

### 1. Initialize Visual Interface
```bash
cd frontend
npm install
npm run dev
Target: http://localhost:5173