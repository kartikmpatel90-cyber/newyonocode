import json
import re

# Load game data
with open('audit_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

yono_titles = [g['title'] for g in data['yono'][:10]]
colour_titles = [g['title'] for g in data['colour'][:10]]
top_titles = yono_titles + colour_titles

# Clean up titles for keywords
keywords = ", ".join(top_titles).lower()
keywords += ", yono games, yono code, colour prediction, earning app"

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Meta Keywords with a shorter version
content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords}">', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Meta keywords shortened for better loading speed.")
