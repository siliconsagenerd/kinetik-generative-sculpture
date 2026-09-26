# KINETIK // Procedural WebGL Sculpture

> **Live Demo:** [Link to your Vercel/Render deployment will go here]

## 🇩🇪 Über das Projekt (Arbeitsprobe zeit:raum)
Kinetik ist ein experimentelles Full-Stack-Projekt, das als Arbeitsprobe für die Position als **Werkstudent Web Development** bei der zeit:raum Gruppe entwickelt wurde.

Anstatt einer statischen Webseite demonstriert dieses Projekt eine **entkoppelte (decoupled) Architektur**, wie sie in modernen Headless-CMS-Umgebungen zum Einsatz kommt. Ein Python-Backend fungiert als algorithmisches "Gehirn", das Texteingaben kryptografisch hasht und deterministische Physik- sowie Farbwerte generiert. Das Vue.js-Frontend konsumiert diese REST-API asynchron und übersetzt die Daten in eine interaktive, echtzeitgerenderte 3D-Skulptur mit PBR-Materialien.

**Warum dieser Stack?**
* **Vue 3:** Reagiert auf User-State und asynchrone Datenabfragen (State Management).
* **Three.js:** Beweist den Umgang mit WebGL, Studio-Beleuchtung (Directional/Ambient) und dem Laden externer CGI-Assets (`.glb`).
* **Python (FastAPI):** Simuliert die Funktionalität eines Headless-Backends und trennt schwere Logik strikt vom DOM.

---

## 🇬🇧 About the Project
Kinetik is an experimental full-stack project developed as a work sample for the **Working Student Web Development** position at zeit:raum.

Instead of a standard static page, this project demonstrates a **decoupled architecture** typical of modern headless CMS pipelines. A Python backend serves as the algorithmic "brain," taking text input and using cryptographic hashing to generate deterministic physics and hex color values. The Vue.js frontend asynchronously consumes this REST API and maps the data onto an interactive, real-time 3D sculpture using PBR materials.

---

## 🏗 Tech Stack & Architecture

**Frontend Layer:**
* Framework: Vue 3 (Composition API)
* Build Tool: Vite
* 3D Engine: Three.js (WebGL, GLTFLoader, ACESFilmicToneMapping)
* Styling: Native CSS3 (Responsive, Backdrop-filters)

**Backend Layer (API):**
* Environment: Python 3
* Framework: FastAPI
* Server: Uvicorn
* Logic: MD5 Cryptographic Hashing for deterministic procedural generation

---

## 🚀 Local Setup

**1. Start the API (Brain)**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload