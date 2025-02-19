from fastapi import FastAPI
from backend.game_logic import gamble, get_leaderboard
from fastapi.middleware.cors import CORSMiddleware

# Initialisation de l'application FastAPI
app = FastAPI()

# Autoriser le CORS pour permettre les requêtes du frontend (Mini App Telegram)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],  # Autoriser uniquement le frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "GAMBLE ARENA API is running"}

@app.post("/play/")
def play_game(user_id: int, bet_amount: int):
    return gamble(user_id, bet_amount)

@app.get("/leaderboard/")
def leaderboard():
    return get_leaderboard()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
