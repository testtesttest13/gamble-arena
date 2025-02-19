from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import hmac
import time

app = FastAPI()

# Autoriser le CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_BOT_TOKEN = "7639397685:AAGfgiGl1ynZ8ys9HSfbI9VrbkbhJN1bUgk"  # Remplace avec ton token de @BotFather

@app.get("/")
def read_root():
    return {"message": "GAMBLE ARENA API is running"}

@app.get("/auth")
async def auth(request: Request):
    query_params = dict(request.query_params)
    
    # Vérifier si Telegram a envoyé les bons paramètres
    if not query_params or "hash" not in query_params:
        return {"error": "Invalid request"}

    # Trier les paramètres comme demandé par Telegram
    auth_data = "\n".join(f"{k}={v}" for k, v in sorted(query_params.items()) if k != "hash")
    secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
    check_hash = hmac.new(secret_key, auth_data.encode(), hashlib.sha256).hexdigest()

    # Vérifier si la requête vient bien de Telegram
    if check_hash != query_params["hash"]:
        return {"error": "Invalid hash"}

    # Vérifier si la requête est récente (éviter les attaques)
    auth_time = int(query_params.get("auth_date", 0))
    if time.time() - auth_time > 86400:  # Plus de 24h
        return {"error": "Request too old"}

    return {
        "user_id": query_params.get("id"),
        "username": query_params.get("username"),
        "first_name": query_params.get("first_name"),
    }
