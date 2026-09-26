<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const seedText = ref('zeitraum');
const isGenerating = ref(false);

let scene, camera, renderer, modelGroup, animationId;
let currentSpeedX = 0.005;
let currentSpeedY = 0.005;

const generateArt = async () => {
  if (!seedText.value) return;
  isGenerating.value = true;

  try {
    const response = await fetch(`http://127.0.0.1:8000/generate/${seedText.value}`);
    const data = await response.json();

    if (modelGroup) {
      modelGroup.traverse((child) => {
        if (child.isMesh) {
          child.material.color.set(data.aesthetics.primary_color);
        }
      });
      document.body.style.backgroundColor = data.aesthetics.secondary_color;
      currentSpeedX = data.physics.speed_x * 0.1;
      currentSpeedY = data.physics.speed_y * 0.1;
    }
  } catch (error) {
    console.error("Backend connection failed:", error);
  }
  isGenerating.value = false;
};

const initThreeJS = () => {
  const container = document.getElementById('webgl-container');

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 6;

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  container.appendChild(renderer.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
  directionalLight.position.set(5, 5, 5);
  scene.add(directionalLight);

  const fillLight = new THREE.DirectionalLight(0xffffff, 1);
  fillLight.position.set(-5, 0, -5);
  scene.add(fillLight);

  const loader = new GLTFLoader();
  modelGroup = new THREE.Group();
  scene.add(modelGroup);

  loader.load('/model.glb', (gltf) => {
    const loadedModel = gltf.scene;

    loadedModel.traverse((child) => {
      if (child.isMesh) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xffffff,
          metalness: 0.8,
          roughness: 0.2,
          envMapIntensity: 1.0
        });
      }
    });

    // Auto-center the model
    const box = new THREE.Box3().setFromObject(loadedModel);
    const center = box.getCenter(new THREE.Vector3());
    loadedModel.position.sub(center);

    // Auto-scale the model so it fits the screen properly
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const scale = 3 / maxDim;
    loadedModel.scale.set(scale, scale, scale);

    modelGroup.add(loadedModel);
    generateArt();
  });

  const animate = () => {
    animationId = requestAnimationFrame(animate);
    if (modelGroup) {
      modelGroup.rotation.x += currentSpeedX;
      modelGroup.rotation.y += currentSpeedY;
    }
    renderer.render(scene, camera);
  };
  animate();
};

const handleResize = () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
};

onMounted(() => {
  initThreeJS();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  cancelAnimationFrame(animationId);
  window.removeEventListener('resize', handleResize);
  renderer.dispose();
});
</script>

<template>
  <div id="webgl-container"></div>

  <main class="ui-overlay">
    <h1>Kinetik</h1>
    <p>Procedural WebGL Sculpture</p>

    <div class="input-group">
      <input
        v-model="seedText"
        @keyup.enter="generateArt"
        type="text"
        placeholder="Type a concept..."
      />
      <button @click="generateArt" :disabled="isGenerating">
        {{ isGenerating ? 'Computing...' : 'Synthesize' }}
      </button>
    </div>
  </main>
</template>

<style>
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  overflow: hidden;
  background-color: #0b0c10;
  font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
  transition: background-color 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}
#webgl-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1;
}
.ui-overlay {
  position: absolute;
  top: 50%;
  left: 10%;
  transform: translateY(-50%);
  z-index: 2;
  color: white;
  pointer-events: auto;
}
h1 {
  font-size: 4rem;
  margin: 0 0 0.2rem 0;
  letter-spacing: -0.04em;
}
p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 0.85rem;
}
.input-group {
  display: flex;
  gap: 1rem;
}
input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 1.5rem;
  color: white;
  border-radius: 6px;
  font-size: 1rem;
  outline: none;
  backdrop-filter: blur(8px);
  transition: border-color 0.3s;
}
input:focus {
  border-color: white;
}
button {
  background: white;
  color: black;
  border: none;
  padding: 1rem 2rem;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: transform 0.2s, background 0.2s;
}
button:hover {
  transform: scale(1.02);
  background: #f0f0f0;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>