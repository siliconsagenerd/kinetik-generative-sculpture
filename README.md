# KINETIK // Procedural WebGL Sculpture & Headless Architecture

> **Live Demo:** [View Live Deployment](https://your-vercel-link.vercel.app)
> *Developed as a technical work sample for the Working Student Web Development position at zeit:raum.*

---

## 🇩🇪 Projektübersicht
**Kinetik** ist eine experimentelle Full-Stack-Webapplikation an der Schnittstelle von generativem Design, WebGL und modernen Software-Architekturen. Das Projekt wurde konzipiert, um zu demonstrieren, wie kreatives Frontend-Design und robuste Backend-Logik in einer entkoppelten (decoupled) Umgebung zusammenarbeiten.

### Kernkonzept
Das System fungiert als algorithmische Brücke zwischen Sprache und visuellem 3D-Raum:
1. **Das Backend (Die Logik):** Ein FastAPI-Server nimmt beliebige Texteingaben entgegen und verarbeitet sie über einen deterministischen MD5-Kryptografie-Algorithmus. Dieser leitet konsistente Physikparameter (Rotationsgeschwindigkeiten) und Farbpaletten ab.
2. **Das Frontend (Die Visualisierung):** Eine Vue 3 Single-Page-Application konsumiert die REST-API asynchron, steuert den Anwendungs-State und mappt die generierten Daten in Echtzeit auf die PBR-Materialien eines externen CGI-Assets (`.glb`) mittels Three.js.

---

## 🇬🇧 Project Overview
**Kinetik** is an experimental full-stack web application bridging generative design, WebGL, and modern system architecture. Built as a work sample, it showcases the seamless integration of creative frontend execution with a decoupled backend pipeline.

### Core Architecture
* **Headless API Pipeline:** A Python backend acts as an algorithmic engine, translating text strings into deterministic color and physics states via cryptographic hashing.
* **Real-time WebGL Rendering:** A Vue 3 frontend handles asynchronous state synchronization, binding live API data to custom lighting setups and PBR-shaded 3D assets (`.glb`).

---

## 🏗 Tech Stack

* **Frontend:** Vue 3 (Composition API), Vite, Three.js (WebGL, GLTFLoader, ACESFilmicToneMapping), CSS3 (Backdrop-filters, Flexbox).
* **Backend:** Python 3, FastAPI, Uvicorn, hashlib (MD5).
* **DevOps / Architecture:** RESTful API design, CORS configuration, Git version control.

---

## ⚙️ Local Installation & Setup

To evaluate this codebase locally, you must run the Python backend and the Vite frontend concurrently in two separate terminal windows.

### Prerequisites
* Python 3.9 or higher
* Node.js & npm installed globally

---

### Step 1: Clone the Repository
Open your terminal and clone the project to your local machine:
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/kinetik-generative-sculpture.git](https://github.com/YOUR_GITHUB_USERNAME/kinetik-generative-sculpture.git)
cd kinetik-generative-sculpture

Step 2: Initialize and Start the Backend (API)
Open your first terminal window, navigate to the backend directory, set up a virtual environment, install dependencies, and launch the server:

Bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
The API will be active and listening at http://127.0.0.1:8000

Step 3: Initialize and Start the Frontend (Interface)
Open a second terminal window, navigate to the frontend directory, install the required packages (including Three.js), and start the development server:

Bash
cd frontend
npm install
npm run dev
The web interface will run locally at http://localhost:5173


### How to update your file:
1. Open PyCharm, click on your **`README.md`** file.
2. Delete everything inside it.
3. Paste the code block above, replace `YOUR_GITHUB_USERNAME` with your actual GitHub username, and save (`Cmd + S`).
4. Commit it to GitHub via your terminal (`git add README.md`, `git commit -m "Update professional bilingual README"`, `git push`).