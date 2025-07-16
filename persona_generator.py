from transformers import pipeline
import random
from llm_utils import ask_gemini

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

TAGS = [
    "gaming", "technology", "AI", "machine learning", "career", "self-help",
    "funny", "advice", "relationships", "personal story", "finance", "education"
]

def classify_text(text):
    result = classifier(text, TAGS)
    top_tag = result["labels"][0]
    return top_tag, result

def score_motivations(texts):
    # Very simple scoring logic — could later use AI
    joined = " ".join(texts).lower()
    return {
        "Convenience": min(100, joined.count("easy") * 10 + 40),
        "Wellness": min(100, joined.count("health") * 10 + 30),
        "Speed": min(100, joined.count("fast") * 10 + 50),
        "Preferences": min(100, joined.count("like") * 10 + 50),
        "Comfort": min(100, joined.count("comfortable") * 10 + 40),
        "Dietary Needs": min(100, joined.count("diet") * 10 + 20)
    }

def map_personality(texts):
    # Simple random mapping — can be replaced with better analysis later
    return {
        "Introvert-Extrovert": random.randint(30, 70),
        "Intuition-Sensing": random.randint(40, 90),
        "Feeling-Thinking": random.randint(30, 80),
        "Perceiving-Judging": random.randint(30, 80),
    }

# def generate_summary(username, top_topics):
#     if "AI" in top_topics or "technology" in top_topics:
#         return f"{username} is a curious and analytical individual who frequently discusses tech and innovation."
#     elif "career" in top_topics:
#         return f"{username} appears career-focused, sharing advice and insights related to personal development."
#     else:
#         return f"{username} enjoys participating in discussions around diverse topics like {', '.join(list(top_topics)[:3])}."

def generate_persona(posts, comments, username=None):
    persona = {
        "Username": username or "",
        "Age": "25–35",
        "Occupation": "Tech Enthusiast",
        "Status": "Active",
        "Location": "Unknown",
        "Archetype": "Curious Explorer",
        "Tier": "Active Redditor",
        "Traits": ["Practical", "Curious", "Spontaneous", "Active"],
        "Behaviours": [],
        "Motivations": {},
        "Personality": {},
        "Goals": [],
        "Frustrations": [],
        "Topics Discussed": set(),
        "Evidence": [],
        "Quote": ""
    }

    # Combine a few posts and comments for analysis
    combined = posts[:5] + comments[:5]
    all_texts = []

    for item in combined:
        text = item.get("body") or item.get("title") or ""
        tag, result = classify_text(text)
        persona["Topics Discussed"].update(result["labels"][:3])
        persona["Evidence"].append(f"\"{text.strip()}\" — classified as {tag}")
        all_texts.append(text)

    all_text = " ".join(all_texts)
    text_blob = all_text.lower()

    # Always define these with safe defaults
    persona["Motivations"] = {}
    persona["Personality"] = {}
    persona["Behaviours"] = []
    persona["Goals"] = []
    persona["Frustrations"] = []
    persona["Quote"] = ""

    # Motivations
    try:
        persona["Motivations"] = score_motivations(all_texts)
    except:
        persona["Motivations"] = {}

    # Personality
    try:
        persona["Personality"] = map_personality(all_texts)
    except:
        persona["Personality"] = {}

    # Behaviours
    try:
        persona["Behaviours"] = ask_gemini(
            f"From the following Reddit posts/comments, list 3 core behaviors or habits that describe this user. Reply as a plain list:\n\n{all_text}"
        ).split("\n")
    except:
        persona["Behaviours"] = ["Explores Reddit frequently", "Engages in thoughtful discussions", "Shows curiosity"]

    # Goals
    try:
        persona["Goals"] = ask_gemini(
            f"What are the top 3 personal goals or needs of this Reddit user based on the following posts and comments? Reply as a plain list:\n\n{all_text}"
        ).split("\n")
    except:
        persona["Goals"] = ["Grow career", "Explore tech trends", "Build online presence"]

    # Frustrations
    try:
        persona["Frustrations"] = ask_gemini(
            f"What 3 frustrations or struggles does the user seem to experience based on the following Reddit content? Reply as a list:\n\n{all_text}"
        ).split("\n")
    except:
        persona["Frustrations"] = ["Lack of quality responses", "Shallow debates", "Negativity in threads"]

    # Quote
    try:
        persona["Quote"] = ask_gemini(
            f"Based on the Reddit content below, write a short motivational quote that captures this user's mindset:\n\n{all_text}"
        )
    except:
        persona["Quote"] = "I enjoy exploring new ideas and sharing what I learn."

    # Age detection
    if any(kw in text_blob for kw in ["high school", "freshman", "college", "i'm 18", "i'm 20", "i am 21"]):
        persona["Age"] = "18–25"
    elif any(kw in text_blob for kw in ["i'm 28", "i'm 30", "working", "corporate", "full-time"]):
        persona["Age"] = "26–35"
    elif any(kw in text_blob for kw in ["my kids", "married", "mortgage", "i’m 40"]):
        persona["Age"] = "36–50"

    # Occupation detection
    if "developer" in text_blob or "coding" in text_blob or "python" in text_blob:
        persona["Occupation"] = "Software Developer"
    elif "teacher" in text_blob or "classroom" in text_blob:
        persona["Occupation"] = "Educator"
    elif "freelancer" in text_blob or "graphic design" in text_blob:
        persona["Occupation"] = "Freelancer / Designer"
    elif "student" in text_blob or "exam" in text_blob:
        persona["Occupation"] = "Student"

    # Location detection
    if "india" in text_blob or "delhi" in text_blob or "mumbai" in text_blob:
        persona["Location"] = "India"
    elif "new york" in text_blob or "usa" in text_blob:
        persona["Location"] = "USA"
    elif "uk" in text_blob or "london" in text_blob:
        persona["Location"] = "UK"

    # Tier logic
    total_items = len(posts) + len(comments)
    if total_items > 50:
        persona["Tier"] = "Power User"
    elif total_items > 20:
        persona["Tier"] = "Active Redditor"
    else:
        persona["Tier"] = "Occasional User"

    # Archetype logic
    if "curious" in persona["Traits"] or "explore" in text_blob:
        persona["Archetype"] = "Curious Explorer"
    elif "help" in text_blob or "care" in text_blob:
        persona["Archetype"] = "Empathetic Helper"
    elif "logic" in text_blob or "science" in text_blob:
        persona["Archetype"] = "Analytical Thinker"
    else:
        persona["Archetype"] = "Quiet Observer"

    # Adjust final quote based on top topics
    topics = {t.lower() for t in persona["Topics Discussed"]}
    if "technology" in topics:
        persona["Quote"] = "Technology inspires me to keep learning and adapting."
    elif "self-help" in topics:
        persona["Quote"] = "Helping others helps me grow too."
    elif "career" in topics:
        persona["Quote"] = "I'm always working on becoming a better version of myself."
    elif "funny" in topics:
        persona["Quote"] = "If you can make people laugh, you’ve already won."
    elif "ai" in topics or "machine learning" in topics:
        persona["Quote"] = "Artificial Intelligence fascinates me and fuels my curiosity."
    elif "politics" in topics:
        persona["Quote"] = "I believe staying informed and speaking up is essential in today’s world."
    else:
        persona["Quote"] = persona["Quote"] or "I enjoy exploring new ideas and sharing what I learn."

    print("Topics Discussed:", persona["Topics Discussed"])  # Debug print
    return persona

