import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Function to remove duplicate game cards from a specific section
def remove_duplicates(html_content, section_id):
    section_start = html_content.find(f'id="{section_id}"')
    if section_start == -1: return html_content
    
    # Find next section or end of list
    next_section = html_content.find('<div class="section-title"', section_start + 1)
    if next_section == -1: next_section = len(html_content)
    
    section_text = html_content[section_start:next_section]
    
    # Split by game cards
    cards = re.split(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', section_text, flags=re.DOTALL)
    
    seen = set()
    new_cards = []
    
    for card in cards:
        if '<div class="game-card"' in card:
            title_match = re.search(r'class="game-title">(.*?)</h4>', card)
            if title_match:
                title = title_match.group(1).strip().lower().replace(" ", "").replace("-", "")
                if title in seen:
                    print(f"Removing duplicate: {title_match.group(1)}")
                    continue
                seen.add(title)
        new_cards.append(card)
    
    new_section_text = "".join(new_cards)
    return html_content[:section_start] + new_section_text + html_content[next_section:]

content = remove_duplicates(content, "yono-apps-list")
content = remove_duplicates(content, "colour-sites-list")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
