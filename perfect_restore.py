import json
import re

with open('audit_results.json', 'r') as f:
    data = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Separate all unique cards into a dictionary by title
all_entries = data['yono'] + data['colour']
seen_titles = set()
unique_entries = []

for e in all_entries:
    t = e['title'].strip()
    if t.lower() in seen_titles: continue
    seen_titles.add(t.lower())
    unique_entries.append(e)

# 2. Categorize strictly
yono_list = []
colour_list = []

colour_keywords = ['club', 'lottery', 'game', 'sikkim', 'goa', 'bdg', 'tiranga', '91', '55', '51', 'in-']
# But Jaiho 91 is a special case (Yono/Colour hybrid), user wants it Rank 1 in BOTH.

for e in unique_entries:
    t = e['title'].lower()
    is_colour = False
    for kw in colour_keywords:
        if kw in t:
            is_colour = True
            break
    
    # If it has "yono", "rummy", "slots", "patti", "spin", "winner", "jackpot" it's YONO
    yono_kws = ['yono', 'rummy', 'slots', 'patti', 'spin', 'winner', 'jackpot', 'bingo', '101', '777']
    for kw in yono_kws:
        if kw in t:
            is_colour = False
            break
            
    if is_colour:
        colour_list.append(e)
    else:
        yono_list.append(e)

# 3. Define the Card Generator (Premium Style)
def get_icon(title):
    # Try to find icon in existing content
    slug = re.sub(r'[^a-z0-9]', '', title.lower())
    m = re.search(f'/{slug}/.*?<img src="(.*?)"', content, flags=re.DOTALL)
    if m: return m.group(1)
    # Check common logos
    if "91club" in slug: return "logo_91club.jpeg"
    if "yaarwin" in slug: return "logo_yaarwin.jpg"
    if "jaiho91" in slug: return "logo_jaiho91.png"
    return f"logo_{slug}.png" # Fallback

def generate_card(entry, rank, is_hot=False):
    title = entry['title']
    link = entry['link']
    slug = re.sub(r'[^a-z0-9]', '', title.lower())
    icon = get_icon(title)
    hot_class = " hot-card" if is_hot else ""
    
    return f"""
    <div class="game-card{hot_class}">
        <div class="game-rank">{rank}</div>
        <div class="game-image"><a href="/{slug}/"><img src="{icon}" alt="{title}" onerror="this.src='ep_code_logo.png'" loading="lazy" width="100" height="100" style="border-radius:15px;"></a></div>
        <div class="game-details">
            <div class="game-info-desktop hidden-mobile">
                <h4 class="game-title"><a href="/{slug}/" style="text-decoration:none; color:inherit;">{title}</a></h4>
                <div class="game-meta-row">
                    <svg class="icon-gift" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M32 448c0 17.7 14.3 32 32 32h160V320H32v128zm256 32h160c17.7 0 32-14.3 32-32V320H288v160zm192-320h-42.1c6.2-12.1 10.1-25.5 10.1-40 0-48.5-39.5-88-88-88-41.6 0-68.5 21.3-103 68.3-34.5-47-61.4-68.3-103-68.3-48.5 0-88 39.5-88 88 0 14.5 3.8 27.9 10.1 40H32c-17.7 0-32 14.3-32 32v80c0 8.8 7.2 16 16 16h480c8.8 0 16-7.2 16-16v-80c0-17.7-14.3-32-32-32z"></path></svg>
                    Bonus ₹245
                </div>
                <div class="game-meta-row">
                    <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                    Min. Withdraw ₹100
                </div>
            </div>
            <div class="game-action-desktop hidden-mobile">
                <a href="{link}" target="_blank" class="btn-download">Register</a>
            </div>
            <div class="game-info-mobile hidden-desktop">
                <h4 class="game-title"><a href="/{slug}/" style="text-decoration:none; color:inherit;">{title}</a></h4>
                <div class="mobile-meta-row">
                    <a href="{link}" target="_blank" class="btn-download-mobile">REGISTER</a>
                    <div class="mobile-bonus-text">Bonus ₹245</div>
                </div>
                <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                    <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                    Min. Withdraw ₹100
                </div>
            </div>
        </div>
    </div>"""

# 4. Build Lists
def build_html_list(entries, list_id, is_yono):
    # Ensure Jaiho and Yaarwin are at top
    jaiho = next((e for e in unique_entries if "jaiho91" in e['title'].lower().replace(" ", "")), None)
    yaarwin = next((e for e in unique_entries if "yaarwin" in e['title'].lower().replace(" ", "")), None)
    
    rest = [e for e in entries if e != jaiho and e != yaarwin]
    
    html = f'<div class="games-list" id="{list_id}" style="display: {"block" if is_yono else "none"};">\n'
    rank = 1
    if jaiho:
        html += generate_card(jaiho, rank, is_hot=(is_yono))
        rank += 1
    if yaarwin:
        html += generate_card(yaarwin, rank, is_hot=False)
        rank += 1
    for e in rest:
        html += generate_card(e, rank, is_hot=False)
        rank += 1
    html += "</div>"
    return html

yono_html = build_html_list(yono_list, "yono-apps-list", True)
colour_html = build_html_list(colour_list, "colour-sites-list", False)

# 5. Full Assemble
# Get Header (keep it as is)
header_match = re.search(r'(<!DOCTYPE html>.*?)<div class="category-filters">', content, flags=re.DOTALL)
header = header_match.group(1) if header_match else content[:content.find('<div class="games-list"')]

# Add Filters
filters = """
 <div class="category-filters">
 <a href="?category=yono" class="btn-cat">Yono Apps</a>
 <a href="?category=colour" class="btn-cat">Colour Site</a>
 </div>
"""

# Get Footer
footer_match = re.search(r'(<div class="footer-marquee">.*</html>)', content, flags=re.DOTALL)
footer = footer_match.group(1) if footer_match else "</body></html>"

# Final CSS
css = """
    <style>
    .games-list { display: flex; flex-direction: column; gap: 15px; width: 100%; max-width: 800px; margin: 0 auto; min-height: 50vh; padding: 10px; }
    .game-card { display: flex; align-items: center; background: #fff; border: 1px solid #eee; border-radius: 15px; padding: 12px; position: relative; gap: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .game-rank { position: absolute; top: -8px; left: -8px; background: #d80000; color: #fff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 2px solid #fff; z-index: 5; }
    .game-image { width: 80px; height: 80px; flex-shrink: 0; }
    .game-image img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }
    .game-details { flex-grow: 1; }
    .game-title { margin: 0 0 5px 0; font-size: 18px; font-weight: 700; color: #333; }
    .game-meta-row { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #666; margin-bottom: 4px; }
    .game-meta-row svg { width: 14px; height: 14px; color: #009C18; }
    .btn-download { background: #007bff; color: #fff; padding: 8px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 14px; transition: 0.3s; }
    .btn-download:hover { background: #0056b3; }
    .btn-download-mobile { background: #007bff; color: #fff; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 700; }
    .hot-card { border: 2px solid #ff4757 !important; animation: glow 2s infinite alternate; background: #fff5f6 !important; }
    @keyframes glow { from { box-shadow: 0 0 5px #ff4757; } to { box-shadow: 0 0 20px #ff4757; } }
    .category-filters { display: flex; justify-content: center; gap: 10px; margin: 20px 0; }
    .btn-cat { padding: 10px 25px; border-radius: 10px; text-decoration: none; font-weight: 700; background: #eee; color: #333; transition: 0.3s; }
    .btn-cat:hover { background: #ddd; }
    @media (max-width: 768px) {
        .game-card { padding: 10px; gap: 10px; }
        .game-image { width: 65px; height: 60px; }
        .game-title { font-size: 15px; }
    }
    </style>
"""

# Inject CSS
if "</head>" in header:
    header = header.replace("</head>", css + "</head>")

final_html = header + filters + yono_html + colour_html + footer

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("PLATFORM COMPLETELY RESTORED AND OPTIMIZED.")
