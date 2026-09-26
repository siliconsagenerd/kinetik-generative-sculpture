from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()

# This allows our future Vue frontend to talk to this Python backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/generate/{seed_text}")
def generate_kinetik_data(seed_text: str):
    """
    Takes a string (like a user's name or a mood) and converts it into
    a unique mathematical hash. We use that hash to generate colors and
    3D transformation values for our Three.js sculpture.
    """

    # Create a unique mathematical hash from the text
    hash_object = hashlib.md5(seed_text.encode())
    hex_hash = hash_object.hexdigest()

    # Extract pieces of the hash to create unique hex colors
    color_1 = f"#{hex_hash[0:6]}"
    color_2 = f"#{hex_hash[6:12]}"

    # Extract numbers to determine how fast the 3D object should spin
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