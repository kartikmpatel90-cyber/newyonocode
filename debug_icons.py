import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

card_pieces = re.split(r'<div class="game-card"', content)[1:]

def get_actual_icon(title):
    for piece in card_pieces:
        # Match title exactly between tags
        if re.search(r'>\s*' + re.escape(title) + r'\s*<', piece, re.IGNORECASE):
            img_match = re.search(r'<img src="(.*?)"', piece)
            if img_match:
                return img_match.group(1)
    return "ep_code_logo.png"

print(f"DEBUG: Jaiho 91 -> {get_actual_icon('Jaiho 91')}")
print(f"DEBUG: YaarWin -> {get_actual_icon('YaarWin')}")
print(f"DEBUG: Yono Rummy -> {get_actual_icon('Yono Rummy')}")
