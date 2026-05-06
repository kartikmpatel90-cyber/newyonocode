import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

yono_list = re.search(r'id="yono-apps-list".*?>(.*?)</div>\s*<div class="games-list" id="colour-sites-list"', content, flags=re.DOTALL)
colour_list = re.search(r'id="colour-sites-list".*?>(.*?)</div>\s*<div class="footer-marquee"', content, flags=re.DOTALL)

if yono_list:
    cards = re.findall(r'class="game-card"', yono_list.group(1))
    print(f"Yono Apps: {len(cards)}")
if colour_list:
    cards = re.findall(r'class="game-card"', colour_list.group(1))
    print(f"Colour Sites: {len(cards)}")
