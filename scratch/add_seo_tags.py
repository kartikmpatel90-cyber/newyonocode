import json
import re

# Load game data
with open('audit_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_titles = []
for game in data['yono']:
    all_titles.append(game['title'])
for game in data['colour']:
    all_titles.append(game['title'])

# Clean up titles for keywords
keywords = ", ".join(all_titles).lower()

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Meta Keywords
content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords}">', content)

# 2. Add Visible Tag Cloud in Footer
# We'll create a style for the tags first
tag_style = """
    .seo-tags-section { padding: 40px 20px; background: #f9f9f9; border-top: 1px solid #eee; text-align: center; }
    .seo-tags-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; max-width: 1000px; margin: 20px auto; }
    .seo-tag { display: inline-block; padding: 5px 12px; background: #fff; border: 1px solid #ddd; border-radius: 20px; font-size: 12px; color: #666; text-decoration: none; transition: 0.2s; }
    .seo-tag:hover { background: #007bff; color: #fff; border-color: #007bff; }
    .seo-title { font-size: 18px; font-weight: 700; color: #333; margin-bottom: 10px; }
"""

# Add style to head if not present
if '.seo-tags-section' not in content:
    content = content.replace('</style>', f'{tag_style}\n    </style>', 1)

# Generate tag cloud HTML
tags_html = ""
for title in all_titles:
    # Use lowercase slug for the link if it exists, or just #
    slug = title.lower().replace(" ", "")
    tags_html += f'<a href="/{slug}/" class="seo-tag">{title}</a> '

seo_section = f"""
    <div class="seo-tags-section">
        <h3 class="seo-title">Related Games & Tags</h3>
        <div class="seo-tags-container">
            {tags_html}
        </div>
    </div>
"""

# Insert before </body>
if '<div class="seo-tags-section">' not in content:
    content = content.replace('</body>', f'{seo_section}\n</body>')
else:
    # Update existing section
    content = re.sub(r'<div class="seo-tags-section">.*?</div>\s*</div>', seo_section, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SEO Keywords and Tags updated successfully.")
