# This is the COMPLETE generate.py file from the beginning
# Copy this ENTIRE file to replace your generate.py

import os
import json
import requests
from datetime import datetime, timezone, timedelta
import re
import sys
import random
import hashlib

API_KEY = os.environ.get("NEWS_API_KEY", "")
ARCHIVE = "archive.json"

def get_cst_time():
    cst = timezone(timedelta(hours=-6))
    return datetime.now(cst)

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
        print("No API key, using fallback")
        return ["Cat Elected Mayor", "Man Wins Lottery Twice"]
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if "articles" in data:
            titles = [a["title"] for a in data["articles"][:10] if a.get("title")]
            if len(titles) >= 2:
                selected = random.sample(titles, 2)
            else:
                selected = titles[:2]
            print(f"Selected {len(selected)} headlines")
            return selected
    except Exception as e:
        print(f"API error: {e}")
    
    return ["Breaking News", "Story Develops"]

def make_slug(text):
    clean = re.sub(r'[^a-z0-9]+', '-', text.lower())
    return clean.strip('-')[:50]

def get_image_url(headline):
    colors = ['FF6B6B', '4ECDC4', '45B7D1', 'FFA07A', '98D8C8', 'F7DC6F']
    color = colors[abs(hash(headline)) % len(colors)]
    return f"https://via.placeholder.com/1200x600/{color}/FFFFFF?text=Breaking+News"

def generate_content(headline):
    words = headline.lower().split()
    subject = ' '.join(words[:5]) if len(words) >= 5 else headline.lower()
    
    openings = [
        f"In a move that surprised nobody, {subject}.",
        f"Breaking: {subject}. The universe shrugged.",
        f"Nation says 'well, that figures' as {subject}.",
    ]
    
    quotes = [
        '"This is definitely happening," confirmed Captain Obvious.',
        '"I am deeply concerned," said local concern-haver.',
        '"Well, that escalated," noted obvious observer.',
    ]
    
    details = [
        "Our team spent minutes on this story.",
        "Social media erupted in its usual fashion.",
        "Experts remain divided about dinner plans.",
    ]
    
    conclusions = [
        "More updates coming, probably.",
        "The nation watches, then checks TikTok.",
        "This concludes our coverage.",
    ]
    
    paragraphs = [f"<p><strong>BREAKING:</strong> {random.choice(openings)}</p>"]
    for q in random.sample(quotes, 2):
        paragraphs.append(f"<p>{q}</p>")
    for d in random.sample(details, 2):
        paragraphs.append(f"<p>{d}</p>")
    for c in conclusions:
        paragraphs.append(f"<p>{c}</p>")
    
    return "\n".join(paragraphs)

def create_article(headline):
    title = headline.upper() + " - SHOCKING EXCLUSIVE"
    slug = make_slug(headline) + ".html"
    date = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    image_url = get_image_url(headline)
    body = generate_content(headline)
    
    encoded_title = headline.replace(' ', '%20')
    encoded_url = f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
* {{margin:0; padding:0; box-sizing:border-box;}}
body {{font-family:Georgia,serif; background:#f5f5f5; padding:20px;}}
nav {{background:#333; padding:15px 0; margin-bottom:20px;}}
nav .container {{max-width:1000px; margin:0 auto; display:flex; justify-content:space-between; padding:0 20px;}}
nav a {{color:white; text-decoration:none; padding:10px 20px;}}
nav a:hover {{background:#555;}}
.logo {{font-weight:bold; color:#c00;}}
.container {{max-width:800px; margin:0 auto; background:white; padding:40px; box-shadow:0 2px 10px rgba(0,0,0,0.1);}}
h1 {{color:#c00; font-size:2.5em; margin-bottom:10px;}}
.meta {{color:#666; margin-bottom:30px; padding-bottom:20px; border-bottom:3px solid #c00;}}
img {{width:100%; margin-bottom:30px; border-radius:5px;}}
p {{font-size:1.1em; line-height:1.8; margin-bottom:20px;}}
.share-section {{margin:40px 0; padding:30px; background:#f9f9f9; text-align:center;}}
.share-buttons {{display:flex; justify-content:center; gap:15px; flex-wrap:wrap; margin-top:20px;}}
.share-btn {{padding:12px 24px; border-radius:6px; color:white; text-decoration:none; font-weight:bold;}}
.share-twitter {{background:#1DA1F2;}}
.share-facebook {{background:#1877F2;}}
.share-reddit {{background:#FF4500;}}
.back {{margin-top:40px; padding-top:20px; border-top:1px solid #ddd;}}
.back a {{color:#c00; text-decoration:none; font-weight:bold;}}
</style>
</head>
<body>
<nav>
<div class="container">
<a href="../index.html" class="logo">The Tabloid Times</a>
<div>
<a href="../about.html">About</a>
<a href="../contact.html">Contact</a>
<a href="../admin.html">Admin</a>
</div>
</div>
</nav>
<div class="container">
<h1>{title}</h1>
<div class="meta">{date}</div>
<img src="{image_url}" alt="News">
{body}
<div class="share-section">
<h3>Share This Story</h3>
<div class="share-buttons">
<a href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" target="_blank" class="share-btn share-twitter">Share on X</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank" class="share-btn share-facebook">Share on Facebook</a>
<a href="https://reddit.com/submit?url={encoded_url}&title={encoded_title}" target="_blank" class="share-btn share-reddit">Share on Reddit</a>
</div>
</div>
<div class="back"><a href="../index.html">← Back to All Stories</a></div>
</div>
</body>
</html>"""
    
    return {"title": title, "slug": slug, "date": date, "html": html, "image": image_url}

def create_homepage(articles):
    now = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    
    article_list = ""
    for art in articles:
        article_list += f"""
        <div class="story">
            <a href="articles/{art['slug']}">
                <img src="{art.get('image', 'https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=News')}" alt="Story">
            </a>
            <div class="story-content">
                <h2><a href="articles/{art['slug']}">{art['title']}</a></h2>
                <p class="date">{art['date']}</p>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Tabloid Times</title>
<style>
* {{margin:0; padding:0; box-sizing:border-box;}}
body {{font-family:Georgia,serif; background:#f5f5f5;}}
nav {{background:#333; padding:15px 0;}}
nav .container {{max-width:1000px; margin:0 auto; display:flex; justify-content:space-between; padding:0 20px;}}
nav a {{color:white; text-decoration:none; padding:10px 20px;}}
nav a:hover {{background:#555;}}
.logo {{font-weight:bold; color:#c00;}}
header {{background:#c00; color:white; padding:40px 20px; text-align:center; margin-bottom:30px;}}
h1 {{font-size:3.5em; text-transform:uppercase; text-shadow:3px 3px 0 #900;}}
.tagline {{font-size:1.2em; margin-top:10px; font-style:italic;}}
.container {{max-width:1000px; margin:0 auto; padding:20px;}}
.updated {{text-align:center; color:#666; margin-bottom:30px;}}
.story {{background:white; margin-bottom:30px; box-shadow:0 2px 5px rgba(0,0,0,0.1); overflow:hidden;}}
.story img {{width:100%; height:300px; object-fit:cover;}}
.story-content {{padding:30px;}}
.story h2 {{color:#c00; font-size:2em; margin-bottom:10px;}}
.story a {{color:#c00; text-decoration:none;}}
.story a:hover {{text-decoration:underline;}}
.date {{color:#666;}}
footer {{text-align:center; padding:40px 20px; color:#666; border-top:3px solid #c00; margin-top:40px;}}
</style>
</head>
<body>
<nav>
<div class="container">
<a href="index.html" class="logo">The Tabloid Times</a>
<div>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
<a href="admin.html">Admin</a>
</div>
</div>
</nav>
<header>
<h1>The Tabloid Times</h1>
<div class="tagline">SHOCKING NEWS - EXCLUSIVE STORIES - UNBELIEVABLE FACTS</div>
</header>
<div class="container">
<div class="updated">Last Updated: {now}</div>
{article_list}
</div>
<footer>
<p>All stories are 100% real and not made up at all. Okay, okay, it's AI generated satire.</p>
<p>&copy; 2026 The Tabloid Times</p>
</footer>
</body>
</html>"""
    
    return html

def create_about_page():
    return """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>About</title>
<style>
body {font-family:Georgia,serif; background:#f5f5f5; margin:0;}
nav {background:#333; padding:15px 0;}
nav .container {max-width:1000px; margin:0 auto; display:flex; justify-content:space-between; padding:0 20px;}
nav a {color:white; text-decoration:none; padding:10px 20px;}
.logo {font-weight:bold; color:#c00;}
.container {max-width:800px; margin:40px auto; background:white; padding:40px;}
h1 {color:#c00; margin-bottom:20px;}
p {line-height:1.8; margin-bottom:20px;}
</style></head>
<body>
<nav><div class="container">
<a href="index.html" class="logo">The Tabloid Times</a>
<div><a href="about.html">About</a><a href="contact.html">Contact</a><a href="admin.html">Admin</a></div>
</div></nav>
<div class="container">
<h1>About The Tabloid Times</h1>
<p>Welcome to The Tabloid Times, where truth meets satire!</p>
<p>We are an AI-powered satirical news site. Nothing here is real news. It's all satire and AI-generated silliness.</p>
</div></body></html>"""

def create_contact_page():
    return """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Contact</title>
<style>
body {font-family:Georgia,serif; background:#f5f5f5; margin:0;}
nav {background:#333; padding:15px 0;}
nav .container {max-width:1000px; margin:0 auto; display:flex; justify-content:space-between; padding:0 20px;}
nav a {color:white; text-decoration:none; padding:10px 20px;}
.logo {font-weight:bold; color:#c00;}
.container {max-width:600px; margin:40px auto; background:white; padding:40px;}
h1 {color:#c00; margin-bottom:20px;}
input,textarea {width:100%; padding:12px; margin-bottom:20px; border:1px solid #ddd; border-radius:4px;}
button {background:#c00; color:white; padding:15px 40px; border:none; border-radius:4px; cursor:pointer; font-weight:bold;}
.success {background:#4CAF50; color:white; padding:15px; margin-bottom:20px; border-radius:4px; display:none;}
</style></head>
<body>
<nav><div class="container">
<a href="index.html" class="logo">The Tabloid Times</a>
<div><a href="about.html">About</a><a href="contact.html">Contact</a><a href="admin.html">Admin</a></div>
</div></nav>
<div class="container">
<h1>Contact Us</h1>
<div class="success" id="msg">Message sent!</div>
<form id="form">
<input type="text" id="name" placeholder="Name" required>
<input type="email" id="email" placeholder="Email" required>
<textarea id="message" placeholder="Message" required></textarea>
<button type="submit">Send</button>
</form>
</div>
<script>
document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    const messages = JSON.parse(localStorage.getItem('tabloid_messages') || '[]');
    messages.unshift({
        id: Date.now(),
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value,
        date: new Date().toLocaleString()
    });
    localStorage.setItem('tabloid_messages', JSON.stringify(messages));
    document.getElementById('msg').style.display = 'block';
    this.reset();
    setTimeout(() => document.getElementById('msg').style.display = 'none', 3000);
};
</script>
</body></html>"""

def create_admin_config():
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD", "tabloid2026")
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return f"""const ADMIN_USERNAME_HASH = '{username_hash}';
const ADMIN_PASSWORD_HASH = '{password_hash}';
"""

def main():
    print("Starting generator...")
    os.makedirs("articles", exist_ok=True)
    
    headlines = fetch_news()
    archive = load_archive()
    new_articles = []
    
    for headline in headlines:
        article = create_article(headline)
        new_articles.append({
            "title": article["title"],
            "slug": article["slug"],
            "date": article["date"],
            "image": article["image"]
        })
        
        with open(f"articles/{article['slug']}", "w") as f:
            f.write(article["html"])
        print(f"Created: {article['slug']}")
    
    all_articles = new_articles + archive
    save_archive(all_articles)
    
    with open("index.html", "w") as f:
        f.write(create_homepage(all_articles))
    
    with open("about.html", "w") as f:
        f.write(create_about_page())
    
    with open("contact.html", "w") as f:
        f.write(create_contact_page())
    
    with open("admin-config.js", "w") as f:
        f.write(create_admin_config())
    
    print(f"Generated {len(new_articles)} articles")
    print(f"Total: {len(all_articles)}")
    print("Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())ervations.",
            "Stakeholders holding stakes gathered to discuss their stake-holding strategies.",
            "Focus groups focused while control groups controlled, results remain inconclusive.",
        ],
        [
            "Political figures from both sides immediately used this to support whatever they already believed.",
            "Activists activated their activism by posting strongly-worded Instagram stories.",
            "Influencers influenced absolutely nothing while gaining 50 followers.",
            "Thought leaders thought thoughts while leading nowhere in particular.",
        ],
        [
            "Polls show that 50% of people have one opinion while 50% have the opposite opinion, margin of error is 100%.",
            "Studies indicate that studies indicate things that require more studies.",
            "Research suggests that researchers need more research funding to research the research.",
            "Analysis of the analysis reveals that too much analysis causes analysis paralysis.",
        ],
        [
            "Concerned parents expressed concern to other concerned parents at their bi-weekly concern meeting.",
            "Youth activists realized they have homework due tomorrow and promised to resume activating later.",
            "Senior citizens wrote strongly worded letters that will never be read by anyone.",
            "Middle-aged folks posted minion memes about it on Facebook, consider activism complete.",
        ],
        [
            "Corporate sponsors released statement supporting both sides while offending nobody and standing for nothing.",
            "Non-profit organizations profited from the non-profit nature of their for-profit fundraising.",
            "Government officials governed unofficially by officially governing unofficial governance.",
            "Regulatory bodies regulated their body temperatures while regulating nothing else.",
        ],
        [
            "Breaking analysis: thing that happened is now being analyzed by analyzers who analyze things.",
            "Developing situation continues to develop developmentally in developing developments.",
            "Emerging trends emerge from emergency emergence of emergent emerging emergencies.",
            "Evolving narrative evolves as evolution of evolved evolution continues evolving.",
        ],
        [
            "At press time, nobody was still reading this far into the article.",
            "According to reports, reports continue to report on reportable reporting.",
            "Fact-checkers checked facts while fiction-writers checked out of reality completely.",
            "In a surprise twist, there was no twist, just more of the same thing we started with.",
        ],
    ]
    
    conclusions = [
        [
            "This story will continue to develop until everyone gets bored, estimated timeline: 48 hours.",
            "Experts predict experts will continue making predictions about things.",
            "More to come, assuming anything more actually comes, which it probably won't.",
        ],
        [
            "As events unfold, we'll be here to unfold the events as they fold and unfold.",
            "The situation remains fluid, mostly because nobody knows what's actually happening.",
            "Updates will be provided as soon as someone figures out what needs updating.",
        ],
        [
            "In conclusion, something happened, people reacted, and we're all moving on with our lives.",
            "The Tabloid Times will continue to provide comprehensive coverage until the next shiny thing appears.",
            "Developing story status: currently developed, future development questionable.",
        ],
        [
            "Stay tuned for our exclusive follow-up: 'Why Everyone Already Forgot About This.'",
            "Check back tomorrow when we'll pretend this was still important.",
            "This has been The Tabloid Times, where news goes to get roasted.",
        ],
        [
            "Officials promise thorough investigation, public promises to forget about this by lunch.",
            "Experts remain divided, mostly about what to have for dinner.",
            "The nation watches closely, then immediately checks TikTok.",
        ],
        [
            "And that's the way the news crumbles, cookie-style.",
            "Coming up next: absolutely nothing related to this story.",
            "In summary: stuff happened, people talked, nobody listened, the end.",
        ],
        [
            "The Tabloid Times: Making you feel better about your own life choices since 2026.",
            "For more hard-hitting journalism like this, continue scrolling to our other made-up stories.",
            "This concludes our coverage of something that will be completely irrelevant by this time tomorrow.",
        ],
        [
            "Remember: if you can't trust AI-generated satire, what CAN you trust? (Answer: nothing.)",
            "Thanks for reading this far. You must really have nothing better to do. Us neither.",
            "Tune in next time when we'll cover something equally meaningless with the same level of false importance.",
        ],
    ]
    
    opening = random.choice(openings)
    quotes = random.choice(quote_sets)
    details = random.choice(detail_sets)
    conclusion = random.choice(conclusions)
    
    paragraphs = [f"<p><strong>BREAKING:</strong> {opening}</p>"]
    
    content_blocks = list(quotes) + list(details)
    random.shuffle(content_blocks)
    
    num_blocks = random.randint(6, 10)
    for block in content_blocks[:num_blocks]:
        paragraphs.append(f"<p>{block}</p>")
    
    for line in conclusion:
        paragraphs.append(f"<p>{line}</p>")
    
    return "\n".join(paragraphs)

def create_article(headline):
    title = headline.upper() + " - SHOCKING EXCLUSIVE"
    slug = make_slug(headline) + ".html"
    date = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    image_url = get_image_url(headline)
    body = generate_unique_content(headline)
    
    encoded_title = headline.replace(' ', '%20').replace('&', '%26')
    encoded_url = f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}".replace(' ', '%20')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{margin: 0; padding: 0; box-sizing: border-box;}}
body {{font-family: Georgia, serif; background: #f5f5f5; padding: 20px;}}
nav {{background: #333; padding: 15px 0; margin-bottom: 20px;}}
nav .container {{max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px;}}
nav a {{color: white; text-decoration: none; padding: 10px 20px; font-size: 0.9em;}}
nav a:hover {{background: #555;}}
.logo {{font-weight: bold; font-size: 1.2em; color: #c00;}}
.container {{max-width: 800px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);}}
h1 {{color: #c00; font-size: 2.5em; margin-bottom: 10px; line-height: 1.2;}}
.meta {{color: #666; font-size: 0.9em; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #c00;}}
.featured-image {{width: 100%; height: auto; margin-bottom: 30px; border-radius: 5px;}}
p {{font-size: 1.1em; line-height: 1.8; margin-bottom: 20px;}}
.back {{margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;}}
.back a {{color: #c00; text-decoration: none; font-weight: bold;}}
.back a:hover {{text-decoration: underline;}}
.share-section {{margin: 40px 0; padding: 30px; background: #f9f9f9; border-radius: 8px; text-align: center;}}
.share-section h3 {{color: #333; margin-bottom: 20px; font-size: 1.5em;}}
.share-buttons {{display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;}}
.share-btn {{display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 6px; text-decoration: none; color: white; font-weight: bold; font-size: 0.95em; transition: transform 0.2s, box-shadow 0.2s; border: none; cursor: pointer;}}
.share-btn:hover {{transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2);}}
.share-twitter {{background: #1DA1F2;}}
.share-facebook {{background: #1877F2;}}
.share-linkedin {{background: #0A66C2;}}
.share-reddit {{background: #FF4500;}}
.share-email {{background: #666;}}
.share-copy {{background: #4CAF50;}}
.share-btn svg {{width: 20px; height: 20px; fill: white;}}
</style>
</head>
<body>
<nav>
<div class="container">
<a href="../index.html" class="logo">The Tabloid Times</a>
<div>
<a href="../about.html">About</a>
<a href="../contact.html">Contact</a>
<a href="../admin.html">Admin</a>
</div>
</div>
</nav>
<div class="container">
<h1>{title}</h1>
<div class="meta">{date}</div>
<img src="{image_url}" alt="Featured image" class="featured-image">
{body}

<div class="share-section">
<h3>Share This Ridiculous Story</h3>
<div class="share-buttons">
<a href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" target="_blank" class="share-btn share-twitter">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
Share on X
</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank" class="share-btn share-facebook">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
Share on Facebook
</a>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}" target="_b
if __name__ == "__main__":
    sys.exit(main())
