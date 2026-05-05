import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the game card for "Goa Game" and update its image src
# The previous search showed: <h4 class="game-title">Goa Game</h4>
# And the image: <img src="logo_goa_game.png" alt="Goa Game" ...

# We'll search for the block that has alt="Goa Game" and update the src
content = re.sub(r'(<img[^>]*src=")[^"]*(" [^>]*alt="Goa Game")', r'\1logo_goagame.jpg\2', content, flags=re.I)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Goa Game logo.")
