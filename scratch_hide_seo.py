import json
import re

# Load all game names
with open('audit_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_titles = []
for game in data['yono']:
    all_titles.append(game['title'])
for game in data['colour']:
    all_titles.append(game['title'])

keywords_full = ", ".join(all_titles).lower()

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Meta Keywords (Full list for growth)
content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords_full}">', content)

# 2. Add SEO Hidden Styles
hidden_css = """
    .seo-hidden { position: absolute; left: -9999px; top: auto; width: 1px; height: 1px; overflow: hidden; }
"""
if '.seo-hidden' not in content:
    content = content.replace('</style>', f'{hidden_css}\n    </style>', 1)

# 3. Add Hidden SEO Section at bottom
seo_text = " ".join(all_titles)
# Add some variations for better SEO
seo_text += " All Yono Games, New Yono Apps, Yono Rummy Download, Best Colour Prediction Sites, Jaiho 91 App, YaarWin Official."

hidden_section = f'<div class="seo-hidden">{seo_text}</div>'

if '<div class="seo-hidden">' in content:
    content = re.sub(r'<div class="seo-hidden">.*?</div>', hidden_section, content)
else:
    content = content.replace('</body>', f'{hidden_section}\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SEO tags hidden but preserved for site growth.")
