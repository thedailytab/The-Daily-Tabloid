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
        return [
            {"title": "Cat Elected Mayor", "image": None},
            {"title": "Man Wins Lottery", "image": None}
        ]
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "articles" in data:
            articles = []
            for a in data["articles"][:10]:
                if a.get("title"):
                    articles.append({
                        "title": a["title"],
                        "image": a.get("urlToImage")  # Get the actual article image
                    })
            if len(articles) >= 2:
                return random.sample(articles, 2)
            return articles[:2]
    except:
        pass
    return [
        {"title": "Breaking News", "image": None},
        {"title": "Story Develops", "image": None}
    ]

def make_slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:50]

def get_image(headline, original_image=None):
    # Use original article image if available
    if original_image:
        return original_image
    
    # Fallback: Use site logo
    return "https://via.placeholder.com/1200x600/c00/ffffff?text=The+Tabloid+Times"

def make_article(headline, original_image=None):
    # Generate genuinely funny, unpredictable content
    # Each style is completely different
    
    styles = [
        # Style 1: Absurdist news report
        lambda h: f"""<p>URGENT: Local reality has temporarily malfunctioned. Officials confirm that {h.lower()} which, according to physics, shouldn't even be possible.</p>
<p>Dr. Gerald Fumblestick, who has never been right about anything, declared this "probably fine" while his lab coat was on fire.</p>
<p>"I've seen weirder things," claimed a man who definitely hasn't. "Like that time a potato became sentient. Wait, that didn't happen either."</p>
<p>The event attracted exactly three onlookers, two of whom were pigeons, and one who was deeply confused about where they parked.</p>
<p>In response, the government has decided to do what it does best: form a committee to discuss forming another committee.</p>
<p>Local Karen, who always has something to say, said something. We didn't write it down because honestly, who cares.</p>
<p>Scientists are baffled. But let's be real, scientists are always baffled. That's literally their whole thing.</p>
<p>This story will be forgotten by lunch. We're having tacos. You're not invited.</p>""",
        
        # Style 2: Conspiracy theorist's dream
        lambda h: f"""<p>THEY DON'T WANT YOU TO KNOW THIS: {h.lower()} - and it's ALL connected, man.</p>
<p>Wake up, sheeple! This is clearly related to that thing from 1987 that nobody remembers because it didn't happen.</p>
<p>One "anonymous insider" (who is definitely just some guy named Derek) leaked documents written in crayon claiming "the truth is out there." The truth is that Derek needs a hobby.</p>
<p>Coincidence? I THINK NOT. Also coincidentally, I failed statistics class three times.</p>
<p>If you rearrange the letters in "{h.lower()}" you get... well, you get those same letters in a different order. SUSPICIOUS.</p>
<p>The mainstream media won't cover this angle because they're too busy covering, you know, actual news.</p>
<p>Follow the money! Which leads to... a Wendy's parking lot. Huh. That's weird.</p>
<p>Stay woke. Or don't. Sleep is nice too. Actually, yeah, just get some sleep.</p>""",
        
        # Style 3: Old man yelling at cloud
        lambda h: f"""<p>BACK IN MY DAY we didn't have {h.lower()}. And we were FINE.</p>
<p>Now everyone's got their phones out, taking pictures, sharing it on the TikToks or whatever. Nobody talks anymore!</p>
<p>"It's unprecedented," they say. You know what was unprecedented? Walking uphill both ways to school in the snow. With wolves!</p>
<p>These young people today don't know how good they have it. We had to deal with actual problems, like... um... well I can't remember, but they were HARD.</p>
<p>And another thing - why is everyone so sensitive now? In my day, we just bottled up our emotions and developed weird personality quirks like normal people.</p>
<p>Mark my words, this'll blow over. Just like that internet thing. Whatever happened to that?</p>
<p>Now get off my lawn. I'm tired. Being angry is exhausting.</p>""",
        
        # Style 4: Overly dramatic Shakespeare
        lambda h: f"""<p>HARK! What light through yonder news break? 'Tis {h.lower()}, and the masses art shooketh.</p>
<p>To care, or not to care? That is the question. The answer is: probably not, but we're here anyway.</p>
<p>Methinks the lady doth protest too much about something completely unrelated. She really needs to stay on topic.</p>
<p>A pox upon this news! Though honestly, we're running low on poxes. Budget cuts, you understand.</p>
<p>The fault, dear reader, lies not in our stars, but in ourselves. And also in whoever decided this was newsworthy.</p>
<p>Friends, Romans, countrymen, lend me your ears! Actually, keep your ears. I was just being dramatic.</p>
<p>All the world's a stage, and this story is definitely not winning any Tonys.</p>
<p>Thus concludes our tale. *Takes dramatic bow* *Trips on own cape*</p>""",
        
        # Style 5: Sports commentary
        lambda h: f"""<p>AND HERE WE GO FOLKS! In a stunning display of things happening, {h.lower()}!</p>
<p>The crowd goes MILD! They're on their feet... to leave! What a moment!</p>
<p>"This changes everything," claims literally nobody with credibility. But you know what? That's never stopped us before!</p>
<p>Let's go to our expert analyst, Chad Broseph: "Yeah, uh, this is definitely a thing that occurred." Brilliant analysis, Chad.</p>
<p>INSTANT REPLAY: Yep, still happened. Still don't understand it. Moving on!</p>
<p>The opposing team has called a timeout to discuss their feelings. Very progressive, team. Very progressive.</p>
<p>With only seconds remaining in this news cycle, can anyone actually care enough to finish reading this? The answer may surprise you! (It won't.)</p>
<p>That's gonna be a MISS from the relevance meter! Better luck next time, story!</p>""",
        
        # Style 6: Nature documentary narrator
        lambda h: f"""<p>*David Attenborough voice* Here, in its natural habitat, we observe {h.lower()}.</p>
<p>Remarkable. The wild headline stalks its prey - your attention span - with calculated precision.</p>
<p>Watch as the news reporters gather, their camera shutters clicking in a symphony of manufactured urgency.</p>
<p>The alpha male of the group attempts to establish dominance by having the loudest opinion. It is... not working.</p>
<p>Fascinating. The herd mentality takes over as social media users copy and paste the same take seventeen thousand times.</p>
<p>Nature is truly... very stupid sometimes.</p>
<p>And here comes a predator - fact-checkers! The headline scatters, seeking refuge in alternative facts.</p>
<p>The circle of news continues. Tomorrow, none of this will matter. Such is the way of things.</p>""",
    ]
    
    # Pick a random style
    style_func = random.choice(styles)
    content = style_func(headline)
    
    title = headline.upper() + " - " + random.choice(["EXCLUSIVE", "BREAKING", "DEVELOPING", "SHOCKING", "UNBELIEVABLE"])
    slug = make_slug(headline) + ".html"
    date = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    img = get_image(headline, original_image)
    
    url = f"https://thedailytab.github.io/The-Daily-Tabloid/articles/{slug}"
    share_title = headline.replace(' ', '%20')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>{title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Georgia,serif;background:#f5f5f5;margin:0;padding:10px;font-size:16px}}
nav{{background:#333;padding:10px;margin-bottom:15px;border-radius:8px}}
nav a{{color:#fff;text-decoration:none;padding:8px 12px;font-size:0.9em;display:inline-block}}
.logo{{color:#c00;font-weight:bold;display:block;margin-bottom:8px}}
.main{{max-width:800px;margin:0 auto;background:#fff;padding:20px;border-radius:8px}}
h1{{color:#c00;font-size:1.5em;line-height:1.3;word-wrap:break-word}}
img{{width:100%;height:auto;margin:15px 0;border-radius:8px;display:block}}
p{{line-height:1.7;margin:15px 0;font-size:1em;word-wrap:break-word}}
.share{{margin:30px 0;text-align:center;padding:20px;background:#f9f9f9;border-radius:8px}}
.share h3{{font-size:1.2em;margin-bottom:15px}}
.btn{{display:inline-block;padding:10px 16px;margin:5px;background:#1DA1F2;color:#fff;text-decoration:none;border-radius:5px;font-weight:bold;font-size:0.9em}}
.comments{{margin:30px 0;padding:20px;background:#fff;border-top:3px solid #c00}}
.comments h2{{font-size:1.3em;margin-bottom:15px}}
.comment-form input,.comment-form textarea{{width:100%;padding:10px;margin:8px 0;border:1px solid #ddd;border-radius:4px;font-family:Georgia,serif;font-size:1em}}
.comment-form button{{background:#c00;color:#fff;padding:12px 24px;border:none;border-radius:4px;cursor:pointer;font-weight:bold;width:100%;font-size:1em}}
.comment{{background:#f9f9f9;padding:15px;margin:15px 0;border-radius:8px;border-left:4px solid #c00}}
.comment-author{{font-weight:bold;color:#c00;margin-bottom:8px;font-size:1em}}
.comment-date{{color:#666;font-size:0.85em;margin-bottom:8px}}
.comment-text{{line-height:1.6;word-wrap:break-word;font-size:0.95em}}
.no-comments{{text-align:center;color:#666;padding:30px;font-style:italic}}
@media (min-width: 768px){{
body{{padding:20px;font-size:18px}}
nav{{padding:15px}}
nav a{{font-size:1em;padding:10px 15px}}
.logo{{display:inline-block;margin-bottom:0}}
.main{{padding:40px}}
h1{{font-size:2em}}
p{{font-size:1.15em}}
.share h3{{font-size:1.4em}}
.btn{{padding:12px 24px;font-size:1em}}
.comment-form button{{width:auto}}
}}
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
<p style="color:#666;font-size:0.9em">{date}</p>
<img src="{img}" alt="Article Image" onerror="this.src='https://placehold.co/1200x600/FF6B6B/ffffff?text=Image+Unavailable'">
{content}
<div class="share">
<h3>Share This Insanity</h3>
<a href="https://twitter.com/intent/tweet?text={share_title}&url={url}" class="btn">X</a>
<a href="https://facebook.com/sharer/sharer.php?u={url}" class="btn" style="background:#1877F2">Facebook</a>
<a href="https://reddit.com/submit?url={url}&title={share_title}" class="btn" style="background:#FF4500">Reddit</a>
</div>
<div class="comments">
<h2>Comments</h2>
<div class="comment-form">
<input type="text" id="commentName" placeholder="Your Name" required>
<input type="email" id="commentEmail" placeholder="Your Email (won't be shown)" required>
<textarea id="commentText" placeholder="Your thoughts on this ridiculous story..." rows="4" required></textarea>
<button onclick="postComment()">Post Comment</button>
</div>
<div id="commentsList"></div>
</div>
<p style="text-align:center;margin-top:30px"><a href="../index.html" style="color:#c00;font-weight:bold;text-decoration:none">← Back</a></p>
</div>
<script>
const ARTICLE_ID = '{slug}';
const COMMENTS_KEY = 'comments_' + ARTICLE_ID;

function loadComments() {{
    const comments = JSON.parse(localStorage.getItem(COMMENTS_KEY) || '[]');
    const container = document.getElementById('commentsList');
    
    if (comments.length === 0) {{
        container.innerHTML = '<div class="no-comments">No comments yet. Be the first!</div>';
        return;
    }}
    
    container.innerHTML = comments.map(c => `
        <div class="comment">
            <div class="comment-author">${{c.name}}</div>
            <div class="comment-date">${{c.date}}</div>
            <div class="comment-text">${{c.text}}</div>
        </div>
    `).join('');
}}

function postComment() {{
    const name = document.getElementById('commentName').value.trim();
    const email = document.getElementById('commentEmail').value.trim();
    const text = document.getElementById('commentText').value.trim();
    
    if (!name || !email || !text) {{
        alert('Please fill in all fields!');
        return;
    }}
    
    const comments = JSON.parse(localStorage.getItem(COMMENTS_KEY) || '[]');
    comments.unshift({{
        name: name,
        text: text,
        date: new Date().toLocaleString('en-US', {{timeZone: 'America/Chicago'}})
    }});
    
    localStorage.setItem(COMMENTS_KEY, JSON.stringify(comments));
    
    document.getElementById('commentName').value = '';
    document.getElementById('commentEmail').value = '';
    document.getElementById('commentText').value = '';
    
    loadComments();
}}

loadComments();
</script>
</body>
</html>"""
    
    return {"title": title, "slug": slug, "date": date, "html": html, "image": img}

def make_homepage(articles):
    now = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    items = ""
    for a in articles:
        img = a.get("image", "https://via.placeholder.com/1200x600/c00/ffffff?text=The+Tabloid+Times")
        items += f'<div class="story"><a href="articles/{a["slug"]}"><img src="{img}" onerror="this.src=\'https://placehold.co/800x400/FF6B6B/ffffff?text=NEWS\'"></a><h2><a href="articles/{a["slug"]}">{a["title"]}</a></h2><p>{a["date"]}</p></div>'
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>The Tabloid Times</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Georgia,serif;background:#f5f5f5;margin:0;font-size:16px}}
nav{{background:#333;padding:10px}}
nav a{{color:#fff;text-decoration:none;padding:8px 12px;font-size:0.9em;display:inline-block}}
.logo{{color:#c00;font-weight:bold;display:block;margin-bottom:8px}}
header{{background:#c00;color:#fff;padding:30px 15px;text-align:center}}
h1{{font-size:2em;text-transform:uppercase;word-wrap:break-word}}
.tagline{{font-size:1em;margin-top:8px}}
.main{{max-width:1000px;margin:0 auto;padding:15px}}
.updated{{text-align:center;color:#666;margin-bottom:20px;font-size:0.9em}}
.story{{background:#fff;margin:15px 0;padding:15px;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}}
.story img{{width:100%;height:auto;object-fit:cover;border-radius:8px;margin-bottom:10px}}
.story h2{{color:#c00;font-size:1.3em;margin:10px 0;word-wrap:break-word;line-height:1.3}}
.story a{{color:#c00;text-decoration:none}}
.story a:hover{{text-decoration:underline}}
.date{{color:#666;font-size:0.85em;margin-top:8px}}
footer{{text-align:center;padding:30px 15px;color:#666;border-top:3px solid #c00;margin-top:30px}}
footer p{{margin:8px 0;font-size:0.9em}}
@media (min-width: 768px){{
nav{{padding:15px}}
nav a{{font-size:1em;padding:10px 15px}}
.logo{{display:inline-block;margin-bottom:0;margin-right:20px}}
header{{padding:40px 20px}}
h1{{font-size:3em}}
.tagline{{font-size:1.2em}}
.main{{padding:20px}}
.story{{padding:20px}}
.story img{{height:250px}}
.story h2{{font-size:2em}}
}}
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
<p class="tagline">SHOCKING NEWS - EXCLUSIVE STORIES</p>
</header>
<div class="main">
<p class="updated">Updated: {now}</p>
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
        custom_content = "<p>AI-powered satirical news. Nothing is real!</p>"
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>About</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Georgia,serif;background:#f5f5f5;margin:0;font-size:16px}}
nav{{background:#333;padding:10px}}
nav a{{color:#fff;text-decoration:none;padding:8px 12px;font-size:0.9em;display:inline-block}}
.logo{{color:#c00;font-weight:bold;display:block;margin-bottom:8px}}
.main{{max-width:800px;margin:20px auto;background:#fff;padding:20px;border-radius:8px}}
h1{{color:#c00;margin-bottom:15px;font-size:1.8em}}
p{{line-height:1.7;margin:12px 0;word-wrap:break-word}}
@media (min-width: 768px){{
nav{{padding:15px}}
nav a{{font-size:1em;padding:10px 15px}}
.logo{{display:inline-block;margin-bottom:0}}
.main{{margin:40px auto;padding:40px}}
h1{{font-size:2.5em}}
p{{line-height:1.8;margin:15px 0}}
}}
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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Contact</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,serif;background:#f5f5f5;margin:0;font-size:16px}
nav{background:#333;padding:10px}
nav a{color:#fff;text-decoration:none;padding:8px 12px;font-size:0.9em;display:inline-block}
.logo{color:#c00;font-weight:bold;display:block;margin-bottom:8px}
.main{max-width:600px;margin:20px auto;background:#fff;padding:20px;border-radius:8px}
h1{color:#c00;margin-bottom:15px;font-size:1.8em}
input,textarea{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:4px;font-family:Georgia,serif;font-size:1em}
textarea{min-height:120px}
button{background:#c00;color:#fff;padding:14px;border:none;border-radius:4px;cursor:pointer;width:100%;font-size:1em;font-weight:bold}
button:active{background:#900}
.success{background:#4CAF50;color:#fff;padding:15px;margin-bottom:15px;border-radius:4px;display:none}
@media (min-width: 768px){
nav{padding:15px}
nav a{font-size:1em;padding:10px 15px}
.logo{display:inline-block;margin-bottom:0}
.main{margin:40px auto;padding:40px}
h1{font-size:2.5em}
button{width:auto;padding:14px 30px}
}
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
<h1>Contact Us</h1>
<div id="msg" class="success">Message sent!</div>
<form id="f">
<input id="n" placeholder="Name" required>
<input id="e" type="email" placeholder="Email" required>
<textarea id="m" placeholder="Message" required></textarea>
<button type="submit">Send Message</button>
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
    
    for article_data in headlines:
        headline = article_data["title"]
        original_img = article_data.get("image")
        
        art = make_article(headline, original_img)
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
