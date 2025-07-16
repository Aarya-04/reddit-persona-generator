import os
import sys
from urllib.parse import urlparse
from reddit_scraper import get_user_content
from persona_generator import generate_persona
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_username(url):
    return urlparse(url).path.strip("/").split("/")[-1]
 

def render_html_persona(persona, username, avatar_url):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('persona_template.html')

    # Normalize keys for template rendering
    persona["motivations"] = persona.get("Motivations", {})
    persona["personality"] = persona.get("Personality", {})
    persona["behaviours"] = persona.get("Behaviours", [])
    persona["goals"] = persona.get("Goals", [])
    persona["frustrations"] = persona.get("Frustrations", [])
    persona["topics"] = sorted(persona.get("Topics Discussed", []))
    persona["evidence"] = persona.get("Evidence", [])
    persona["traits"] = persona.get("Traits", [])

    # ✅ Add missing normalized keys for template
    persona["age"] = persona.get("Age", "")
    persona["occupation"] = persona.get("Occupation", "")
    persona["status"] = persona.get("Status", "")
    persona["location"] = persona.get("Location", "")
    persona["tier"] = persona.get("Tier", "")
    persona["archetype"] = persona.get("Archetype", "")

    html = template.render(**persona, username=username, avatar_url=avatar_url)

    output_file = os.path.join(OUTPUT_DIR, f"{username}_persona.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[✓] HTML persona saved as: {output_file}")



def save_persona(persona, username):
    filename = os.path.join(OUTPUT_DIR, f"{username}_persona.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{'='*50}\n")
        f.write(f"           REDDIT USER PERSONA - u/{username}\n")
        f.write(f"{'='*50}\n\n")

        # 👤 Personal Info
        f.write("👤 PERSONAL INFORMATION\n")
        f.write(f"Name: u/{username}\n")
        f.write(f"Age: {persona['Age']}\n")
        f.write(f"Occupation: {persona['Occupation']}\n")
        f.write(f"Location: {persona['Location']}\n")
        f.write(f"Status: {persona['Status']}\n")
        f.write(f"Tier: {persona['Tier']}\n")
        f.write(f"Archetype: {persona['Archetype']}\n\n")

        # 📝 Summary
        # f.write("📝 SUMMARY\n")
        # f.write(f"{persona['Summary']}\n\n")

        # ⭐ Traits
        f.write("⭐ TRAITS\n")
        f.write(", ".join(persona["Traits"]) + "\n\n")

        # 🔢 Motivations (scale 1–100)
        f.write("🔢 MOTIVATIONS (1–100)\n")
        for key, score in persona["Motivations"].items():
            f.write(f"- {key}: {score}\n")
        f.write("\n")

        # 🧠 Personality Spectrum
        f.write("🧠 PERSONALITY SPECTRUM\n")
        def scale(label, score, left, right):
            pos = int((score or 0) / 100 * 40)
            return f"{left} |" + ("=" * pos).ljust(40) + f"| {right} ({score})"

        f.write(scale("Introvert-Extrovert", persona["Personality"]["Introvert-Extrovert"], "Introvert", "Extrovert") + "\n")
        f.write(scale("Intuition-Sensing", persona["Personality"]["Intuition-Sensing"], "Intuition", "Sensing") + "\n")
        f.write(scale("Feeling-Thinking", persona["Personality"]["Feeling-Thinking"], "Feeling", "Thinking") + "\n")
        f.write(scale("Perceiving-Judging", persona["Personality"]["Perceiving-Judging"], "Perceiving", "Judging") + "\n\n")

        # 🧍 Behavior
        f.write("🧍 BEHAVIOR & HABITS\n")
        for item in persona["Behaviours"]:
            f.write(f"- {item}\n")
        f.write("\n")

        # 🎯 Goals
        f.write("🎯 GOALS & NEEDS\n")
        for item in persona["Goals"]:
            f.write(f"- {item}\n")
        f.write("\n")

        # 😤 Frustrations
        f.write("😤 FRUSTRATIONS\n")
        for item in persona["Frustrations"]:
            f.write(f"- {item}\n")
        f.write("\n")

        # 📚 Topics Discussed
        f.write("📚 TOPICS DISCUSSED\n")
        for topic in sorted(persona["Topics Discussed"]):
            f.write(f"- {topic}\n")
        f.write("\n")

        # 🔗 Evidence
        f.write("🔗 EVIDENCE & CITATIONS\n")
        for line in persona["Evidence"]:
            f.write(f"- {line}\n")
        f.write("\n")

        # 💬 Quote
        f.write("💬 INSPIRATIONAL QUOTE\n")
        f.write(f"\"{persona['Quote']}\"\n")

    print(f"[✓] Text persona saved as: {filename}")

if __name__ == "__main__":
    url = sys.argv[1]
    username = extract_username(url)
    posts, comments, avatar_url = get_user_content(username)
    persona = generate_persona(posts, comments, username)
    save_persona(persona, username)
    render_html_persona(persona, username, avatar_url)  # 👈 pass image
    print(f"[✓] Persona saved as {username}_persona.txt")
