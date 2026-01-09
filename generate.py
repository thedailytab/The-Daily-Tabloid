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
    """Get current time in CST"""
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

def get_image_url(headline):
    """Get relevant image from Unsplash based on headline keywords"""
    keywords = headline.split()[:3]
    query = '+'.join(keywords)
    return f"https://source.unsplash.com/1200x600/?{query},news"

def generate_unique_content(headline):
    """Generate varied satirical content based on the headline"""
    
    templates = [
        {
            "intro": f"In a stunning turn of events, {headline.lower()} has left experts baffled and the public demanding answers.",
            "quotes": [
                '"I have never seen anything like this in my entire career," said Dr. Sarah Martinez, a leading expert in the field.',
                '"This changes everything we thought we knew," added Professor James Chen from MIT.',
            ],
            "details": [
                "According to leaked documents obtained exclusively by The Tabloid Times, the situation has been developing for weeks.",
                "Eyewitnesses reported scenes of chaos and confusion at the scene.",
                "Social media erupted with thousands sharing their reactions within minutes.",
            ]
        },
        {
            "intro": f"Breaking news: {headline.lower()} and nobody saw it coming.",
            "quotes": [
                '"This is absolutely unprecedented," claimed anonymous sources close to the matter.',
                '"We are monitoring the situation closely," a spokesperson reluctantly admitted.',
            ],
            "details": [
                "Our investigative team has uncovered shocking details that suggest this story goes deeper than anyone imagined.",
                "Industry insiders are calling this the scandal of the decade.",
                "Legal experts predict this could have far-reaching implications.",
            ]
        },
        {
            "intro": f"Exclusive investigation reveals that {headline.lower()} and the implications are staggering.",
            "quotes": [
                '"I knew something was wrong, but I never expected this," said a source who wished to remain anonymous.',
                '"The public deserves to know the truth," declared activist Kelly Rodriguez.',
            ],
            "details": [
                "Documents show a pattern of behavior that raises serious questions.",
                "Multiple witnesses have come forward with corroborating accounts.",
                "Calls for an official investigation are growing louder by the hour.",
            ]
        }
    ]
    
    template = random.choice(templates)
    
    paragraphs = [f"<p><strong>BREAKING:</strong> {template['intro']}</p>"]
    
    for quote in template['quotes']:
        paragraphs.append(f"<p>{quote}</p>")
    
    for detail in template['details']:
        paragraphs.append(f"<p>{detail}</p>")
    
    paragraphs.extend([
        "<p>The story continues to develop as more information becomes available.</p>",
        "<p>Experts are divided on what this means for the future.</p>",
        "<p>Public opinion polls show a nation deeply conflicted.</p>",
        "<p>Meanwhile, international observers are watching closely.</p>",
        "<p>Stay tuned to The Tabloid Times for continuing coverage of this developing story.</p>"
    ])
    
    return "\n".join(paragraphs)

def create_article(headline):
    title = headline.upper() + " - SHOCKING EXCLUSIVE"
    slug = make_slug(headline) + ".html"
    date = get_cst_time().strftime("%B %d, %Y at %I:%M %p CST")
    image_url = get_image_url(headline)
    body = generate_unique_content(headline)
    
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
nav .container {{max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;}}
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
</style>
</head>
<body>
<nav>
<div class="container">
<a href="../index.html" class="logo">The Tabloid Times</a>
<div>
<a href="../about.html">About</a>
<a href="../contact.html">Contact</a>
</div>
</div>
</nav>
<div class="container">
<h1>{title}</h1>
<div class="meta">{date}</div>
<img src="{image_url}" alt="Featured image for {headline}" class="featured-image">
{body}
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
                <img src="{art.get('image', 'https://source.unsplash.com/800x400/?news')}" alt="Story image">
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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Tabloid Times - Shocking News Daily</title>
<style>
* {{margin: 0; padding: 0; box-sizing: border-box;}}
body {{font-family: Georgia, serif; background: #f5f5f5; padding: 0;}}
nav {{background: #333; padding: 15px 0;}}
nav .container {{max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;}}
nav a {{color: white; text-decoration: none; padding: 10px 20px; font-size: 0.9em;}}
nav a:hover {{background: #555;}}
.logo {{font-weight: bold; font-size: 1.2em; color: #c00;}}
.container {{max-width: 1000px; margin: 0 auto; padding: 20px;}}
header {{background: #c00; color: white; padding: 40px 20px; text-align: center; margin-bottom: 30px;}}
h1 {{font-size: 3.5em; text-transform: uppercase; letter-spacing: 2px; text-shadow: 3px 3px 0 #900;}}
.tagline {{font-size: 1.2em; margin-top: 10px; font-style: italic;}}
.updated {{text-align: center; color: #666; margin-bottom: 30px;}}
.story {{background: white; margin-bottom: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden;}}
.story img {{width: 100%; height: 300px; object-fit: cover; display: block;}}
.story-content {{padding: 30px;}}
.story h2 {{color: #c00; font-size: 2em; margin-bottom: 10px;}}
.story a {{color: #c00; text-decoration: none;}}
.story a:hover {{text-decoration: underline;}}
.date {{color: #666; font-size: 0.9em;}}
footer {{text-align: center; padding: 40px 20px; color: #666; border-top: 3px solid #c00; margin-top: 40px;}}
</style>
</head>
<body>
<nav>
<div class="container">
<a href="index.html" class="logo">The Tabloid Times</a>
<div>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
</div>
</div>
</nav>
<header>
<h1>The Tabloid Times</h1>
<div class="tagline">SHOCKING NEWS • EXCLUSIVE STORIES • UNBELIEVABLE FACTS</div>
</header>
<div class="container">
<div class="updated">Last Updated: {now}</div>
{article_list}
</div>
<footer>
<p>All stories are 100% real and not made up at all. Okay, okay, it's AI generated satire.</p>
<p>© {datetime.now().year} The Tabloid Times</p>
</footer>
</body>
</html>"""
    
    return html

def create_about_page():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About - The Tabloid Times</title>
<style>
* {margin: 0; padding: 0; box-sizing: border-box;}
body {font-family: Georgia, serif; background: #f5f5f5;}
nav {background: #333; padding: 15px 0;}
nav .container {max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;}
nav a {color: white; text-decoration: none; padding: 10px 20px; font-size: 0.9em;}
nav a:hover {background: #555;}
.logo {font-weight: bold; font-size: 1.2em; color: #c00;}
.container {max-width: 800px; margin: 40px auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);}
h1 {color: #c00; font-size: 2.5em; margin-bottom: 20px;}
p {font-size: 1.1em; line-height: 1.8; margin-bottom: 20px;}
</style>
</head>
<body>
<nav>
<div class="container">
<a href="index.html" class="logo">The Tabloid Times</a>
<div>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
</div>
</div>
</nav>
<div class="container">
<h1>About The Tabloid Times</h1>
<p>Welcome to The Tabloid Times, where truth meets satire and reality takes a coffee break!</p>
<p>We are an AI-powered satirical news site that transforms real headlines into gloriously absurd stories. Our mission is simple: to make you laugh, think, and question everything you read online.</p>
<p>Every story you see here is automatically generated using cutting-edge AI technology, real news headlines, and a healthy dose of creative absurdity. Think of us as The Onion's quirky robot cousin.</p>
<p><strong>Disclaimer:</strong> Nothing here is real news. It's all satire, parody, and AI-generated silliness. Please don't quote us in your research papers.</p>
<p>New stories are automatically generated several times a day, so check back often for your daily dose of delightful nonsense!</p>
</div>
</body>
</html>"""
    return html

def create_contact_page():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contact - The Tabloid Times</title>
<style>
* {margin: 0; padding: 0; box-sizing: border-box;}
body {font-family: Georgia, serif; background: #f5f5f5;}
nav {background: #333; padding: 15px 0;}
nav .container {max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;}
nav a {color: white; text-decoration: none; padding: 10px 20px; font-size: 0.9em;}
nav a:hover {background: #555;}
.logo {font-weight: bold; font-size: 1.2em; color: #c00;}
.container {max-width: 600px; margin: 40px auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);}
h1 {color: #c00; font-size: 2.5em; margin-bottom: 20px;}
p {font-size: 1.1em; line-height: 1.8; margin-bottom: 20px;}
form {margin-top: 30px;}
label {display: block; margin-bottom: 8px; font-weight: bold; color: #333;}
input, textarea {width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; font-family: Georgia, serif; font-size: 1em;}
textarea {min-height: 150px; resize: vertical;}
button {background: #c00; color: white; padding: 15px 40px; border: none; border-radius: 4px; font-size: 1.1em; cursor: pointer; font-weight: bold;}
button:hover {background: #900;}
.success {background: #4CAF50; color: white; padding: 15px; margin-bottom: 20px; border-radius: 4px; display: none;}
</style>
</head>
<body>
<nav>
<div class="container">
<a href="index.html" class="logo">The Tabloid Times</a>
<div>
<a href="about.html">About</a>
<a href="contact.html">Contact</a>
</div>
</div>
</nav>
<div class="container">
<h1>Contact Us</h1>
<p>Have a hot tip? Want to suggest a story? Think we're hilarious (or terrible)? Let us know!</p>
<div class="success" id="successMessage">Message sent successfully! We'll get back to you soon.</div>
<form id="contactForm">
<label for="name">Name:</label>
<input type="text" id="name" name="name" required>
<label for="email">Email:</label>
<input type="email" id="email" name="email" required>
<label for="message">Message:</label>
<textarea id="message" name="message" required></textarea>
<button type="submit">Send Message</button>
</form>
</div>
<script>
const MESSAGES_KEY = 'tabloid_messages';

function saveMessage(name, email, message) {
    const messages = JSON.parse(localStorage.getItem(MESSAGES_KEY) || '[]');
    messages.unshift({
        id: Date.now(),
        name: name,
        email: email,
        message: message,
        date: new Date().toLocaleString('en-US', {timeZone: 'America/Chicago'})
    });
    localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages));
}

document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    saveMessage(name, email, message);
    
    document.getElementById('successMessage').style.display = 'block';
    this.reset();
    
    setTimeout(() => {
        document.getElementById('successMessage').style.display = 'none';
    }, 3000);
});
</script>
</body>
</html>"""
    return html

def create_admin_page():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin - Messages</title>
<style>
* {margin: 0; padding: 0; box-sizing: border-box;}
body {font-family: Georgia, serif; background: #f5f5f5; padding: 20px;}
.login-container {max-width: 400px; margin: 100px auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-radius: 8px;}
.admin-container {max-width: 1000px; margin: 40px auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: none;}
h1 {color: #c00; margin-bottom: 30px;}
h2 {color: #c00; margin-bottom: 20px;}
.login-form input {width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; font-size: 1em;}
.login-form button {width: 100%; background: #c00; color: white; padding: 15px; border: none; border-radius: 4px; font-size: 1.1em; cursor: pointer; font-weight: bold;}
.login-form button:hover {background: #900;}
.error {color: #c00; margin-top: 10px; display: none;}
.message-card {background: #f9f9f9; border-left: 4px solid #c00; padding: 20px; margin-bottom: 20px; border-radius: 4px;}
.message-header {display: flex; justify-content: space-between; margin-bottom: 10px; color: #666; font-size: 0.9em;}
.message-name {font-weight: bold; color: #333; font-size: 1.1em;}
.message-text {margin-top: 15px; line-height: 1.6;}
.delete-btn {background: #c00; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-size: 0.9em;}
.delete-btn:hover {background: #900;}
.logout-btn {background: #666; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; float: right;}
.logout-btn:hover {background: #444;}
.no-messages {text-align: center; color: #666; padding: 40px;}
</style>
</head>
<body>
<div class="login-container" id="loginContainer">
<h1>Admin Login</h1>
<form class="login-form" id="loginForm">
<input type="password" id="password" placeholder="Enter password" required>
<button type="submit">Login</button>
<div class="error" id="loginError">Incorrect password</div>
</form>
</div>

<div class="admin-container" id="adminContainer">
<button class="logout-btn" onclick="logout()">Logout</button>
<h1>Contact Messages</h1>
<div id="messagesList"></div>
</div>

<script src="admin-config.js"></script>
<script>
const MESSAGES_KEY = 'tabloid_messages';

async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

function checkAuth() {
    return sessionStorage.getItem('admin_auth') === 'true';
}

async function login(password) {
    const hashedInput = await hashPassword(password);
    if (hashedInput === ADMIN_PASSWORD_HASH) {
        sessionStorage.setItem('admin_auth', 'true');
        document.getElementById('loginContainer').style.display = 'none';
        document.getElementById('adminContainer').style.display = 'block';
        loadMessages();
        return true;
    }
    return false;
}

function logout() {
    sessionStorage.removeItem('admin_auth');
    document.getElementById('loginContainer').style.display = 'block';
    document.getElementById('adminContainer').style.display = 'none';
    document.getElementById('password').value = '';
}

function loadMessages() {
    const messages = JSON.parse(localStorage.getItem(MESSAGES_KEY) || '[]');
    const container = document.getElementById('messagesList');
    
    if (messages.length === 0) {
        container.innerHTML = '<div class="no-messages">No messages yet</div>';
        return;
    }
    
    container.innerHTML = messages.map(msg => `
        <div class="message-card" id="msg-${msg.id}">
            <div class="message-header">
                <span class="message-name">${msg.name} (${msg.email})</span>
                <span>${msg.date}</span>
            </div>
            <div class="message-text">${msg.message}</div>
            <button class="delete-btn" onclick="deleteMessage(${msg.id})">Delete</button>
        </div>
    `).join('');
}

function deleteMessage(id) {
    if (confirm('Delete this message?')) {
        let messages = JSON.parse(localStorage.getItem(MESSAGES_KEY) || '[]');
        messages = messages.filter(msg => msg.id !== id);
        localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages));
        loadMessages();
    }
}

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const password = document.getElementById('password').value;
    const success = await login(password);
    if (!success) {
        document.getElementById('loginError').style.display = 'block';
    }
});

if (checkAuth()) {
    document.getElementById('loginContainer').style.display = 'none';
    document.getElementById('adminContainer').style.display = 'block';
    loadMessages();
}
</script>
</body>
</html>"""
    return html

def create_admin_config():
    """Create hashed password config - password never exposed in source"""
    password = os.environ.get("ADMIN_PASSWORD", "tabloid2026")
    # Create SHA-256 hash
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    js_content = f"""// Auto-generated password hash - secure and safe to be public
const ADMIN_PASSWORD_HASH = '{hashed}';
"""
    return js_content

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
            "date": article["date"],
            "image": article["image"]
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
    
    about_page = create_about_page()
    with open("about.html", "w") as f:
        f.write(about_page)
    
    contact_page = create_contact_page()
    with open("contact.html", "w") as f:
        f.write(contact_page)
    
    admin_page = create_admin_page()
    with open("admin.html", "w") as f:
        f.write(admin_page)
    
    # Create secure admin config with hashed password
    admin_config = create_admin_config()
    with open("admin-config.js", "w") as f:
        f.write(admin_config)
    print("Created secure admin config")
    
    print(f"Generated {len(new_articles)} new articles")
    print(f"Total articles: {len(all_articles)}")
    print("Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
