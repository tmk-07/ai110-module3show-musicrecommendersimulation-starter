# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of it like a 100-point report card for every song, based on how well it matches your taste.

Each song earns points in four categories:

- **Genre (40 points):** If the song's genre matches your favorite genre, it gets all 40 points. Otherwise, zero — genre is treated as an all-or-nothing match.
- **Mood (30 points):** Same idea — if the song's mood matches your favorite mood, it gets all 30 points, otherwise zero.
- **Energy (20 points):** This one isn't all-or-nothing. The model checks how close the song's energy level is to the energy you asked for, and gives partial credit the closer it gets. A song with energy almost exactly where you want it gets nearly all 20 points; a song that's way off gets very little.
- **Acousticness (10 points):** Works the same way as energy — if you said you like (or don't like) acoustic songs, the model checks how close the song's acoustic level is to what you want and gives partial credit accordingly.

All four scores are added up to get a final score out of 100. Songs are then sorted from highest to lowest score, and the top few are shown to you along with plain-language reasons (like "genre match (rock)" or "energy is close to your target") explaining why each one scored the way it did.

The idea behind giving genre and mood more weight than energy and acousticness is that matching what kind of music and vibe you want matters more than fine-tuning the exact intensity or acoustic feel — but those still matter, so they're rewarded gradually rather than ignored.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
