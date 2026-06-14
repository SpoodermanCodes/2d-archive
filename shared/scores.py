import json, os

SCORES_FILE = os.path.join(os.path.dirname(__file__), '..', 'scores.json')

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f:
            return json.load(f)
    return {g: 0 for g in ['snake', 'tetris', 'pong', 'space_invaders', 'flappy_bird']}

def save_score(game, score):
    scores = load_scores()
    if score > scores.get(game, 0):
        scores[game] = score
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f)
