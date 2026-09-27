from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()

allowed_origins = [
    "https://kinetik-generative-sculpture.vercel.app",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate/{seed_text}")
def generate_kinetik_data(seed_text: str):
    hash_object = hashlib.md5(seed_text.encode())
    hex_hash = hash_object.hexdigest()
    
    # 0:6 and 6:12 bypassed to maintain hardcoded Corporate Identity colors.
    # Deterministic mapping shifted to material physics.
    
    rotation_speed_x = int(hex_hash[12:14], 16) / 255.0
    rotation_speed_y = int(hex_hash[14:16], 16) / 255.0
    
    metalness_val = int(hex_hash[16:18], 16) / 255.0
    roughness_val = int(hex_hash[18:20], 16) / 255.0
    
    # 15% probability of wireframe topology based on hash slice
    wireframe_probability = int(hex_hash[20:22], 16) / 255.0
    is_wireframe = wireframe_probability > 0.85

    return {
        "concept": seed_text,
        "hash_signature": hex_hash,
        "physics": {
            "speed_x": round(rotation_speed_x, 3),
            "speed_y": round(rotation_speed_y, 3)
        },
        "material": {
            "metalness": round(metalness_val, 3),
            "roughness": round(roughness_val, 3),
            "wireframe": is_wireframe
        }
    }
