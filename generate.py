import os
import json
import requests
from datetime import datetime
import re
import sys

API_KEY = os.environ.get("NEWS_API_KEY", "")
ARCHIVE = "archive.json"

def load_archive():
    if os.path.exists(ARCHIVE):
        with open(ARCHIVE, "r") as f:
            return json.load(f)
    return []

def save_archive(data):
    with open(ARCHIVE, "w") as f:
        json.dump(data, f, indent=2)

def fetch_news():
    if not API_KEY:
        print("No API key found, using fallback headlines")
        return [
            "Local Cat Declares Itself Mayor",
            "Man Wins Lottery Twice in One Day",
            "Scientists Discover Coffee Makes You Awake",
            "Celebrity Spotted Eating Food",
            "Weather Happens Outside Today",
            "Internet Argues About Something"
        ]
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if "articles" in data:
            titles = [a["title"] for a in data["articles"][:6] if a.get("title")]
            print(f"Fetched {len(titles)} headlines")
            return titles
    except Exception as e:
        print(f"API error: {e}")
    
    return ["Breaking News Breaks", "Story Develops Into Story"]

def make_slug(text):
    clean = re.sub(r'[^a-z0-9]+', '-', text.lower())
    return clean.strip('-')[:50]

def create_article(headline):
    title = headline.upper() + " - SHOCKING EXCLUSIVE"
    slug = make_slug(headline) + ".html"
    date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    body = f"""
    <p><strong>BREAKING:</strong> Sources confirm that {headline.lower()} and experts are stunned.</p>
    <p>"This is unprecedented," said one anonymous insider who definitely exists.</p>
    <p>Witnesses report seeing things with their own eyes.</p>
    <p>Social media has exploded with reactions ranging from shock to surprise.</p>
    <p>Industry experts predict this will have consequences.</p>
    <p>More details are emerging as we speak.</p>
    <p>Officials have released a statement containing words.</p>
    <p>The public is advised to remain aware of the situation.</p>
    <p>This story is developing and will continue to develop.</p>
    <p>Stay tuned for updates that may or may not arrive.</p>
    """ * 3
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{margin: 0; padding: 0; box-sizing: border-box;}}
body {{font-family: Georgia, serif; background: #f5f5f5; padding: 20px;}}
.container {{max-width: 800px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);}}
h1 {{color: #c00; font-size: 2.5em; margin-bottom: 10px; line-height: 1.2;}}
.meta {{color: #666; font-size: 0.9em; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #c00;}}
p {{font-size: 1.1em; line-height: 1.8; margin-bottom: 20px;}}
.back {{margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;}}
.back a {{color: #c00; text-decoration: none; font-weight: bold;}}
.back a:hover {{text-decoration: underline;}}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<div class="meta">{date}</div>
{body}
<div class="back"><a href="../index.html">← Back to All Stories</a></div>
</div>
</body>
</html>"""
    
    return {"title": title, "slug": slug, "date": date, "html": html}

def create_homepage(articles):
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    article_list = ""
    for art in articles:
        article_list += f"""
        <div class="story">
            <h2><a href="articles/{art['slug']}">{art['title']}</a></h2>
            <p class="date">{art['date']}</p>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Tabloid Times - Shocking News Daily</title>
<style>
* {{margin: 0; padding: 0; box-sizing: border-box;}}
body {{font-family: Georgia, serif; background: #f5f5f5; padding: 20px;}}
.container {{max-width: 1000px; margin: 0 auto;}}
header {{background: #c00; color: white; padding: 40px 20px; text-align: center; margin-bottom: 30px;}}
h1 {{font-size: 3.5em; text-transform: uppercase; letter-spacing: 2px; text-shadow: 3px 3px 0 #900;}}
.tagline {{font-size: 1.2em; margin-top: 10px; font-style: italic;}}
.updated {{text-align: center; color: #666; margin-bottom: 30px;}}
.story {{background: white; padding: 30px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}}
.story h2 {{color: #c00; font-size: 2em; margin-bottom: 10px;}}
.story a {{color: #c00; text-decoration: none;}}
.story a:hover {{text-decoration: underline;}}
.date {{color: #666; font-size: 0.9em;}}
footer {{text-align: center; padding: 40px 20px; color: #666; border-top: 3px solid #c00; margin-top: 40px;}}
</style>
</head>
<body>
<div class="container">
<header>
<h1>The Tabloid Times</h1>
<div class="tagline">SHOCKING NEWS • EXCLUSIVE STORIES • UNBELIEVABLE FACTS</div>
</header>
<div class="updated">Last Updated: {now}</div>
{article_list}
<footer>
<p>All stories are 100% real and not made up at all.</p>
<p>© {datetime.now().year} The Tabloid Times</p>
</footer>
</div>
</body>
</html>"""
    
    return html

def main():
    print("Starting Tabloid Times generator...")
    
    os.makedirs("articles", exist_ok=True)
    
    headlines = fetch_news()
    archive = load_archive()
    new_articles = []
    
    for headline in headlines:
        article = create_article(headline)
        new_articles.append({
            "title": article["title"],
            "slug": article["slug"],
            "date": article["date"]
        })
        
        filepath = os.path.join("articles", article["slug"])
        with open(filepath, "w") as f:
            f.write(article["html"])
        print(f"Created: {article['slug']}")
    
    all_articles = new_articles + archive
    save_archive(all_articles)
    
    homepage = create_homepage(all_articles)
    with open("index.html", "w") as f:
        f.write(homepage)
    
    print(f"Generated {len(new_articles)} new articles")
    print(f"Total articles: {len(all_articles)}")
    print("Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main()){articles_html}
<hr style="border: 3px dashed red;">
<p style="text-align:center; color:gray;">ARCHIVE: Every funny story saved forever!</p>
</body>
</html>"""

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {font-family: Arial Black, Arial, sans-serif; margin: 20px auto; max-width: 800px;}
h1 {color: red; font-size: 3.2em; text-transform: uppercase; text-align: center;}
img {width: 100 percent; max-height: 500px; object-fit: cover; border-radius: 15px; margin: 30px 0;}
em {display: block; text-align: center; font-size: 1.7em; margin: 40px 0;}
p {font-size: 1.4em; line-height: 1.9;}
.share {text-align: center; margin: 60px 0;}
.share-btn {background: red; color: white; padding: 18px 35px; margin: 15px; font-size: 1.6em; border-radius: 10px; text-decoration: none;}
.back {text-align: center; margin: 60px 0; font-size: 1.4em;}
</style>
</head>
<body>
<h1>{title}</h1>
<img src="{image_url}" alt="Funny Picture">
<em>{summary}</em>
<div>{content}</div>
<div class="share">
<a class="share-btn" href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" target="_blank">SCREAM ON X!</a>
<a class="share-btn" href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank">BLAST ON FACEBOOK!</a>
</div>
<div class="back"><a href="../index.html">MORE FUNNY STORIES</a></div>
</body>
</html>"""

def get_headlines():
    if not NEWS_API_KEY:
        print("ERROR: NEWS_API_KEY not found!")
        return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]
    
    try:
        print("Fetching headlines from NewsAPI...")
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if 'articles' not in data:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]
        
        headlines = [a['title'] for a in data['articles'][:6] if a.get('title')]
        print(f"Successfully fetched {len(headlines)} headlines")
        return headlines
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]
    except Exception as e:
        print(f"Error: {e}")
        return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " - EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you will not believe what happened next!"
    
    content_piece = (
        "EXCLUSIVE: Multiple sources have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        "This is the biggest thing ever said one insider.\n\n"
        "Eyewitnesses report seeing mysterious things.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward.\n\n"
        "Our investigation is ongoing - stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
    content = content_piece * 5
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    keywords = title.split()[:3]
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

    content_html = content.replace("\n", "<br>")
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}")
    
    with open(f"articles/{slug}", "w", encoding="utf-8") as f:
        f.write(ARTICLE_TEMPLATE.format(
            title=title, 
            summary=summary, 
            content=content_html, 
            image_url=image_url, 
            encoded_title=encoded_title, 
            encoded_url=encoded_url
        ))

archive = new_entries + archive

with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive, f, ensure_ascii=False, indent=2)

articles_html = ""
for entry in archive:
    articles_html += f'<div class="article"><h2><a href="articles/{entry["slug"]}">{entry["title"]}</a></h2><p>{entry["summary"]}</p><p class="date">{entry["date"]}</p></div>'

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HOME_TEMPLATE.format(time=current_time, articles_html=articles_html))

print(f"Generated {len(new_entries)} new articles")
print(f"Total articles in archive: {len(archive)}")
print("Your Tabloid Daily News is ready!")
sys.exit(0){articles_html}
<hr style="border: 3px dashed #ff0000;">
<p style="text-align:center; color:#777;">ARCHIVE: Every funny story saved forever!</p>
</body>
</html>"""

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {font-family: Arial Black, Arial, sans-serif; margin: 20px auto; max-width: 800px;}
h1 {color: #ff0000; font-size: 3.2em; text-transform: uppercase; text-align: center;}
img {width: 100%; max-height: 500px; object-fit: cover; border-radius: 15px; margin: 30px 0;}
em {display: block; text-align: center; font-size: 1.7em; margin: 40px 0;}
p {font-size: 1.4em; line-height: 1.9;}
.share {text-align: center; margin: 60px 0;}
.share-btn {background: #ff0000; color: white; padding: 18px 35px; margin: 15px; font-size: 1.6em; border-radius: 10px; text-decoration: none;}
.back {text-align: center; margin: 60px 0; font-size: 1.4em;}
</style>
</head>
<body>
<h1>{title}</h1>
<img src="{image_url}" alt="Funny Picture">
<em>{summary}</em>
<div>{content}</div>
<div class="share">
<a class="share-btn" href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" target="_blank">SCREAM ON X!</a>
<a class="share-btn" href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank">BLAST ON FACEBOOK!</a>
</div>
<div class="back"><a href="../index.html">MORE FUNNY STORIES</a></div>
</body>
</html>"""

def get_headlines():
    if not NEWS_API_KEY:
        print("ERROR: NEWS_API_KEY not found!")
        return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]
    
    try:
        print("Fetching headlines from NewsAPI...")
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if 'articles' not in data:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]
        
        headlines = [a['title'] for a in data['articles'][:6] if a.get('title')]
        print(f"Successfully fetched {len(headlines)} headlines")
        return headlines
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching headlines: {e}")
        return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]
    except Exception as e:
        print(f"Error fetching headlines: {e}")
        return ["Celebrity Secret Revealed!", "Politician Wild Mistake!"]

def make_funny_article(headline):
    title = headline.upper() + " - EXCLUSIVE BOMBSHELL!"
    summary = "Insiders say you will not believe what happened next!"
    
    content_piece = (
        "EXCLUSIVE: Multiple sources close to the situation have come forward with jaw-dropping details about " + headline.lower() + ".\n\n"
        "This is the biggest thing ever said one insider who wished to remain anonymous.\n\n"
        "Eyewitnesses report seeing mysterious things happening.\n\n"
        "Celebrity watchers are linking it to famous people.\n\n"
        "Leaked documents show secret stuff.\n\n"
        "The plot thickens as more people come forward with wild stories.\n\n"
        "Our investigation is ongoing - stay tuned!\n\n"
        "Sources say this changes everything.\n\n"
        "More to come as this story develops!\n\n"
    )
    content = content_piece * 5
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    keywords = title.split()[:3]
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

    content_html = content.replace("\n", "<br>")
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}")
    
    with open(f"articles/{slug}", "w", encoding="utf-8") as f:
        f.write(ARTICLE_TEMPLATE.format(
            title=title, 
            summary=summary, 
            content=content_html, 
            image_url=image_url, 
            encoded_title=encoded_title, 
            encoded_url=encoded_url
        ))

archive = new_entries + archive

with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive, f, ensure_ascii=False, indent=2)

articles_html = ""
for entry in archive:
    articles_html += f'<div class="article"><h2><a href="articles/{entry["slug"]}">{entry["title"]}</a></h2><p>{entry["summary"]}</p><p class="date">{entry["date"]}</p></div>'

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HOME_TEMPLATE.format(time=current_time, articles_html=articles_html))

print(f"Generated {len(new_entries)} new articles")
print(f"Total articles in archive: {len(archive)}")
print("Your Tabloid Daily News is ready!")
sys.exit(0)<hr style="border: 3px dashed #ff0000;">
<p style="text-align:center; color:#777;">ARCHIVE: Every funny story saved forever!</p>
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
    content = content * 5
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    keywords = title.split()[:3]
    query = urllib.parse.quote(' '.join(keywords))
    return f"https://source.unsplash.com/featured/1200x600/?{query}"

# Create articles directory
os.makedirs("articles", exist_ok=True)

# Get headlines and generate stories
headlines = get_headlines()
new_entries = []
current_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
current_date = datetime.now().strftime("%Y-%m-%d")

for headline in headlines:
    article = make_funny_article(headline)
    title = article["title"]
    summary = article["summary"]
    content = article["content"]

    # Create safe slug
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
sys.exit(0)lhr style="border: 3px dashed #ff0000;">
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
    content = content * 5
    return {"title": title, "summary": summary, "content": content}

def get_matching_image(title):
    keywords = title.split()[:3]
    query = urllib.parse.quote(' '.join(keywords))
    return f"https://source.unsplash.com/featured/1200x600/?{query}"

# Create articles directory
os.makedirs("articles", exist_ok=True)

# Get headlines and generate stories
headlines = get_headlines()
new_entries = []
current_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
current_date = datetime.now().strftime("%Y-%m-%d")

for headline in headlines:
    article = make_funny_article(headline)
    title = article["title"]
    summary = article["summary"]
    content = article["content"]

    # Create safe slug
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
sys.exit(0)<hr style="border: 3px dashed #ff0000;">
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
