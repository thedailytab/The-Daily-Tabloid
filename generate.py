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
    sys.exit(main())
