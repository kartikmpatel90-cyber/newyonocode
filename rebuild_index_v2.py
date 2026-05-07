import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Identify the list containers
yono_start = content.find('id="yono-apps-list"')
yono_inner_start = content.find('>', yono_start) + 1
colour_start = content.find('id="colour-sites-list"')
colour_inner_start = content.find('>', colour_start) + 1
# End of colour list is before the seo-hidden div or body
colour_inner_end = content.find('<div class="seo-hidden">')
if colour_inner_end == -1: colour_inner_end = content.find('</body>')

# 2. Extract all cards as a list of strings
# We use a regex that matches from <div class="game-card to the next one or the end of the list
all_cards_raw = re.findall(r'<div class="game-card.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)

# 3. Clean each card to ensure it has EXACTLY 4 closing divs at the end and NO extra ones
cleaned_cards = []
for card in all_cards_raw:
    # Remove all trailing whitespace and divs
    cleaned = re.sub(r'(\s*</div>\s*)+$', '', card, flags=re.DOTALL)
    # Add exactly 4
    cleaned += '</div></div></div></div>'
    cleaned_cards.append(cleaned)

# 4. Now we need to know WHICH card goes in WHICH list
# We'll use the audit_results.json for that
import json
with open('audit_results.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

# Create a map of title -> cleaned_card
card_map = {}
for card in cleaned_cards:
    title_match = re.search(r'alt="(.*?)"', card)
    if title_match:
        title = title_match.group(1)
        card_map[title] = card

# 5. Rebuild the lists based on audit data
def rebuild_list(games):
    new_list = []
    for i, game in enumerate(games):
        title = game['title']
        if title in card_map:
            card = card_map[title]
            # Update rank
            card = re.sub(r'<div class="game-rank">.*?</div>', f'<div class="game-rank">{i+1}</div>', card)
            # Update hot-card class
            if i == 0:
                if 'hot-card' not in card:
                    card = card.replace('game-card', 'game-card hot-card')
            else:
                card = card.replace(' hot-card', '')
            new_list.append(card)
    return "\n".join(new_list)

yono_new = rebuild_list(audit_data['yono'])
colour_new = rebuild_list(audit_data['colour'])

# 6. Assemble the final content
header = content[:yono_inner_start]
# We need to find the gap between yono end and colour start
yono_end_tag = '</div>\n<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">'
footer = content[colour_inner_end:]

final_content = header + "\n" + yono_new + "\n" + yono_end_tag + "\n" + colour_new + "\n" + footer

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("index.html structure rebuilt and cleaned.")
