import os
import time
import csv 
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# .env laden
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("Fehlender API_KEY in Umgebungsvariablen")

BASE_URL = "https://api.exchangerate.host/convert"
CACHE_FILE = "cache.csv"
CACHE_TTL = 3600  # 60 Minuten

app = FastAPI(title="Währungsrechner mit CSV-Cache")

# -----------------------------
# Cache: Speicher im Speicher + CSV
# -----------------------------
CACHE: dict = {}

def get_cache_key(from_currency: str, to_currency: str, amount: float) -> str:
    return f"{from_currency.upper()}-{to_currency.upper()}-{amount}"

def load_cache():
    """Lädt vorhandene Cache-Einträge aus der CSV"""
    if not os.path.exists(CACHE_FILE):
        return
    with open(CACHE_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = get_cache_key(row["from"], row["to"], float(row["amount"]))
            CACHE[key] = {
                "timestamp": float(row["timestamp"]),
                "data": {
                    "from": row["from"],
                    "to": row["to"],
                    "amount": float(row["amount"]),
                    "result": float(row["result"]),
                    "info": {
                        "rate": float(row["rate"]) if row["rate"] not in (None, '', 'None') else None
                    }
                }
            }

def save_cache():
    """Schreibt den Cache in die CSV-Datei"""
    with open(CACHE_FILE, mode="w", newline="") as f:
        fieldnames = ["from", "to", "amount", "result", "rate", "timestamp"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in CACHE.values():
            data = entry["data"]
            writer.writerow({
                "from": data["from"],
                "to": data["to"],
                "amount": data["amount"],
                "result": data["result"],
                "rate": data["info"].get("rate", None),  # <-- Fix here
                "timestamp": entry["timestamp"]
            })

def get_cache(key: str):
    item = CACHE.get(key)
    if item:
        if time.time() - item["timestamp"] < CACHE_TTL:
            return item["data"]
        else:
            del CACHE[key]
            save_cache()
    return None

def set_cache(key: str, value: dict):
    CACHE[key] = {"timestamp": time.time(), "data": value}
    save_cache()

# Lade Cache beim Start
load_cache()

# -----------------------------
# API-Endpunkt
# -----------------------------
@app.get("/convert")
async def convert(from_currency: str, to_currency: str, amount: float):
    cache_key = get_cache_key(from_currency, to_currency, amount)

    # 1. Cache prüfen
    cached = get_cache(cache_key)
    if cached:
        return {"cached": True, **cached}

    # 2. API-Aufruf
    params = {
        "access_key": API_KEY,
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"API-Anfrage fehlgeschlagen: {response.status_code}")#The error 

    data = response.json()
    if not data.get("success", False):
        err = data.get("error", {})
        raise HTTPException(status_code=400, detail=f"API-Fehler: {err}")

    result = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
        "result": data.get("result"),
        "info": data.get("info")  # enthält rate
    }

    # 3. Cache speichern
    set_cache(cache_key, result)

    return {"cached": False, **result}
