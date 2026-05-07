import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def fix_list(list_id):
    start_marker = f'id="{list_id}"'
    start_idx = content.find(start_marker)
    if start_idx == -1: return content
    
    list_open_tag_end = content.find('>', start_idx) + 1
    
    # Find the end of this list div
    # Heuristic: the lists are separated by </div></div>
    # or followed by another games-list or footer
    if list_id == "yono-apps-list":
        end_idx = content.find('id="colour-sites-list"', list_open_tag_end)
        end_idx = content.rfind('</div></div>', 0, end_idx)
    else:
        end_idx = content.find('<div class="seo-tags-section">', list_open_tag_end)
        if end_idx == -1: end_idx = content.find('</body>', list_open_tag_end)
        end_idx = content.rfind('</div></div>', 0, end_idx)
        
    if end_idx == -1: return content

    list_inner = content[list_open_tag_end:end_idx]
    
    # Split by game-card start
    # We use a regex that looks for the card start and captures everything until the next card start or end of string
    cards_raw = re.split(r'(<div class="game-card.*?>)', list_inner)
    # pieces will be [garbage, tag1, content1, tag2, content2, ...]
    
    fixed_cards = []
    for i in range(1, len(cards_raw), 2):
        tag = cards_raw[i]
        inner = cards_raw[i+1]
        
        # Clean up ALL trailing </div> tags from inner to start fresh
        # We also remove whitespace
        inner_clean = re.sub(r'(\s*</div>\s*)+$', '', inner, flags=re.DOTALL)
        
        # Now we add the required closing tags
        # Based on analysis, we need:
        # 1. </div> for mobile-withdraw-text
        # 2. </div> for game-info-mobile
        # 3. </div> for game-details
        # 4. </div> for game-card
        # Total 4 tags.
        
        # Wait, let's verify if the inner actually HAS those tags open.
        # Simple counting of <div vs </div> in inner_clean
        opens = inner_clean.count('<div')
        closes = inner_clean.count('</div>')
        needed = opens - closes + 1 # +1 for the game-card itself which started in 'tag'
        
        fixed_card = tag + inner_clean + ("</div>" * needed)
        fixed_cards.append(fixed_card)
    
    new_list_inner = "\n".join(fixed_cards)
    
    return content[:list_open_tag_end] + "\n" + new_list_inner + "\n" + content[end_idx:]

# Apply fixes
new_content = fix_list("yono-apps-list")
content = new_content
new_content = fix_list("colour-sites-list")

# Also fix the CSS and display: block override
new_content = new_content.replace('id="yono-apps-list" style="display: block;"', 'id="yono-apps-list" class="games-list" style="display: flex; flex-direction: column;"')
new_content = new_content.replace('id="colour-sites-list" style="display: none;"', 'id="colour-sites-list" class="games-list" style="display: none; flex-direction: column;"')

# Ensure CSS in head is robust
# Remove the duplicate style blocks and replace with one clean one
css_replacement = """
    <style>
    .games-list { 
        display: flex; 
        flex-direction: column; 
        gap: 15px; 
        width: 100%; 
        max-width: 800px; 
        margin: 0 auto; 
        padding: 10px; 
        box-sizing: border-box;
    }
    .game-card { 
        display: flex !important; 
        flex-direction: row !important;
        align-items: center; 
        background: #fff; 
        border: 1px solid #eee; 
        border-radius: 15px; 
        padding: 12px; 
        position: relative; 
        gap: 15px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
        width: 100%;
        box-sizing: border-box;
        margin-bottom: 5px;
    }
    .game-rank { 
        position: absolute; 
        top: -8px; 
        left: -8px; 
        background: #d80000; 
        color: #fff; 
        width: 24px; 
        height: 24px; 
        border-radius: 50%; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: 12px; 
        font-weight: bold; 
        border: 2px solid #fff; 
        z-index: 5; 
    }
    .game-image { width: 80px; height: 80px; flex-shrink: 0; }
    .game-image img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }
    .game-details { flex-grow: 1; display: flex; flex-direction: row; align-items: center; justify-content: space-between; }
    .game-title { margin: 0 0 5px 0; font-size: 18px; font-weight: 700; color: #333; }
    
    .hot-card { border: 2px solid #ff4757 !important; animation: glow 2s infinite alternate; background: #fff5f6 !important; }
    @keyframes glow { from { box-shadow: 0 0 5px #ff4757; } to { box-shadow: 0 0 20px #ff4757; } }
    
    @media (max-width: 768px) {
        .game-card { padding: 10px; gap: 10px; }
        .game-image { width: 65px; height: 65px; }
        .game-title { font-size: 16px; }
        .game-details { flex-direction: column; align-items: flex-start; }
    }
    </style>
"""

# Find the old style blocks and replace them
# We'll just replace everything between the first <style> and last </style> in the head
style_start = new_content.find('<style>')
style_end = new_content.rfind('</style>', 0, new_content.find('</head>')) + 8
if style_start != -1 and style_end != -1:
    new_content = new_content[:style_start] + css_replacement + new_content[style_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("index.html layout and divs fixed successfully.")
