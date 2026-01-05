import os
import json
import requests
from datetime import datetime
import re
import urllib.parse

NEWS_API_KEY = "d26a1d4af82d416d955b4237adae75f6"

ARCHIVE_FILE = "archive.json"

if os.path.exists(ARCHIVE_FILE):
    with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
        archive = json.load(f)
else:
    archive = []

HOME_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>The Tabloid Daily News</title>
<style>
body {font-family: Arial Black, Arial, sans-serif; margin: 20px auto; max-width: 900px; background: #fff;}
h1 {text-align: center; color: #ff0000; font-size: 3.5em; text-transform: uppercase; text-shadow: 4px 4px #ffff00;}
.subtitle {text-align: center; font-size: 1.8em; font-style: italic;}
.article {border-bottom: 6px dashed #ff0000; padding: 30px 0; background: #fffbe6; margin: 20px 0; border-radius: 15px;}
h2 {color: #ff0000; font-size: 2.4em; text-transform: uppercase;}
a {text-decoration: none; color: inherit;}
.date {font-size: 0.9em; color: #555; text-align: right;}
</style></head><body>
<h1>THE TABLOID DAILY NEWS</h1>
<p class="subtitle">EXCLUSIVE BOMBSHELLS! OUTRAGEOUS SCANDALS!</p>
<p style="text-align:center;">Updated: {time}</p>
{articles_html}
<hr style="border: 3px dashed #ff0000;">
<p style="text-align:center; color:#777;">ARCHIVE: Every funny story saved forever 😈</p>
</body></html>"""

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body {font-family: Arial Black, Arial, sans-serif; margin: 20px auto; max-width: 800px;}
h1 {color: #ff0000; font-size: 3.2em; text-transform: uppercase; text-align: center;}
img {width: 100%; max-height: 500px; object-fit: cover; border-radius: 15px; margin: 30px 0;}
em {display: block; text-align: center; font-size: 1.7em; margin: 40px 0;}
p {font-size: 1.4em; line-height: 1.9;}
.share {text-align: center; margin: 60px 0;}
.share-btn {background: #ff0000; color: white; padding: 18px 35px; margin: 15px; font-size: 1.6em; border-radius: 10px; text-decoration: none;}
.back {text-align: center; margin: 60px 0; font-size: 1.4em;}
</style></head><body>
<h1>{title}</h1>
<img src="{image_url}" alt="Funny Picture">
<em>{summary}</em>
<div>{content}</div>
<div class="share">
  <a class="share-btn" href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" target="_blank">SCREAM ON X!</a>
  <a class="share-btn" href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank">BLAST ON FACEBOOK!</a>
</div>
<div class="back"><a href="../index.html">← MORE FUNNY STORIES</a></div>
</body></html>"""

def get_headlines():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}").json()
        return [a['title'] for a in r['articles'][:6] if a['title']]
    except:
        return ["Big Celebrity Secret!", "Politician's Funny Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " — EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = f"""
    EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about {headline.lower()}.

    "This is the biggest thing ever!" said one insider who wished to remain anonymous.

    Eyewitnesses report seeing mysterious things happening.

    Celebrity watchers are linking it to famous people.

    Leaked documents show secret stuff.

    The plot thickens as more people come forward with wild stories.

    Our investigation is ongoing — stay tuned!

    Sources say this changes everything.

    More to come as this story develops!
    """
    content = content * 5  # Make it long
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    query = urllib.parse.quote(title + " funny tabloid scandal")
    return f"https://source.unsplash.com/featured/1200x600/?{query}"

os.makedirs("articles", exist_ok=True)

headlines = get_headlines()
new_entries = []
current_time = datetime.now().strftime("%B %d, %Y • %I:%M %p")
current_date = datetime.now().strftime("%Y-%m-%d")

for headline in headlines:
    article = make_funny_article(headline)
    title = article["title"]
    summary = article["summary"]
    content = article["content"]

    slug_base = re.sub(r'[^a-z0-9 ]', '', title.lower())
    slug = re.sub(r' +', '-', slug_base).strip('-')[:60] + ".html"
    slug = f"{current_date}-{slug}"

    image_url = get_matching_image(title)

    new_entries.append({"title": title, "summary": summary, "slug": slug, "date": current_time, "image_url": image_url})

    content_html = content.replace("\n", "<br>")
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}")
    with open(f"articles/{slug}", "w", encoding="utf-8") as f:
        f.write(ARTICLE_TEMPLATE.format(title=title, summary=summary, content=content_html, image_url=image_url, encoded_title=encoded_title, encoded_url=encoded_url))

archive = new_entries + archive

with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive, f, ensure_ascii=False, indent=2)

articles_html = ""
for entry in archive:
    articles_html += f'<div class="article"><h2><a href="articles/{entry["slug"]}">{entry["title"]}</a></h2><p>{entry["summary"]}</p><p class="date">{entry["date"]}</p></div>'

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HOME_TEMPLATE.format(time=current_time, articles_html=articles_html))

print("Your Tabloid Daily News is ready!")e {text-decoration: none; color: inherit;}
.date {font-size: 0.9em; color: #555; text-align: right;}
</style></head><body>
<h1>THE TABLOID DAILY NEWS</h1>
<p class="subtitle">EXCLUSIVE BOMBSHELLS! OUTRAGEOUS SCANDALS!</p>
<p style="text-align:center;">Updated: {time}</p>
{articles_html}
<hr style="border: 3px dashed #ff0000;">
<p style="text-align:center; color:#777;">ARCHIVE: Every funny story saved forever 😈</p>
</body></html>"""

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body {font-family: Arial Black, Arial, sans-serif; margin: 20px auto; max-width: 800px;}
h1 {color: #ff0000; font-size: 3.2em; text-transform: uppercase; text-align: center;}
img {width: 100%; max-height: 500px; object-fit: cover; border-radius: 15px; margin: 30px 0;}
em {display: block; text-align: center; font-size: 1.7em; margin: 40px 0;}
p {font-size: 1.4em; line-height: 1.9;}
.share {text-align: center; margin: 60px 0;}
.share-btn {background: #ff0000; color: white; padding: 18px 35px; margin: 15px; font-size: 1.6em; border-radius: 10px; text-decoration: none;}
.back {text-align: center; margin: 60px 0; font-size: 1.4em;}
</style></head><body>
<h1>{title}</h1>
<img src="{image_url}" alt="Funny Picture">
<em>{summary}</em>
<div>{content}</div>
<div class="share">
  <a class="share-btn" href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" target="_blank">SCREAM ON X!</a>
  <a class="share-btn" href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank">BLAST ON FACEBOOK!</a>
</div>
<div class="back"><a href="../index.html">← MORE FUNNY STORIES</a></div>
</body></html>"""

def get_headlines():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}").json()
        return [a['title'] for a in r['articles'][:6] if a['title']]
    except:
        return ["Celebrity Secret!", "Politician's Funny Mistake!"]

def generate_satire(headline):
    payload = {
        "messages": [
            {"role": "system", "content": "You are a crazy funny tabloid writer. Make a LONG story (10-15 parts) with ALL CAPS, fake funny quotes, silly conspiracies, and celebrity names. Make people laugh! No 'shock' word."},
            {"role": "user", "content": headline}
        ],
        "max_tokens": 2000,
        "temperature": 1.0
    }
    response = requests.post(f"https://models.inference.ai.azure.com/chat/completions?model={MODEL}", headers=headers, json=payload)
    if response.status_code != 200:
        return {"title": headline.upper() + " EXCLUSIVE!", "summary": "You won't believe...", "content": "Long funny story here..." * 10}
    data = response.json()
    full_text = data["choices"][0]["message"]["content"]
    title = full_text.split("\n")[0].strip() or headline.upper() + " BOMBSHELL!"
    summary = full_text.split("\n")[1].strip() or "Insiders say the funniest thing..."
    content = full_text
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    query = urllib.parse.quote(title + " funny tabloid scandal")
    return f"https://source.unsplash.com/featured/1200x600/?{query}"

os.makedirs("articles", exist_ok=True)

headlines = get_headlines()
new_entries = []
current_time = datetime.now().strftime("%B %d, %Y • %I:%M %p")
current_date = datetime.now().strftime("%Y-%m-%d")

for headline in headlines:
    article = generate_satire(headline)
    title = article["title"]
    summary = article["summary"]
    content = article["content"]

    slug_base = re.sub(r'[^a-z0-9 ]', '', title.lower())
    slug = re.sub(r' +', '-', slug_base).strip('-')[:60] + ".html"
    slug = f"{current_date}-{slug}"

    image_url = get_matching_image(title)

    new_entries.append({"title": title, "summary": summary, "slug": slug, "date": current_time, "image_url": image_url})

    content_html = content.replace("\n", "<br>")
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}")
    with open(f"articles/{slug}", "w", encoding="utf-8") as f:
        f.write(ARTICLE_TEMPLATE.format(title=title, summary=summary, content=content_html, image_url=image_url, encoded_title=encoded_title, encoded_url=encoded_url))

archive = new_entries + archive

with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive, f, ensure_ascii=False, indent=2)

articles_html = ""
for entry in archive:
    articles_html += f'<div class="article"><h2><a href="articles/{entry["slug"]}">{entry["title"]}</a></h2><p>{entry["summary"]}</p><p class="date">{entry["date"]}</p></div>'

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HOME_TEMPLATE.format(time=current_time, articles_html=articles_html))

print("Your newspaper is ready with GitHub's free AI!")
