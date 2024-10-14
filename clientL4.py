#client.py

import requests
from api_models import Character


char = Character(
    name="none",
    height=1,
    mass=1,
    hair_color="none",
    skin_color="none",
    eye_color="none",
    birth_year=1.5,
    gender="not found",
    homeworld="space",
    species="speck"

)

requests.post("http://localhost:8000/characters", json=char.dict())