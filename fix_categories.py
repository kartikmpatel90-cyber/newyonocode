import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Move Promo Banner from Footer to Header
# Extract it from footer
banner_m = re.search(r'<a href="https://telegram.me/epcode".*?<img src="ep_code_banner.png".*?</a>', content, re.DOTALL)
if banner_m:
    banner_code = banner_m.group(0)
    # Remove from footer
    content = content.replace(banner_code, '')
    # Insert into header after the marquee (seo-banner)
    content = content.replace('</div>\n <!-- Rollable / Promotional Banner -->', 
                              f'</div>\n <div class="promo-banner-top" style="text-align:center; margin:10px 0;">{banner_code}</div>\n <!-- Rollable / Promotional Banner -->')

# 2. Fix Categorization: IN- 999 (to Colour) and Jaiho Win (to Yono)
# We'll find the cards and move them.
# Extract IN- 999 card
in999_m = re.search(r'<div class="game-card">.*?IN- 999.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)
# Extract Jaiho Win card
jaihowin_m = re.search(r'<div class="game-card">.*?Jaiho Win.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)

if in999_m and jaihowin_m:
    in999_card = in999_m.group(0)
    jaihowin_card = jaihowin_m.group(0)
    
    # Remove them from their original spots
    content = content.replace(in999_card, '')
    content = content.replace(jaihowin_card, '')
    
    # Re-insert in999 into colour-sites-list
    content = content.replace('<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">',
                              f'<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">\n{in999_card}')
                              
    # Re-insert jaihowin into yono-apps-list (maybe at the end of hot cards or top)
    # We'll just put it at the top of the yono list
    content = content.replace('<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">',
                              f'<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">\n{jaihowin_card}')

# 3. Final touch: Clean up any double spaces or empty lines created
content = re.sub(r'\n\s*\n', '\n', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Categorization fixed: IN- 999 moved to Colour, Jaiho Win moved to Yono. Banner moved to header.")
