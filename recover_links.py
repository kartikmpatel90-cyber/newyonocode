import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all cards
cards = re.findall(r'<div class="game-card".*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)

links_db = {}

for card in cards:
    title_m = re.search(r'alt="(.*?)"', card)
    if not title_m: continue
    title = title_m.group(1)
    
    # Internal link starts with /
    internal_m = re.search(r'href="(/(?!https).*?)"', card)
    internal_link = internal_m.group(1) if internal_m else f"/{title.lower().replace(' ', '')}/"
    
    # Download link starts with http
    download_m = re.search(r'href="(https?://.*?)"', card)
    download_link = download_m.group(1) if download_m else "#"
    
    # Image
    img_m = re.search(r'src="(.*?)"', card)
    image = img_m.group(1) if img_m else "ep_code_logo.png"
    
    links_db[title] = {
        'internal_link': internal_link,
        'download_link': download_link,
        'image': image
    }

with open('links_recovery.json', 'w') as f:
    json.dump(links_db, f, indent=2)

print(f"Extracted {len(links_db)} games from index.html.")
# Print some examples to verify
for title in list(links_db.keys())[:5]:
    print(f"{title}: {links_db[title]['download_link']}")
