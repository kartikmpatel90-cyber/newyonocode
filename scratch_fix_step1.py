import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the seo-tags-section
content = re.sub(r'<div class="seo-tags-section">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
# Fallback if the above doesn't match exactly
content = re.sub(r'<div class="seo-tags-section">.*?</body>', '</body>', content, flags=re.DOTALL)

# 2. Move IN- 999 to Colour list
# First, extract the IN- 999 card from yono list
in999_pattern = r'(<div class="game-card".*?IN- 999.*?</div>\s*</div>\s*</div>\s*</div>)'
match = re.search(in999_pattern, content, re.DOTALL)

if match:
    card_html = match.group(1)
    # Remove it from the current position
    content = content.replace(card_html, "")
    
    # Insert it into the colour list
    colour_list_marker = '<div class="games-list" id="colour-sites-list"'
    insertion_point = content.find('>', content.find(colour_list_marker)) + 1
    content = content[:insertion_point] + "\n" + card_html + content[insertion_point:]

# 3. Clean up the resulting code (remove extra whitespace/newlines)
content = re.sub(r'\n\s*\n', '\n', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("IN- 999 moved and footer tags removed.")
