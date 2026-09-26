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

    color_1 = f"#{hex_hash[0:6]}"
    color_2 = f"#{hex_hash[6:12]}"

    rotation_speed_x = int(hex_hash[12:14], 16) / 255.0
    rotation_speed_y = int(hex_hash[14:16], 16) / 255.0

    return {
        "concept": seed_text,
        "aesthetics": {
            "primary_color": color_1,
            "secondary_color": color_2
        },
        "physics": {
            "speed_x": round(rotation_speed_x, 3),
            "speed_y": round(rotation_speed_y, 3)
        }
    }