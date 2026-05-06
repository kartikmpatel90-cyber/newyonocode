import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the sections
yono_section = re.search(r'id="yono-apps-list".*?</ul>', content, re.DOTALL)
colour_section = re.search(r'id="colour-sites-list".*?</ul>', content, re.DOTALL)

def extract_from_section(section_text):
    if not section_text:
        return []
    # Find all game cards
    cards = re.findall(r'<div class="game-card".*?</div>\s*</div>\s*</div>', section_text, re.DOTALL)
    results = []
    for card in cards:
        title_match = re.search(r'<div class="game-title">(.*?)</div>', card)
        link_match = re.search(r'href="(.*?)"', card)
        if title_match and link_match:
            results.append({
                'title': title_match.group(1).strip(),
                'link': link_match.group(1).strip()
            })
    return results

yono_apps = extract_from_section(yono_section.group(0) if yono_section else "")
colour_sites = extract_from_section(colour_section.group(0) if colour_section else "")

data = {'yono': yono_apps, 'colour': colour_sites}
with open('games_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Extracted {len(yono_apps)} yono apps and {len(colour_sites)} colour sites.")
