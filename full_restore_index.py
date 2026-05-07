import json
import re

# Source of Truth
with open('audit_results.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Parse index.html to get card templates (using Jaiho 91 as template)
template_match = re.search(r'(<div class="game-card".*?Jaiho 91.*?</div>\s*</div>\s*</div>\s*</div>)', content, re.DOTALL)
if not template_match:
    print("Could not find Jaiho 91 template!")
    exit(1)

template = template_match.group(1)

def build_card(game, rank):
    card = template
    # Update title
    card = re.sub(r'alt=".*?"', f'alt="{game["title"]}"', card)
    card = re.sub(r'>.*?</a></h4>', f'>{game["title"]}</a></h4>', card)
    # Update links
    card = re.sub(r'href="/jaiho91/"', f'href="{game["link"]}"', card)
    card = re.sub(r'href="https://jaiho91\.cc/.*?"', f'href="{game["download_link"]}"', card)
    # Update image
    card = re.sub(r'src="logo_jaiho91\.png"', f'src="{game["image"]}"', card)
    # Update rank
    card = re.sub(r'<div class="game-rank">1</div>', f'<div class="game-rank">{rank}</div>', card)
    # Update hot-card
    if rank == 1:
        if 'hot-card' not in card:
            card = card.replace('game-card', 'game-card hot-card')
    else:
        card = card.replace(' hot-card', '')
    return card

yono_cards = [build_card(g, i+1) for i, g in enumerate(audit_data['yono'])]
colour_cards = [build_card(g, i+1) for i, g in enumerate(audit_data['colour'])]

# 2. Extract parts
header_end_marker = '<div class="category-filters">'
header_end_idx = content.find('</div>', content.find(header_end_marker)) + 6
header = content[:header_end_idx]

footer_start_marker = '<div class="seo-hidden">'
footer_start_idx = content.find(footer_start_marker)
footer = content[footer_start_idx:]

# 3. Assemble
new_lists = f'''
<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">
{"".join(yono_cards)}
</div>
<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">
{"".join(colour_cards)}
</div>
'''

final_content = header + "\n" + new_lists + "\n" + footer

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("index.html fully rebuilt with all apps restored.")
