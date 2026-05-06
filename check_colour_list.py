import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Colour Site section
start = content.find('id="colour-sites-list"')
if start != -1:
    # Find next section or end
    end = content.find('<div class="section-title"', start + 1)
    if end == -1: end = len(content)
    
    section_text = content[start:end]
    
    # Extract all titles
    titles = re.findall(r'class="game-title">.*?>(.*?)</a>', section_text)
    if not titles:
        # Try without the link wrap (just in case)
        titles = re.findall(r'class="game-title">(.*?)</h4>', section_text)
        
    print("Games in Colour Site List:")
    for t in titles:
        print(f"- {t}")
else:
    print("Could not find Colour Site section.")
