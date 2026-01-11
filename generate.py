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
    
    # Generate unique roast content
    roasts = [
        f"Oh great, another thrilling update: {subject}. I'm sure this will change your life forever. Spoiler alert: it won't.",
        f"Breaking news that absolutely nobody asked for: {subject}. You're welcome for wasting 30 seconds of your day.",
        f"Hold the phone, folks: {subject}. And by 'hold the phone,' I mean put it down and go do literally anything else.",
        f"In news that will shock exactly zero people: {subject}. Moving on.",
        f"Alert the media! Oh wait, they already know: {subject}. And they're as unimpressed as you are.",
        f"Stop the presses for this earth-shattering development: {subject}. Just kidding, the presses stopped caring hours ago.",
        f"Here's something that happened: {subject}. Was it interesting? Debatable. Did we report it anyway? Obviously.",
        f"Exclusive scoop that you could've found on literally any news site: {subject}. But hey, you're here now.",
        f"In today's episode of 'Things That Technically Happened': {subject}. Tune in tomorrow for more riveting updates.",
        f"Brace yourself for this mind-blowing revelation: {subject}. And by mind-blowing, I mean incredibly predictable.",
    ]
    
    middle_roasts = [
        "Experts who are definitely real and not made up claim this is 'a thing that occurred.' Groundbreaking analysis, truly.",
        "Anonymous sources, who wish to remain anonymous because they value their reputation, confirm that yes, this happened.",
        "Industry insiders report they have insider knowledge about being inside the industry. Very insightful.",
        "Witnesses at the scene witnessed things at the scene where things were happening. Journalism at its finest.",
        "Social media erupted with the usual mixture of outrage, confusion, and people asking 'who cares?' Spoiler: nobody.",
        "Political figures from both sides immediately used this to support whatever nonsense they were already peddling.",
        "Analysts analyzed the situation analytically, concluding that analysis was needed. We need better analysts.",
        "Breaking: people had opinions about this. Those opinions ranged from 'meh' to 'super meh.' Democracy in action.",
        "The public responded with a collective shrug heard 'round the world. Or not heard. Because shrugs are silent.",
        "Think tanks thought about things in their tanks while the rest of us wondered why we're still reading this.",
    ]
    
    endings = [
        "This story will develop until everyone forgets about it. Estimated time: 6 minutes.",
        "Updates will follow if anything remotely interesting happens. Don't hold your breath.",
        "The Tabloid Times will continue coverage until something shinier catches our attention.",
        "In conclusion: stuff happened, people talked, nobody cared. See you tomorrow for more of the same.",
        "Stay tuned for our follow-up piece: 'Why This Story Doesn't Matter and Never Did.'",
        "This has been your daily dose of news you didn't need. You're welcome.",
        "And that's the way the cookie crumbles when nobody wanted cookies in the first place.",
        "More developments as they develop. Or don't. We'll report it either way.",
        "Check back never for updates on a story we've already forgotten about.",
        "The Tabloid Times: Making you question your life choices since 2026.",
    ]
    
    opening = random.choice(roasts)
    middle = random.sample(middle_roasts, 3)
    ending = random.choice(endings)
    
    content = f"<p><strong>BREAKING:</strong> {opening}</p>"
    for m in middle:
        content += f"<p>{m}</p>"
    content += f"<p>{ending}</p>"
    
    title = headline.upper() + " - EXCLUSIVE"
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
.main{{max-width:800px;margin:0 auto;background:#fff;padding:40px}}
h1{{color:#c00;font-size:2em}}
img{{width:100%;margin:20px 0;border-radius:8px}}
p{{line-height:1.8;margin:15px 0;font-size:1.1em}}
.share{{margin:30px 0;text-align:center}}
.btn{{display:inline-block;padding:10px 20px;margin:5px;background:#1DA1F2;color:#fff;text-decoration:none;border-radius:5px}}
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
<h1>{title}</h1>
<p style="color:#666">{date}</p>
<img src="{img}" alt="Breaking News">
{content}
<div class="share">
<a href="https://twitter.com/intent/tweet?text={share_title}&url={url}" class="btn">Share on X</a>
<a href="https://facebook.com/sharer/sharer.php?u={url}" class="btn" style="background:#1877F2">Facebook</a>
</div>
<p><a href="../index.html" style="color:#c00">← Back</a></p>
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
