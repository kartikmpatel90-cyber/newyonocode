import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the first <div class="game-card and the matching end
# We'll just take from the first <div class="game-card" to the first occurrence of </div></div></div></div>
start_idx = content.find('<div class="game-card')
end_idx = content.find('</div></div></div></div>', start_idx) + 24
template = content[start_idx:end_idx]

print(f"Template found (length {len(template)}):")
print(template[:100] + "...")

# Source of Truth
with open('audit_results.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

# Extract data from current file
all_card_data = {}
blocks = re.findall(r'<div class="game-card.*?</div></div></div></div>', content, re.DOTALL)
for block in blocks:
    title_m = re.search(r'alt="(.*?)"', block)
    if title_m:
        title = title_m.group(1)
        img_m = re.search(r'src="(.*?)"', block)
        dl_m = re.search(r'href="(https?://.*?)"', block)
        link_m = re.search(r'href="(/(?!https).*?)"', block)
        all_card_data[title] = {
            'image': img_m.group(1) if img_m else "ep_code_logo.png",
            'download_link': dl_m.group(1) if dl_m else "#",
            'link': link_m.group(1) if link_m else f"/{title.lower().replace(' ', '')}/"
        }

def build_card(game, rank):
    title = game['title']
    data = all_card_data.get(title, {
        'image': 'ep_code_logo.png',
        'download_link': '#',
        'link': game['link']
    })
    card = template
    card = re.sub(r'alt=".*?"', f'alt="{title}"', card)
    card = re.sub(r'src=".*?"', f'src="{data["image"]}"', card)
    # Be more careful with link replacement to not destroy the structure
    # Replace the download link (it starts with http)
    card = re.sub(r'href="https?://.*?"', f'href="{data["download_link"]}"', card)
    # Replace internal links (they start with /)
    # We'll replace all occurrences of the template's link
    template_link_match = re.search(r'href="(/(?!https).*?)"', template)
    if template_link_match:
        template_link = template_link_match.group(1)
        card = card.replace(f'href="{template_link}"', f'href="{data["link"]}"')
    
    # Title text
    card = re.sub(r'>.*?</a></h4>', f'>{title}</a></h4>', card)
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

print("Done.")
