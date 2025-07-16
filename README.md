
# Reddit Persona Generator 🤖

Generate a detailed **user persona** for any public Reddit user using AI-based analysis, NLP, and Gemini models.  
Outputs include a **beautiful HTML page** and a structured **text report** summarizing behaviors, traits, motivations, frustrations, and more.

---

## 📂 Project Structure

```
.
├── .env                    # Stores API keys
├── check_gemini_models.py  # Lists available Gemini models
├── llm_utils.py            # Utility function to call Gemini API
├── main.py                 # Main driver script
├── persona_generator.py    # AI-based logic to generate persona
├── reddit_scraper.py       # Scrapes posts/comments using PRAW
├── requirements.txt        # Python dependencies
├── outputs/                # Generated personas (HTML + TXT)
├── templates/
│   └── persona_template.html  # Jinja2 HTML template for persona
└── venv/                   # Python virtual environment (optional)
```

---

## 🚀 Features

- ✅ Scrapes recent **Reddit posts and comments**
- ✅ Uses **Gemini 1.5 Pro** LLM to infer:
  - Behaviors
  - Goals & Needs
  - Frustrations
  - Motivational scores
  - Personality spectrums
  - Inspiring quotes
- ✅ Generates:
  - `username_persona.txt` → for structured text report
  - `username_persona.html` → a visual persona dashboard
- ✅ Runs from command line with just a Reddit profile URL!

---

## 🔧 Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up `.env` file

Create a file named `.env` in the root directory and add the following:

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_custom_user_agent
GEMINI_API_KEY=your_gemini_api_key
```

---

## ✅ Run the Script

```bash
python main.py https://www.reddit.com/user/kojied/
```

Outputs will be saved in the `outputs/` folder:

- `kojied_persona.txt`
- `kojied_persona.html`

---

## 📦 Dependencies

- `praw` — Reddit API wrapper  
- `transformers` — For zero-shot classification  
- `google-generativeai` — Gemini model API  
- `python-dotenv` — Load secrets from `.env`  
- `torch` — Backend for transformers  
- `jinja2` — For rendering HTML templates  

---

## 🔍 Sample Users Processed

The following Reddit users have been successfully processed by the system:

```markdown
1. u/kojied  
2. u/Hungry-Move-6603  
3. u/books  
4. u/politics  
5. u/PeterExplainsTheJoke  
```

For each user, the system generates:

```
📄 outputs/<username>_persona.txt  
🌐 outputs/<username>_persona.html  
```

You can find them in the `outputs/` folder after running the script.

---

## 📄 License

This project is licensed under the MIT License.

---
