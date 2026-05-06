import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

card_pieces = re.split(r'<div class="game-card"', index_content)[1:]

def get_actual_icon(title):
    for piece in card_pieces:
        if f'class="game-title">{title}</h4>' in piece or f'alt="{title}"' in piece:
            img_match = re.search(r'<img src="(.*?)"', piece)
            if img_match:
                return img_match.group(1)
    return "ep_code_logo.png"

print(f"Jaiho 91 icon: {get_actual_icon('Jaiho 91')}")
print(f"YaarWin icon: {get_actual_icon('YaarWin')}")
print(f"Yono Rummy icon: {get_actual_icon('Yono Rummy')}")
