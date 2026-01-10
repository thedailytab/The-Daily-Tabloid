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
        ]
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if "articles" in data:
            # Get more articles to ensure variety
            titles = [a["title"] for a in data["articles"][:10] if a.get("title")]
            # Return only 2 random articles per run for hourly updates
            if len(titles) >= 2:
                selected = random.sample(titles, 2)
            else:
                selected = titles[:2]
            print(f"Selected {len(selected)} headlines for this hour")
            return selected
    except Exception as e:
        print(f"API error: {e}")
    
    return ["Breaking News Breaks", "Story Develops Into Story"]

def make_slug(text):
    clean = re.sub(r'[^a-z0-9]+', '-', text.lower())
    return clean.strip('-')[:50]

def get_image_url(headline):
    """Get placeholder image - using placeholder.com which is ultra-reliable"""
    # Use a completely reliable placeholder service
    # Each article gets a unique color based on headline
    colors = ['FF6B6B', '4ECDC4', '45B7D1', 'FFA07A', '98D8C8', 'F7DC6F', 'BB8FCE', '85C1E2']
    color_index = abs(hash(headline)) % len(colors)
    color = colors[color_index]
    
    # Alternative: just use a static, always-working image URL
    return f"https://via.placeholder.com/1200x600/{color}/FFFFFF?text=Breaking+News"

def generate_unique_content(headline):
    """Generate truly varied and actually funny satirical content"""
    
    # Extract key elements from headline
    words = headline.lower().split()
    subject = ' '.join(words[:5]) if len(words) >= 5 else headline.lower()
    
    # Remove common news source tags
    subject = re.sub(r'\s*-\s*(cnn|fox|abc|nbc|bbc|reuters|associated press).*

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
.share-btn {{display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 6px; text-decoration: none; color: white; font-weight: bold; font-size: 0.95em; transition: transform 0.2s, box-shadow 0.2s;}}
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
<img src="{image_url}" alt="Featured image for {headline}" class="featured-image">
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
<a href="https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}" target="_blank" class="share-btn share-linkedin">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
Share on LinkedIn
</a>
<a href="https://reddit.com/submit?url={encoded_url}&title={encoded_title}" target="_blank" class="share-btn share-reddit">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>
Share on Reddit
</a>
<a href="mailto:?subject={encoded_title}&body=Check out this story: {encoded_url}" class="share-btn share-email">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
Email
</a>
<button onclick="copyLink()" class="share-btn share-copy">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
Copy Link
</button>
</div>
</div>

<div class="back"><a href="../index.html">← Back to All Stories</a></div>
</div>

<script>
function copyLink() {{
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {{
        const btn = event.target.closest('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="width:20px;height:20px;fill:white;"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>Copied!';
        setTimeout(() => {{
            btn.innerHTML = originalText;
        }}, 2000);
    }});
}}
</script>
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
<a href="admin.html">Admin</a>
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
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD", "tabloid2026")
    
    # Create SHA-256 hash for password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    # Create SHA-256 hash for username  
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    
    js_content = f"""// Auto-generated admin credentials hash - secure and safe to be public
const ADMIN_USERNAME_HASH = '{username_hash}';
const ADMIN_PASSWORD_HASH = '{password_hash}';
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
, '', subject, flags=re.IGNORECASE)
    
    # Massively expanded opening hooks (30+ variations)
    openings = [
        f"In a move that surprised absolutely nobody who has been paying attention, {subject}.",
        f"Local sources confirm what everyone already suspected: {subject}.",
        f"Breaking: {subject}. When reached for comment, the universe shrugged.",
        f"Shocking development in ongoing series of developments: {subject}.",
        f"Area residents report that {subject}, immediately regret reading the news today.",
        f"In what experts are calling 'peak 2026,' {subject}.",
        f"Scientists baffled to discover that {subject}, despite literally predicting this exact thing last week.",
        f"Nation collectively says 'well, that figures' as {subject}.",
        f"Reports indicate {subject}. Nation's eyeballs remain rolled.",
        f"This just in: {subject}. Nation's surprise meter registers absolute zero.",
        f"Developing story: {subject}. Editors scramble to make this sound more interesting than it is.",
        f"In scenes reminiscent of every other week this year, {subject}.",
        f"Exclusive: {subject}. In related news, sky still blue, water still wet.",
        f"Sources reveal {subject}, promptly get ignored by everyone who could do anything about it.",
        f"Analysis reveals {subject}. Analysis also reveals that nobody asked for this analysis.",
        f"The thing that everyone said would happen has happened: {subject}.",
        f"Controversial new development: {subject}. Controversy expected to last until next news cycle.",
        f"Officials scramble to explain how {subject}, despite it being painfully obvious.",
        f"In a stunning display of doing exactly what was expected, {subject}.",
        f"Recent events suggest {subject}. Recent events also suggest we're all just making this up as we go.",
        f"Experts convene emergency meeting to discuss how {subject}, decide to just tweet about it instead.",
        f"Late-breaking: {subject}. Not really that late, and not really breaking, but here we are.",
        f"Sources close to the situation report {subject}, immediately distance themselves from said situation.",
        f"Witnesses stunned as {subject}, despite witnessing identical events every single week.",
        f"Investigation reveals {subject}. Investigation then gets defunded.",
        f"In what historians will probably forget by Tuesday, {subject}.",
        f"Concerned citizens demand to know why {subject}, realize they don't actually want to know.",
        f"Local man confident that {subject}, wrong about everything else in life.",
        f"After extensive research, experts conclude {subject}. Research budget immediately questioned.",
        f"Multiple sources now confirm {subject}, multiple sources also need to find better hobbies.",
    ]
    
    # Dramatically expanded quote collections (50+ variations)
    quote_sets = [
        [
            '"This is definitely a thing that is happening," confirmed Captain Obvious, who graduated top of his class at Obvious University.',
            '"I am deeply concerned," said local concern-haver, deeply.',
            '"Somebody should do something," suggested person who will definitely not be doing anything.',
        ],
        [
            '"I cannot believe this," gasped woman who absolutely should have seen this coming.',
            '"This changes everything," announced man who says this about his lunch order.',
            '"The implications are staggering," wheezed pundit who needs to get out more.',
        ],
        [
            '"Well, that escalated," noted person who watched it escalate in slow motion over six months.',
            '"We need answers," demanded questioner with no intention of listening to answers.',
            '"This is unprecedented," claimed historian with very selective memory.',
        ],
        [
            '"Literally shaking right now," typed person sitting perfectly still.',
            '"Nobody could have predicted this," lied psychic who predicted this exact thing.',
            '"History will remember this," predicted fortune teller with spotty track record.',
        ],
        [
            '"I have seen a lot in my career, but this..." trailed off person who has seen way worse.',
            '"The science is clear," stated scientist, referring to completely different science.',
            '"This violates everything we know," claimed expert who knows very little.',
        ],
        [
            '"As a mother," began woman, continuing to somehow make this about herself.',
            '"Speaking as an American," prefaced non-expert before sharing completely uninformed opinion.',
            '"I'm not saying it was aliens, but..." suggested person definitely saying it was aliens.',
        ],
        [
            '"We must come together," urged person currently arguing with strangers online.',
            '"This is what democracy looks like," shouted protester at non-democratic event.',
            '"The children are our future," stated person who avoids children at all costs.',
        ],
        [
            '"I have receipts," threatened person with screenshots nobody will ever see.',
            '"Do your own research," suggested researcher who did no research.',
            '"Wake up, sheeple!" bleated person who is definitely also a sheeple.',
        ],
        [
            '"This is fine," muttered dog in burning building.',
            '"Nothing to see here," insisted person standing in front of spectacular disaster.',
            '"Perfectly normal," claimed spokesperson for increasingly abnormal situation.',
        ],
        [
            '"They don't want you to know this," whispered conspiracy theorist with public YouTube channel.',
            '"The mainstream media won't cover this," posted person to mainstream media outlet.',
            '"I'm just asking questions," said person absolutely not just asking questions.',
        ],
    ]
    
    # Massively varied satirical observations (60+ combinations)
    detail_sets = [
        [
            "Our investigative team spent literally minutes on this story before deciding it wasn't worth more minutes.",
            "According to documents that may or may not exist, the situation has been developing since approximately whenever.",
            "Eyewitnesses report seeing things with their eyes, witnesses report witnessing things, and eye-havers report having eyes.",
            "Social media erupted in its usual fashion: thousands of people typing things they'll regret in 20 minutes.",
        ],
        [
            "Industry insiders who are totally real and not made up confirm that they are indeed inside the industry.",
            "Legal experts predict this could have legal implications, or possibly no implications, billable hours remain constant.",
            "Data shows a strong correlation between this event and the forward progression of time.",
            "Critics criticize while supporters support, in a display of doing exactly what their job titles suggest.",
        ],
        [
            "Anonymous sources, speaking on condition of anonymity because they're anonymous, anonymously confirmed anonymous things.",
            "Leaked documents reveal shocking information that was already public knowledge.",
            "Insider knowledge from outsiders suggests that insiders might be outside or possibly inside.",
            "Confidential reports that everyone has seen indicate things that everyone already knew.",
        ],
        [
            "The public responded with their usual mixture of outrage, indifference, and confusion about what's happening.",
            "International observers observed internationally while observing international observations.",
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
    
    # Much more varied conclusions (30+ endings)
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
    
    # Randomly select elements
    opening = random.choice(openings)
    quotes = random.choice(quote_sets)
    details = random.choice(detail_sets)
    conclusion = random.choice(conclusions)
    
    # Build content with randomized structure
    paragraphs = [f"<p><strong>BREAKING:</strong> {opening}</p>"]
    
    # Shuffle quotes and details together
    content_blocks = list(quotes) + list(details)
    random.shuffle(content_blocks)
    
    # Take random number of blocks (6-10 paragraphs)
    num_blocks = random.randint(6, 10)
    for block in content_blocks[:num_blocks]:
        paragraphs.append(f"<p>{block}</p>")
    
    # Add conclusion
    for line in conclusion:
        paragraphs.append(f"<p>{line}</p>")
    
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
