# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

The Song object will use features like genre, mood, energy, valence, tempo_bpm, danceability, and acousticness, while UserProfile will store preferred values. 

### Algorithm Recipe (finalized)

Each song is scored against a user's taste profile on a 100-point scale, split across four signals:

| Signal | Weight | Type | How it's scored |
|---|---|---|---|
| Genre match | 40 pts | categorical (all-or-nothing) | Full 40 pts if `song.genre == favorite_genre`, else 0 |
| Mood match | 30 pts | categorical (all-or-nothing) | Full 30 pts if `song.mood == favorite_mood`, else 0 |
| Energy closeness | 20 pts | continuous (graded) | `20 * (1 - |song.energy - target_energy|)`, floored at 0 — near misses still earn partial credit |
| Acousticness fit | 10 pts | continuous (graded) | `10 * (1 - |song.acousticness - (1 if likes_acoustic else 0)|)`, floored at 0 |

Steps:
1. Load all songs and the user's `UserProfile` (favorite genre, favorite mood, target energy, acoustic preference).
2. Score every song with the recipe above, collecting a human-readable reason for each point source that applied.
3. Sort all songs by total score, descending.
4. Return the top `k` songs (default 5) along with their score and explanation string.

Genre and mood are treated as identity signals — you either match the user's stated taste or you don't — while energy and acousticness are treated as dials, rewarding songs that are *close* to the target rather than requiring an exact match.

### Potential Biases

- **Genre dominance**: genre is worth 40% of the score, the single largest weight. A song that matches genre but nothing else can still outscore a song that matches mood, energy, and acousticness combined. This means the system can over-prioritize genre and overlook great songs that match the user's mood or vibe but happen to sit in a different genre bucket.
- **Cold start / popularity blindness**: scoring is based purely on declared taste attributes, so the system has no way to surface songs the user might like but wouldn't have predicted from their stated profile (no collaborative filtering, no "users like you also enjoyed..." signal).
- **Exact-match bias on categorical fields**: genre and mood are all-or-nothing, so a song labeled "indie pop" scores 0 genre points against a user who said "pop," even though a human would call them closely related. This can penalize songs due to labeling granularity rather than actual taste mismatch.
- **No diversity control**: the top-k results are a pure sort by score, so recommendations can cluster heavily around one artist or sub-genre if several of their songs all score well, rather than giving the user a varied list.
- **Small, manually curated catalog**: with only ~20 songs, the system can't demonstrate how it handles genre/mood imbalance at scale (e.g., if most catalog songs are pop, non-pop fans are structurally underserved regardless of scoring logic).

--- 



## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



