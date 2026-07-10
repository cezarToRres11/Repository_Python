import requests

BASE = "https://pokeapi.co/api/v2"


def buscar_pokemon(nome_ou_id):
    url = f"{BASE}/pokemon/{str(nome_ou_id).lower()}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {
        "id": data["id"],
        "nome": data["name"].capitalize(),
        "altura": data["height"],
        "peso": data["weight"],
        "tipos": [t["type"]["name"] for t in data["types"]],
        "imagem": data["sprites"]["front_default"],
    }
