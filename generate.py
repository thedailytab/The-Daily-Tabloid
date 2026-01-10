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
            titles = [a["title"] for a in data["articles"][:10] if a.get("title")]
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
    colors = ['FF6B6B', '4ECDC4', '45B7D1', 'FFA07A', '98D8C8', 'F7DC6F', 'BB8FCE', '85C1E2']
    color_index = abs(hash(headline)) % len(colors)
    color = colors[color_index]
    return f"https://via.placeholder.com/1200x600/{color}/FFFFFF?text=Breaking+News"

def generate_unique_content(headline):
    """Generate truly varied and actually funny satirical content"""
    
    words = headline.lower().split()
    subject = ' '.join(words[:5]) if len(words) >= 5 else headline.lower()
    subject = re.sub(r'\s*-\s*(cnn|fox|abc|nbc|bbc|reuters).*$', '', subject, flags=re.IGNORECASE)
    
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
            '"I\'m not saying it was aliens, but..." suggested person definitely saying it was aliens.',
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
            '"They don\'t want you to know this," whispered conspiracy theorist with public YouTube channel.',
            '"The mainstream media won\'t cover this," posted person to mainstream media outlet.',
            '"I\'m just asking questions," said person absolutely not just asking questions.',
        ],
    ]
    
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
