<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const seedText = ref('zeitraum');
const isGenerating = ref(false);

let scene, camera, renderer, sceneGroup, modelGroup, animationId, controls;
let currentSpeedX = 0.005;
let currentSpeedY = 0.005;

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let baseScale = 1;
let isPulsing = false;
let pulseTimer = 0;

const onMouseClick = (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  if (modelGroup) {
    const intersects = raycaster.intersectObject(modelGroup, true);
    if (intersects.length > 0 && !isPulsing) {
      isPulsing = true;
      pulseTimer = 0;
    }
  }
};

const generateArt = async () => {
  if (!seedText.value) return;
  isGenerating.value = true;

  try {
    const response = await fetch(`https://kinetik-generative-sculpture.vercel.app/generate/${seedText.value}`);
    const data = await response.json();

    if (modelGroup) {
      // Color overrides disabled to maintain agency brand consistency
      currentSpeedX = data.physics.speed_x * 0.1;
      currentSpeedY = data.physics.speed_y * 0.1;
    }
  } catch (error) {
    console.error("API error:", error);
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

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enableZoom = true;
  controls.minDistance = 3;
  controls.maxDistance = 10;
  controls.enablePan = false;

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
  directionalLight.position.set(5, 5, 5);
  scene.add(directionalLight);

  const fillLight = new THREE.DirectionalLight(0xffffff, 1);
  fillLight.position.set(-5, 0, -5);
  scene.add(fillLight);

  sceneGroup = new THREE.Group();
  scene.add(sceneGroup);

  modelGroup = new THREE.Group();
  sceneGroup.add(modelGroup);

  const loader = new GLTFLoader();

  loader.load('/model.glb', (gltf) => {
    const loadedModel = gltf.scene;

    loadedModel.traverse((child) => {
      if (child.isMesh) {
        child.material = new THREE.MeshStandardMaterial({
          color: 0xA87BFA,
          metalness: 0.6,
          roughness: 0.2,
          envMapIntensity: 1.0
        });
      }
    });

    const box = new THREE.Box3().setFromObject(loadedModel);
    const center = box.getCenter(new THREE.Vector3());
    loadedModel.position.sub(center);

    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    baseScale = 3 / maxDim;
    loadedModel.scale.set(baseScale, baseScale, baseScale);

    modelGroup.add(loadedModel);
    generateArt();
  });

  const animate = () => {
    animationId = requestAnimationFrame(animate);

    controls.update();

    if (modelGroup) {
      modelGroup.rotation.x += currentSpeedX;
      modelGroup.rotation.y += currentSpeedY;

      if (isPulsing) {
        pulseTimer += 0.15;
        const pulseScale = baseScale + Math.sin(pulseTimer) * (baseScale * 0.2);
        modelGroup.children[0].scale.set(pulseScale, pulseScale, pulseScale);

        if (pulseTimer > Math.PI) {
          isPulsing = false;
          modelGroup.children[0].scale.set(baseScale, baseScale, baseScale);
        }
      }
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
  window.addEventListener('click', onMouseClick);
});

onUnmounted(() => {
  cancelAnimationFrame(animationId);
  window.removeEventListener('resize', handleResize);
  window.removeEventListener('click', onMouseClick);
  if (controls) controls.dispose();
  renderer.dispose();
});
</script>

<template>
  <div id="webgl-container"></div>

  <main class="ui-overlay">
    <h1>Kinetik<br><span class="accent">Architecture</span></h1>
    <p>Procedural WebGL Sculpture</p>

    <div class="input-group">
      <input
        v-model="seedText"
        @keyup.enter="generateArt"
        type="text"
        placeholder="Enter parameter..."
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
  background-color: #050505;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
  color: #ffffff;
  pointer-events: auto;
}
h1 {
  font-size: 5rem;
  line-height: 1.1;
  margin: 0 0 1rem 0;
  letter-spacing: -0.04em;
  font-weight: 700;
}
.accent {
  color: #A87BFA;
}
p {
  color: #a0a0a0;
  margin-bottom: 2.5rem;
  letter-spacing: 0.05em;
  font-size: 1rem;
  font-weight: 400;
}
.input-group {
  display: flex;
  gap: 1rem;
}
input {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(168, 123, 250, 0.3);
  padding: 1rem 1.5rem;
  color: white;
  border-radius: 50px;
  font-size: 1rem;
  outline: none;
  backdrop-filter: blur(8px);
  transition: border-color 0.3s;
  min-width: 250px;
}
input:focus {
  border-color: #A87BFA;
}
button {
  background: #A87BFA;
  color: #000000;
  border: none;
  padding: 1rem 2rem;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  transition: transform 0.2s, background 0.2s;
}
button:hover {
  transform: scale(1.02);
  background: #b58dfa;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>