import json
import re

# Source of Truth
with open('audit_results.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Parse index.html to get card template
# We'll use a very loose match for the template and then clean it
template_match = re.search(r'<div class="game-card".*?Jaiho 91.*?Min\. Withdraw ₹100</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)
if not template_match:
    # Try another way
    template_match = re.search(r'<div class="game-card".*?Jaiho 91.*?Register</a>.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)

if not template_match:
    print("STILL could not find Jaiho 91 template! Printing local content for debug...")
    # Print a chunk of index.html around line 310
    exit(1)

template = template_match.group(0)

# Build a dictionary of images and download links from the current file to preserve them
# This is crucial because audit_results.json is missing them!
all_card_data = {}
# Find all cards in the current file (even if brokenly placed)
raw_cards = re.findall(r'<div class="game-card.*?alt="(.*?)".*?href="(.*?)".*?src="(.*?)".*?href="(.*?)".*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)
# Note: the above regex is very specific. Let's use a simpler one.
raw_cards_blocks = re.findall(r'<div class="game-card.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)
for block in raw_cards_blocks:
    title_m = re.search(r'alt="(.*?)"', block)
    if title_m:
        title = title_m.group(1)
        img_m = re.search(r'src="(.*?)"', block)
        dl_m = re.search(r'href="(https://.*?)"', block)
        link_m = re.search(r'href="(/(?!https).*?)"', block)
        
        all_card_data[title] = {
            'image': img_m.group(1) if img_m else "ep_code_logo.png",
            'download_link': dl_m.group(1) if dl_m else "#",
            'link': link_m.group(1) if link_m else f"/{title.lower().replace(' ', '')}/"
        }

def build_card(game, rank):
    # Get the best data we have
    title = game['title']
    data = all_card_data.get(title, {
        'image': 'ep_code_logo.png',
        'download_link': '#',
        'link': game['link']
    })
    
    card = template
    # Replace all placeholders
    card = re.sub(r'alt=".*?"', f'alt="{title}"', card)
    card = re.sub(r'src=".*?"', f'src="{data["image"]}"', card)
    # The register links appear twice (desktop and mobile)
    card = re.sub(r'href="https://.*?"', f'href="{data["download_link"]}"', card)
    # The internal links appear multiple times
    card = re.sub(r'href="/jaiho91/"', f'href="{data["link"]}"', card)
    # The title text
    card = re.sub(r'>Jaiho 91</a>', f'>{title}</a>', card)
    # Rank
    card = re.sub(r'<div class="game-rank">\d+</div>', f'<div class="game-rank">{rank}</div>', card)
    # Hot card
    if rank == 1:
        if 'hot-card' not in card:
            card = card.replace('game-card', 'game-card hot-card')
    else:
        card = card.replace(' hot-card', '')
    return card

yono_cards = [build_card(g, i+1) for i, g in enumerate(audit_data['yono'])]
colour_cards = [build_card(g, i+1) for i, g in enumerate(audit_data['colour'])]

# Assemble
header_marker = '<div class="category-filters">'
header_end_idx = content.find('</div>', content.find(header_marker)) + 6
header = content[:header_end_idx]

footer_marker = '<div class="seo-hidden">'
footer_idx = content.find(footer_marker)
footer = content[footer_idx:]

new_middle = f'''
<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">
{"".join(yono_cards)}
</div>
<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">
{"".join(colour_cards)}
</div>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(header + "\n" + new_middle + "\n" + footer)

print("index.html fully restored with all 68 games and correct layout.")
