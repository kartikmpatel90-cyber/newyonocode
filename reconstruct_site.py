import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. EXTRACT ALL CARDS
# We use a non-greedy match to find all game-card blocks
all_cards = re.findall(r'<div class="game-card.*?</div>\s*</div>\s*</div>', content, flags=re.DOTALL)

print(f"Found {len(all_cards)} total cards.")

# 2. CATEGORIZE
yono_cards = []
colour_cards = []
seen = set()

def get_title(card):
    m = re.search(r'class="game-title">.*?>(.*?)</a>', card)
    if not m: m = re.search(r'class="game-title">(.*?)</h4>', card)
    if not m: m = re.search(r'alt="(.*?)"', card)
    return m.group(1).strip() if m else ""

for card in all_cards:
    title = get_title(card)
    if not title: continue
    t_low = title.lower().replace(" ", "")
    if t_low in seen: continue
    seen.add(t_low)
    
    # Check if it's Yono or Colour
    # If title has "yono" or icon is a yono icon
    is_yono = "yono" in t_low or "rummy" in t_low or "slots" in t_low or "teenpatti" in t_low
    
    if is_yono:
        yono_cards.append(card)
    else:
        colour_cards.append(card)

# Special Case: Jaiho 91 and YaarWin should be in BOTH but treated as primary
# Move them to a separate "Top" group
top_titles = ["jaiho91", "yaarwin"]
top_cards = []
final_yono = []
final_colour = []

for card in yono_cards + colour_cards:
    t = get_title(card)
    tl = t.lower().replace(" ", "")
    if tl in top_titles:
        top_cards.append(card)
    elif "yono" in tl or "rummy" in tl or "slots" in tl:
        final_yono.append(card)
    else:
        final_colour.append(card)

# 3. CONSTRUCT TEMPLATE
def create_standard_card(card, rank, is_hot=False):
    # Update rank
    card = re.sub(r'class="game-rank">\d+</div>', f'class="game-rank">{rank}</div>', card)
    # Update glow
    if is_hot:
        if 'hot-card' not in card:
            card = card.replace('class="game-card"', 'class="game-card hot-card"')
    else:
        card = card.replace(' hot-card', '')
    return card

def build_list(top, rest, list_id, is_yono):
    html = f'<div class="games-list" id="{list_id}" style="display: {"block" if is_yono else "none"};">\n'
    
    # Add top 2
    rank = 1
    # Find Jaiho 91 and YaarWin in top cards
    jaiho = next((c for c in top if "jaiho" in get_title(c).lower()), None)
    yaarwin = next((c for c in top if "yaarwin" in get_title(c).lower()), None)
    
    if jaiho:
        html += create_standard_card(jaiho, rank, is_hot=(rank==1 and is_yono))
        rank += 1
    if yaarwin:
        html += create_standard_card(yaarwin, rank, is_hot=False)
        rank += 1
        
    for c in rest:
        html += create_standard_card(c, rank, is_hot=False)
        rank += 1
    
    html += '</div>'
    return html

new_yono_html = build_list(top_cards, final_yono, "yono-apps-list", True)
new_colour_html = build_list(top_cards, final_colour, "colour-sites-list", False)

# 4. RE-ASSEMBLE
header_end = content.find('<div class="category-filters">')
if header_end == -1: header_end = content.find('<!-- Games List -->')
header = content[:header_end]

# Make sure category filters are there
filters = """
 <div class="category-filters">
 <a href="?category=yono" class="btn-cat">Yono Apps</a>
 <a href="?category=colour" class="btn-cat">Colour Site</a>
 </div>
"""

footer_start = content.find('<div class="footer-marquee">')
footer = content[footer_start:]

# Fix layout issues in CSS
css_fix = """
    <style>
    .games-list { display: flex; flex-direction: column; gap: 15px; width: 100%; max-width: 800px; margin: 0 auto; min-height: 100vh; padding: 10px; }
    .game-card { display: flex; align-items: center; background: #fff; border: 1px solid #eee; border-radius: 15px; padding: 12px; position: relative; gap: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .hot-card { border: 2px solid #ff4757 !important; animation: glow 2s infinite alternate; background: #fff5f6 !important; }
    @keyframes glow { from { box-shadow: 0 0 5px #ff4757; } to { box-shadow: 0 0 20px #ff4757; } }
    </style>
"""

# Re-insert CSS into header
if "</head>" in header:
    header = re.sub(r'<style>.*?</style>', '', header, flags=re.DOTALL) # Clean old styles
    header = header.replace("</head>", css_fix + "</head>")

final_html = header + filters + new_yono_html + new_colour_html + footer

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("COMPLETE RECONSTRUCTION SUCCESSFUL.")
