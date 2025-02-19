import random
from backend.database import players

def gamble(user_id, bet_amount):
    if user_id not in players:
        players[user_id] = {"points": 1000, "wins": 0, "losses": 0}
    
    if players[user_id]["points"] < bet_amount:
        return {"status": "error", "message": "Pas assez de points"}
    
    players[user_id]["points"] -= bet_amount
    outcome = random.choice(["win", "lose"])
    
    if outcome == "win":
        winnings = bet_amount * 2
        players[user_id]["points"] += winnings
        players[user_id]["wins"] += 1
        return {"status": "win", "message": f"Vous avez gagné {winnings} points!"}
    else:
        players[user_id]["losses"] += 1
        return {"status": "lose", "message": "Dommage, vous avez perdu!"}

def get_leaderboard():
    sorted_players = sorted(players.items(), key=lambda x: x[1]['points'], reverse=True)
    return [{"user_id": uid, "points": data["points"]} for uid, data in sorted_players[:5]]
