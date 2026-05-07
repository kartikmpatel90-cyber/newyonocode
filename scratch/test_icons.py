import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

card_pieces = re.split(r'<div class="game-card"', index_content)[1:]

def get_actual_icon(title):
    for piece in card_pieces:
        if f'class="game-title">{title}' in piece or f'alt="{title}"' in piece:
            img_match = re.search(r'<img src="(.*?)"', piece)
            if img_match:
                return img_match.group(1)
    return "ep_code_logo.png"

print(f"Ind Rummy icon: {get_actual_icon('Ind Rummy')}")
print(f"Yono Rummy icon: {get_actual_icon('Yono Rummy')}")
