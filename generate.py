import os
import json
import requests
from datetime import datetime
import re
import urllib.parse
import sys

# Get API key from environment variable (GitHub Secrets)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "d26a1d4af82d416d955b4237adae75f6")

ARCHIVE_FILE = "archive.json"

# Load existing archive
if os.path.exists(ARCHIVE_FILE):
    with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
        archive = json.load(f)
else:
    archive = []

# HTML Templates
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
    if not NEWS_API_KEY:
        print("ERROR: NEWS_API_KEY not found!")
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]
    
    try:
        print(f"Fetching headlines from NewsAPI...")
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if 'articles' not in data:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]
        
        headlines = [a['title'] for a in data['articles'][:6] if a.get('title')]
        print(f"Successfully fetched {len(headlines)} headlines")
        return headlines
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching headlines: {e}")
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]
    except Exception as e:
        print(f"Error fetching headlines: {e}")
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " - EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        '"This is the biggest thing ever!" said one insider who wished to remain anonymous.\n\n'
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing - stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
    content = content * 5  # Make it long
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    # Use a simpler query to avoid URL encoding issues
    keywords = title.split()[:3]  # First 3 words
    query = urllib.parse.quote(' '.join(keywords))
    return f"https://source.unsplash.com/featured/1200x600/?{query}"

os.makedirs("articles", exist_ok=True)

headlines = get_headlines()
new_entries = []
current_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
current_date = datetime.now().strftime("%Y-%m-%d")

for headline in headlines:
    article = make_funny_article(headline)
    title = article["title"]
    summary = article["summary"]
    content = article["content"]

    # Create a safe slug
    slug_base = re.sub(r'[^a-z0-9 ]', '', title.lower())
    slug = re.sub(r' +', '-', slug_base).strip('-')[:60] + ".html"
    slug = f"{current_date}-{slug}"

    image_url = get_matching_image(title)

    new_entries.append({
        "title": title, 
        "summary": summary, 
        "slug": slug, 
        "date": current_time, 
        "image_url": image_url
    })

    # Prepare content for HTML
    content_html = content.replace("\n", "<br>")
    
    # Encode for sharing
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}")
    
    # Write article file
    with open(f"articles/{slug}", "w", encoding="utf-8") as f:
        f.write(ARTICLE_TEMPLATE.format(
            title=title, 
            summary=summary, 
            content=content_html, 
            image_url=image_url, 
            encoded_title=encoded_title, 
            encoded_url=encoded_url
        ))

# Update archive
archive = new_entries + archive

# Save archive
with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive, f, ensure_ascii=False, indent=2)

# Build homepage HTML
articles_html = ""
for entry in archive:
    articles_html += f'''<div class="article">
        <h2><a href="articles/{entry["slug"]}">{entry["title"]}</a></h2>
        <p>{entry["summary"]}</p>
        <p class="date">{entry["date"]}</p>
    </div>'''

# Write homepage
with open("index.html", "w", encoding="utf-8") as f:
    f.write(HOME_TEMPLATE.format(time=current_time, articles_html=articles_html))

print(f"Generated {len(new_entries)} new articles")
print(f"Total articles in archive: {len(archive)}")
print("Your Tabloid Daily News is ready!")
sys.exit(0)  # Ensure clean exit for GitHub ActionsARTICLE_TEMPLATE = """<!DOCTYPE html>
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
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " — EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        '"This is the biggest thing ever!" said one insider who wished to remain anonymous.\n\n'
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing — stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
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

print("Your Tabloid Daily News is ready!")ARTICLE_TEMPLATE = """<!DOCTYPE html>
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
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " — EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        '"This is the biggest thing ever!" said one insider who wished to remain anonymous.\n\n'
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing — stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
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

print("Your Tabloid Daily News is ready!")ARTICLE_TEMPLATE = """<!DOCTYPE html>
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
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " — EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        '"This is the biggest thing ever!" said one insider who wished to remain anonymous.\n\n'
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing — stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
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

print("Your Tabloid Daily News is ready!")ARTICLE_TEMPLATE = """<!DOCTYPE html>
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
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " — EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        '"This is the biggest thing ever!" said one insider who wished to remain anonymous.\n\n'
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing — stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
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

print("Your Tabloid Daily News is ready!")ARTICLE_TEMPLATE = """<!DOCTYPE html>
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
        return ["Celebrity Secret Revealed!", "Politician's Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " — EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you won't believe what happened next!"
    content = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        '"This is the biggest thing ever!" said one insider who wished to remain anonymous.\n\n'
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing — stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
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

print("Your Tabloid Daily News is ready!")
