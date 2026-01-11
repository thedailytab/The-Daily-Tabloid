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
        return ["Cat Elected Mayor", "Man Wins Lottery"]
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "articles" in data:
            titles = [a["title"] for a in data["articles"][:10] if a.get("title")]
            return random.sample(titles, min(2, len(titles)))
    except:
        pass
    return ["Breaking News", "Story Develops"]

def make_slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:50]

def get_image(headline):
    colors = ['FF6B6B', '4ECDC4', '45B7D1', 'FFA07A', '98D8C8', 'F7DC6F', 'BB8FCE', '85C1E2']
    color = colors[abs(hash(headline)) % len(colors)]
    # Use a more reliable image service
    return f"https://placehold.co/1200x600/{color}/ffffff?text=BREAKING+NEWS"

def make_article(headline):
    subject = headline.lower()
    
    # Stand-up comedy openings
    openings = [
        f"So you guys hear about this? {subject}. I mean, are you kidding me?",
        f"Alright, alright, settle down. So apparently {subject}. Yeah, I'll wait while you process that nonsense.",
        f"You know what I love? When {subject}. Said nobody ever.",
        f"Can we talk about this for a second? {subject}. I mean, who comes up with this stuff?",
        f"Okay, real talk: {subject}. And I'm supposed to act like this is normal?",
        f"Ladies and gentlemen, breaking news: {subject}. And the crowd goes mild!",
        f"So get this - {subject}. No seriously, I'm not making this up. I wish I was.",
        f"You're gonna love this one: {subject}. Actually, no you won't. Nobody does.",
        f"Alright, story time: {subject}. Are you ready for this level of absurdity?",
        f"Hold on, hold on. So {subject}. Yeah. That's where we are as a society.",
    ]
    
    # Comedy bits and observations
    bits = [
        "And of course, the 'experts' weighed in. You know, those people who are experts in having opinions about everything. Real helpful, guys.",
        "Social media had a meltdown, naturally. Because that's what we do now. Something happens, we panic-tweet. It's very productive.",
        "My favorite part? The people who said 'I saw this coming.' Really? You saw THIS coming? Then why didn't you warn the rest of us?",
        "Sources say they're 'monitoring the situation.' Translation: we have no idea what's happening but we're watching it happen.",
        "Witnesses described it as 'shocking.' Which is code for 'we literally can't believe we have to report on this.'",
        "Political figures rushed to make statements. Both sides. Saying opposite things. As usual. It's like watching a tennis match of terrible takes.",
        "One analyst called it 'unprecedented.' You know what else is unprecedented? Using the word unprecedented for every single thing that happens.",
        "They released a statement. A whole statement! Full of words that said absolutely nothing. It's an art form, really.",
        "The internet did what the internet does best: argued about it. Pro tip: nobody won. Nobody ever wins internet arguments.",
        "Experts predict this will have 'far-reaching implications.' Yeah, it'll reach far... into next week when everyone forgets about it.",
        "Someone called it 'a wake-up call.' Folks, if this is your wake-up call, you've been asleep for YEARS.",
        "They say it 'raises important questions.' The only question I have is: why am I still talking about this?",
        "Insiders claim they 'always knew.' Congrats on your hindsight, insiders. Super impressive.",
        "The official response was to 'look into it.' You know what that means? Nothing. That means absolutely nothing.",
        "People are demanding action. Which people? The same people who'll forget this happened by dinner time.",
    ]
    
    # Comedy closers
    closers = [
        "And that, ladies and gentlemen, is what passes for news these days. You're welcome for that migraine.",
        "So yeah, that happened. Will it matter tomorrow? Nope. Am I gonna keep talking about it? Also nope. Moving on!",
        "In conclusion: humans are weird, news is weirder, and I need a drink. Thank you, you've been a lovely audience!",
        "Anyway, that's my time. Remember: none of this matters and we're all gonna die someday. Goodnight!",
        "And that's the story. Was it worth your time? Debatable. Will I do it again tomorrow? Absolutely. I got bills to pay.",
        "So there you have it. Another day, another ridiculous headline. If you need me, I'll be questioning my life choices.",
        "And scene! That was today's episode of 'What The Heck Is Happening.' Tune in tomorrow for more chaos.",
        "Alright, I'm done. You guys have been great. The news has been terrible. Balance, you know?",
        "That's all I got for you today, folks. Same time tomorrow? Yeah, probably. This stuff writes itself.",
        "And with that, I bid you adieu. May your day be better than this news story. Low bar, but still.",
    ]
    
    # Build the stand-up routine
    opening = random.choice(openings)
    middle_bits = random.sample(bits, random.randint(4, 6))
    closer = random.choice(closers)
    
    # Add crowd work and callbacks
    crowd_work = [
        "You guys are laughing, but this is REAL. This actually happened. We live in a simulation, I swear.",
        "I can see some of you nodding. Yeah, you get it. You've seen the madness too.",
        "Some of you look confused. Don't worry, I'm confused too. We're all confused. Welcome to the club.",
        "That guy in the back is on his phone. Sir, this is important! Just kidding, it's not. Keep scrolling.",
    ]
    
    content = f"<p><strong>{opening}</strong></p>"
    content += f"<p>{random.choice(crowd_work)}</p>"
    
    for bit in middle_bits:
        content += f"<p>{bit}</p>"
    
    # Add a callback to the headline
    content += f"<p>But seriously, think about it: {subject}. That's the world we're living in. Let that sink in.</p>"
    content += f"<p>{closer}</p>"
    
    title = headline.upper() + " - COMEDY SPECIAL"
    slug = make_slug(headline) + ".html"
    date = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    img = get_image(headline)
    
    url = f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}"
    share_title = headline.replace(' ', '%20')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body{{font-family:Georgia,serif;background:#f5f5f5;margin:0;padding:20px}}
nav{{background:#333;padding:15px;margin-bottom:20px}}
nav a{{color:#fff;text-decoration:none;padding:10px 15px}}
.logo{{color:#c00;font-weight:bold}}
.main{{max-width:800px;margin:0 auto;background:#fff;padding:40px;border-left:5px solid #c00}}
h1{{color:#c00;font-size:2em;line-height:1.3}}
.comedy-tag{{background:#c00;color:#fff;padding:8px 16px;display:inline-block;margin:10px 0;font-size:0.9em;border-radius:4px}}
img{{width:100%;margin:20px 0;border-radius:8px;border:3px solid #c00}}
p{{line-height:1.9;margin:20px 0;font-size:1.15em;font-style:italic}}
p strong{{font-size:1.2em;color:#c00;font-style:normal}}
.share{{margin:40px 0;text-align:center;padding:30px;background:#f9f9f9;border-radius:8px}}
.btn{{display:inline-block;padding:12px 24px;margin:5px;background:#1DA1F2;color:#fff;text-decoration:none;border-radius:5px;font-weight:bold}}
</style>
</head>
<body>
<nav>
<a href="../index.html" class="logo">The Tabloid Times</a>
<a href="../about.html">About</a>
<a href="../contact.html">Contact</a>
<a href="../admin.html">Admin</a>
</nav>
<div class="main">
<div class="comedy-tag">🎤 STAND-UP COMEDY</div>
<h1>{title}</h1>
<p style="color:#666;font-style:normal">{date}</p>
<img src="{img}" alt="Breaking News">
{content}
<div class="share">
<h3 style="margin-bottom:20px">Share This Comedy Bit</h3>
<a href="https://twitter.com/intent/tweet?text={share_title}&url={url}" class="btn">Share on X</a>
<a href="https://facebook.com/sharer/sharer.php?u={url}" class="btn" style="background:#1877F2">Share on Facebook</a>
<a href="https://reddit.com/submit?url={url}&title={share_title}" class="btn" style="background:#FF4500">Share on Reddit</a>
</div>
<p style="text-align:center;font-style:normal"><a href="../index.html" style="color:#c00;font-weight:bold">← Back to More Comedy</a></p>
</div>
</body>
</html>"""
    
    return {"title": title, "slug": slug, "date": date, "html": html, "image": img}

def make_homepage(articles):
    now = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    items = ""
    for a in articles:
        img = a.get("image", "https://placehold.co/800x400/FF6B6B/ffffff?text=BREAKING+NEWS")
        items += f'<div class="story"><a href="articles/{a["slug"]}"><img src="{img}" onerror="this.src=\'https://placehold.co/800x400/FF6B6B/ffffff?text=NEWS\'"></a><h2><a href="articles/{a["slug"]}">{a["title"]}</a></h2><p>{a["date"]}</p></div>'
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>The Tabloid Times</title>
<style>
body{{font-family:Georgia,serif;background:#f5f5f5;margin:0}}
nav{{background:#333;padding:15px}}
nav a{{color:#fff;text-decoration:none;padding:10px 15px}}
.logo{{color:#c00;font-weight:bold}}
header{{background:#c00;color:#fff;padding:40px;text-align:center}}
h1{{font-size:3em;text-transform:uppercase}}
.main{{max-width:1000px;margin:0 auto;padding:20px}}
.story{{background:#fff;margin:20px 0;padding:20px}}
.story img{{width:100%;height:250px;object-fit:cover}}
.story h2{{color:#c00;margin:15px 0}}
.story a{{color:#c00;text-decoration:none}}
footer{{text-align:center;padding:40px;color:#666;border-top:3px solid #c00}}
</style>
</head>
<body>
<nav>
<a href="index.html" class="logo">The Tabloid Times</a>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
<a href="admin.html">Admin</a>
</nav>
<header>
<h1>The Tabloid Times</h1>
<p>SHOCKING NEWS - EXCLUSIVE STORIES</p>
</header>
<div class="main">
<p style="text-align:center;color:#666">Updated: {now}</p>
{items}
</div>
<footer>
<p>All stories are AI generated satire.</p>
<p>&copy; 2026 The Tabloid Times</p>
</footer>
</body>
</html>"""

def make_about():
    # Check if custom about content exists in a file
    custom_about_file = "about_custom.txt"
    if os.path.exists(custom_about_file):
        with open(custom_about_file, "r", encoding="utf-8") as f:
            custom_content = f.read()
    else:
        custom_content = "AI-powered satirical news. Nothing is real!"
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>About</title>
<style>
body{{font-family:Georgia,serif;background:#f5f5f5;margin:0}}
nav{{background:#333;padding:15px}}
nav a{{color:#fff;text-decoration:none;padding:10px 15px}}
.logo{{color:#c00}}
.main{{max-width:800px;margin:40px auto;background:#fff;padding:40px}}
h1{{color:#c00}}
p{{line-height:1.8;margin:15px 0}}
</style>
</head>
<body>
<nav>
<a href="index.html" class="logo">The Tabloid Times</a>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
<a href="admin.html">Admin</a>
</nav>
<div class="main">
<h1>About The Tabloid Times</h1>
{custom_content}
</div>
</body>
</html>"""

def make_contact():
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Contact</title>
<style>
body{font-family:Georgia,serif;background:#f5f5f5;margin:0}
nav{background:#333;padding:15px}
nav a{color:#fff;text-decoration:none;padding:10px 15px}
.logo{color:#c00}
.main{max-width:600px;margin:40px auto;background:#fff;padding:40px}
input,textarea{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd}
button{background:#c00;color:#fff;padding:15px 30px;border:none;cursor:pointer}
</style>
</head>
<body>
<nav>
<a href="index.html" class="logo">The Tabloid Times</a>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
<a href="admin.html">Admin</a>
</nav>
<div class="main">
<h1>Contact</h1>
<div id="msg" style="background:#4CAF50;color:#fff;padding:15px;display:none">Sent!</div>
<form id="f">
<input id="n" placeholder="Name" required>
<input id="e" type="email" placeholder="Email" required>
<textarea id="m" placeholder="Message" required></textarea>
<button>Send</button>
</form>
</div>
<script>
document.getElementById('f').onsubmit=function(ev){
ev.preventDefault();
var msgs=JSON.parse(localStorage.getItem('tabloid_messages')||'[]');
msgs.unshift({id:Date.now(),name:document.getElementById('n').value,email:document.getElementById('e').value,message:document.getElementById('m').value,date:new Date().toLocaleString()});
localStorage.setItem('tabloid_messages',JSON.stringify(msgs));
document.getElementById('msg').style.display='block';
this.reset();
setTimeout(function(){document.getElementById('msg').style.display='none'},3000)
};
</script>
</body>
</html>"""

def make_config():
    u = os.environ.get("ADMIN_USERNAME", "admin")
    p = os.environ.get("ADMIN_PASSWORD", "tabloid2026")
    uh = hashlib.sha256(u.encode()).hexdigest()
    ph = hashlib.sha256(p.encode()).hexdigest()
    return f"const ADMIN_USERNAME_HASH='{uh}';\nconst ADMIN_PASSWORD_HASH='{ph}';\n"

def main():
    print("Starting...")
    os.makedirs("articles", exist_ok=True)
    
    headlines = fetch_news()
    archive = load_archive()
    new = []
    
    for h in headlines:
        art = make_article(h)
        new.append({"title": art["title"], "slug": art["slug"], "date": art["date"], "image": art["image"]})
        with open(f"articles/{art['slug']}", "w") as f:
            f.write(art["html"])
        print(f"Created: {art['slug']}")
    
    all_articles = new + archive
    save_archive(all_articles)
    
    with open("index.html", "w") as f:
        f.write(make_homepage(all_articles))
    with open("about.html", "w") as f:
        f.write(make_about())
    with open("contact.html", "w") as f:
        f.write(make_contact())
    with open("admin-config.js", "w") as f:
        f.write(make_config())
    
    print(f"Done! {len(new)} new, {len(all_articles)} total")
    return 0

if __name__ == "__main__":
    sys.exit(main())
