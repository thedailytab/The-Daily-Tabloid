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
            {"title": "Cat Elected Mayor", "image": None, "url": None},
            {"title": "Man Wins Lottery", "image": None, "url": None}
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
                        "image": a.get("urlToImage"),
                        "url": a.get("url")  # Get original article URL
                    })
            if len(articles) >= 2:
                return random.sample(articles, 2)
            return articles[:2]
    except:
        pass
    return [
        {"title": "Breaking News", "image": None, "url": None},
        {"title": "Story Develops", "image": None, "url": None}
    ]

def make_slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:50]

def get_image(headline, original_image=None):
    # Use original article image if available
    if original_image:
        return original_image
    
    # Fallback: Use site logo
    return "https://via.placeholder.com/1200x600/c00/ffffff?text=The+Tabloid+Times"

def make_article(headline, original_image=None, original_url=None):
    # Generate Bill Burr-style roasts
    
    summary = f"Alright, so here's what happened: {headline.lower()}."
    
    # Bill Burr style roasts - angry, brutally honest, hilarious
    roasts = [
        f"Oh Jesus Christ, really? {headline.lower()}? This is what we're doing now? THIS is what's important?",
        f"So let me get this straight - {headline.lower()}. And everybody's acting like this matters. Are you KIDDING me?",
        f"You gotta be fu- you gotta be kidding me. {headline.lower()}. WHO CARES?!",
        f"{headline.upper()}! OH MY GOD! Can we just - can we STOP pretending like this is news?",
        f"Alright, alright, alright. So {headline.lower()}. And I'm supposed to give a shit about this? Really?",
        f"Here we go again. {headline.lower()}. Another day, another stupid story that doesn't matter.",
        f"Oh for Christ's sake. {headline.lower()}. This is what passes for journalism now?",
    ]
    
    commentary = [
        "Look, I'm not saying this isn't A thing. I'm saying it's not a thing WE need to care about. There's a difference!",
        "And everyone's got an opinion about it. EVERYONE. Like suddenly every moron with a phone is an expert.",
        "You know what kills me? The fact that we're talking about this instead of literally anything else that matters.",
        "The media's acting like this is the biggest story of the year. It's Tuesday! It's not even a good Tuesday!",
        "Here's the thing - and I love this - nobody actually cares. But we're all gonna pretend we do for like, 48 hours.",
        "And the comments! Oh my God, the COMMENTS. Everyone's got a hot take. Everyone thinks they're right. Nobody knows anything!",
        "You know what this reminds me of? Remember when we used to care about actual problems? Yeah, me neither.",
        "I'm watching this unfold and I'm thinking, 'This is it. This is what we've become. THIS is the pinnacle of human civilization.'",
        "The problem is nobody has anything better to do. So we just sit around caring about stuff that doesn't affect us AT ALL.",
        "And you know what the worst part is? Tomorrow there'll be something else. Some OTHER stupid thing. It never ends!",
    ]
    
    followup = [
        "So naturally, the 'experts' came out of the woodwork. Because of COURSE they did.",
        "People on Twitter are losing their minds. Which, let's be honest, they were gonna do anyway.",
        "Somebody called for an investigation. AN INVESTIGATION! Into THIS!",
        "The news is covering this 24/7. TWENTY. FOUR. SEVEN. Like there's nothing else happening in the world.",
        "And now politicians are weighing in. OH GREAT. Just what we needed - politicians' opinions on this.",
        "Social media's having a meltdown. Shocking. Absolutely shocking. Said no one.",
        "They're doing analysis on it. ANALYSIS! They got charts and graphs and everything. For THIS!",
        "Everyone's demanding answers. Answers to WHAT? What question are we even asking here?",
    ]
    
    rants = [
        "You know what I love? How we all act surprised. Like 'Oh no, I can't BELIEVE this happened!' Yeah you can. We all can.",
        "And here's the thing about people - they LOVE being outraged. They're ADDICTED to it. It's like crack for boring people.",
        "I'm watching all this and I'm thinking, 'We deserve everything that's coming to us. We absolutely deserve it.'",
        "Nobody's asking the real questions. Like 'Why am I still reading this?' That's a good question. I got nothing for you.",
        "The level of stupid here is just... *chef's kiss*. It's beautiful, really. In a horrifying way.",
        "And we wonder why nothing gets done in this country. THIS. This is why. Because we're focused on THIS!",
        "I'm not even mad anymore. I'm impressed. Impressed that we've reached this level of absurdity and just rolled with it.",
    ]
    
    closer = [
        "Anyway, that's the news. I'm gonna go drink now. You should too.",
        "And that's it. That's the story. Congratulations, you're dumber for having read it. You're welcome.",
        "Alright, I'm done. I can't - I can't talk about this anymore. It's too stupid. I'm out.",
        "So yeah. That happened. Check back tomorrow when something else stupid happens. Spoiler alert: it will.",
        "In conclusion: we're all doomed. Not because of this story. Just in general. Have a nice day!",
        "That's all I got. Now if you'll excuse me, I need to go question my life choices.",
    ]
    
    content = f"<p><strong>{summary}</strong></p>"
    content += f"<p>{random.choice(roasts)}</p>"
    content += f"<p>{random.choice(commentary)}</p>"
    content += f"<p>{random.choice(followup)}</p>"
    content += f"<p>{random.choice(rants)}</p>"
    content += f"<p>{random.choice(commentary)}</p>"
    content += f"<p>{random.choice(closer)}</p>"
    
    title = headline.upper() + " - " + random.choice(["EXCLUSIVE", "BREAKING", "DEVELOPING", "SHOCKING", "UNBELIEVABLE"])
    slug = make_slug(headline) + ".html"
    date = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    img = get_image(headline, original_image)
    
    # Create source link section
    source_link = ""
    if original_url:
        source_link = f'<p style="background:#f0f0f0;padding:15px;border-radius:8px;margin:20px 0"><strong>📰 Original Story:</strong> <a href="{original_url}" target="_blank" style="color:#c00;text-decoration:underline">Read the actual news article here</a></p>'
    
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
.login-prompt{{background:#fff3cd;padding:15px;border-radius:8px;margin-bottom:20px;border-left:4px solid #ffc107}}
.login-prompt a{{color:#c00;font-weight:bold;text-decoration:underline}}
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
<div>
<a href="../about.html">About</a>
<a href="../contact.html">Contact</a>
<a href="../login.html">Login</a>
<a href="../admin.html">Admin</a>
</div>
</nav>
<div class="main">
<h1>{title}</h1>
<p style="color:#666;font-size:0.9em">{date}</p>
{source_link}
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
<div id="loginPrompt" class="login-prompt" style="display:none">
Please <a href="../login.html">login</a> or <a href="../register.html">create an account</a> to comment.
</div>
<div class="comment-form" id="commentForm" style="display:none">
<textarea id="commentText" placeholder="Share your thoughts..." rows="4" required></textarea>
<button onclick="postComment()">Post Comment</button>
</div>
<div id="commentsList"></div>
</div>
<p style="text-align:center;margin-top:30px"><a href="../index.html" style="color:#c00;font-weight:bold;text-decoration:none">← Back</a></p>
</div>
<script>
const ARTICLE_ID = '{slug}';
const COMMENTS_KEY = 'comments_' + ARTICLE_ID;

function getCurrentUser() {{
    const user = localStorage.getItem('current_user');
    return user ? JSON.parse(user) : null;
}}

function checkLoginStatus() {{
    const user = getCurrentUser();
    if (user) {{
        document.getElementById('loginPrompt').style.display = 'none';
        document.getElementById('commentForm').style.display = 'block';
    }} else {{
        document.getElementById('loginPrompt').style.display = 'block';
        document.getElementById('commentForm').style.display = 'none';
    }}
}}

function loadComments() {{
    const comments = JSON.parse(localStorage.getItem(COMMENTS_KEY) || '[]');
    const container = document.getElementById('commentsList');
    
    if (comments.length === 0) {{
        container.innerHTML = '<div class="no-comments">No comments yet. Be the first!</div>';
        return;
    }}
    
    container.innerHTML = comments.map(c => `
        <div class="comment">
            <div class="comment-author">${{c.username}}</div>
            <div class="comment-date">${{c.date}}</div>
            <div class="comment-text">${{c.text}}</div>
        </div>
    `).join('');
}}

function postComment() {{
    const user = getCurrentUser();
    if (!user) {{
        alert('Please login to comment');
        window.location.href = '../login.html';
        return;
    }}
    
    const text = document.getElementById('commentText').value.trim();
    if (!text) {{
        alert('Please enter a comment!');
        return;
    }}
    
    const comments = JSON.parse(localStorage.getItem(COMMENTS_KEY) || '[]');
    comments.unshift({{
        username: user.username,
        text: text,
        date: new Date().toLocaleString('en-US', {{timeZone: 'America/Chicago'}})
    }});
    
    localStorage.setItem(COMMENTS_KEY, JSON.stringify(comments));
    document.getElementById('commentText').value = '';
    loadComments();
}}

checkLoginStatus();
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
<a href="login.html">Login</a>
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
<a href="login.html">Login</a>
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
<a href="login.html">Login</a>
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
        original_url = article_data.get("url")
        
        art = make_article(headline, original_img, original_url)
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
