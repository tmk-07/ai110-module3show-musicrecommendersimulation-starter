import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Point weights for score_song. Genre and mood are categorical "identity"
# signals (all-or-nothing match), energy and acousticness are continuous
# dials scored by closeness to the user's target.
GENRE_WEIGHT = 40
MOOD_WEIGHT = 30
ENERGY_WEIGHT = 20
ACOUSTIC_WEIGHT = 10

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs for a user, ranked by score."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        songs_as_dicts = [vars(song) for song in self.songs]
        ranked = recommend_songs(user_prefs, songs_as_dicts, k=k)
        by_id = {song.id: song for song in self.songs}
        return [by_id[song_dict["id"]] for song_dict, _score, _explanation in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a plain-language explanation of why a song scored as it did."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _score, reasons = score_song(user_prefs, vars(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts."""
    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences out of 100, with reasons for each point awarded."""
    reasons = []
    score = 0.0

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song['genre']}) (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song['mood']}) (+{MOOD_WEIGHT:.1f})")

    energy_closeness = 1 - abs(song["energy"] - user_prefs["target_energy"])
    energy_points = ENERGY_WEIGHT * max(0.0, energy_closeness)
    score += energy_points
    if energy_closeness >= 0.8:
        reasons.append(f"energy ({song['energy']:.2f}) is close to your target (+{energy_points:.1f})")

    acoustic_target = 1.0 if user_prefs["likes_acoustic"] else 0.0
    acoustic_closeness = 1 - abs(song["acousticness"] - acoustic_target)
    acoustic_points = ACOUSTIC_WEIGHT * max(0.0, acoustic_closeness)
    score += acoustic_points
    if user_prefs["likes_acoustic"] and song["acousticness"] > 0.5:
        reasons.append(f"has the acoustic feel you like (+{acoustic_points:.1f})")
    elif not user_prefs["likes_acoustic"] and song["acousticness"] <= 0.5:
        reasons.append(f"isn't too acoustic, as you prefer (+{acoustic_points:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores and sorts songs for a user, returning the top-k (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches, but still worth a listen"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
