import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def extract_cards(list_id):
    start_tag = f'id="{list_id}"'
    start_idx = content.find(start_tag)
    if start_idx == -1: return []
    
    # Find the closing </div> of this list
    # We need to find the balanced closing div
    list_content_start = content.find('>', start_idx) + 1
    
    # Simple heuristic: cards are <div class="game-card"> ... </div> </div> </div>
    # We split by <div class="game-card"
    # But wait, the list itself ends with </div>
    # Let's find all card blocks
    # A card block usually ends with </div> </div> </div> or similar
    # Let's use re.findall with non-greedy match
    cards = re.findall(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', content[list_content_start:], re.DOTALL)
    
    # However, some cards might have different endings.
    # Let's refine the search within the list part
    # We find the next </div> that is NOT inside a card.
    
    return cards

yono_cards = extract_cards("yono-apps-list")
colour_cards = extract_cards("colour-sites-list")

print(f"Initial: Yono={len(yono_cards)}, Colour={len(colour_cards)}")

def get_title(card):
    m = re.search(r'class="game-title">.*?>(.*?)</a>', card)
    if not m: m = re.search(r'class="game-title">(.*?)</h4>', card)
    if not m: m = re.search(r'alt="(.*?)"', card)
    return m.group(1).strip() if m else ""

# Categorization
final_yono = []
final_colour = []

# Move requests:
# Remove from Colour: Jaiho 91, Club INR, Maha Games, Ind Club
to_remove_from_colour = ["jaiho91", "clubinr", "mahagames", "indclub"]
# Remove from Yono: OKWIN, Raja Luck
to_remove_from_yono = ["okwin", "rajaluck"]

# Process Yono list
for card in yono_cards:
    title = get_title(card)
    t_low = title.lower().replace(" ", "").replace("-", "")
    if t_low in to_remove_from_yono:
        final_colour.append(card)
    else:
        final_yono.append(card)

# Process Colour list
for card in colour_cards:
    title = get_title(card)
    t_low = title.lower().replace(" ", "").replace("-", "")
    if t_low in to_remove_from_colour:
        # Move to Yono if not already there
        # Check if already in final_yono
        if not any(t_low == get_title(c).lower().replace(" ", "").replace("-", "") for c in final_yono):
            final_yono.append(card)
        # Else, just drop from colour (already in yono)
    else:
        final_colour.append(card)

print(f"Final: Yono={len(final_yono)}, Colour={len(final_colour)}")

# Update ranks and construct HTML
def update_ranks(cards):
    updated = []
    for i, card in enumerate(cards):
        # Replace class="game-rank">...</div> with new rank
        new_card = re.sub(r'class="game-rank">\d+</div>', f'class="game-rank">{i+1}</div>', card)
        updated.append(new_card)
    return "\n".join(updated)

new_yono_html = update_ranks(final_yono)
new_colour_html = update_ranks(final_colour)

# Replace in content
# We need to find the exact boundaries to replace
def get_boundaries(list_id):
    start_tag = f'id="{list_id}"'
    start_idx = content.find(start_tag)
    list_content_start = content.find('>', start_idx) + 1
    
    # Find the end of the cards list (before the closing </div> of the list)
    # The last card ends with </div> </div> </div>
    # Let's find the last occurrence of that before the next big section or end of file
    # Or just search for the </div></div> that closes the list
    # In the file it was: </div></div><div class="games-list"
    
    # Let's use a simpler approach: replace everything between the start of first card and end of last card
    first_card_start = content.find('<div class="game-card"', list_content_start)
    # Find the last card's end
    # We look for the </div> that closes the list
    # For yono list, it's followed by <div class="games-list" id="colour-sites-list"
    if list_id == "yono-apps-list":
        end_idx = content.find('<div class="games-list" id="colour-sites-list"', first_card_start)
        # Go back to the </div> before it
        end_idx = content.rfind('</div>', 0, end_idx)
    else:
        # For colour list, it's followed by </div> or end of main
        end_idx = content.find('</main>', first_card_start)
        if end_idx == -1: end_idx = len(content)
        end_idx = content.rfind('</div>', 0, end_idx)
        
    return first_card_start, end_idx

y_start, y_end = get_boundaries("yono-apps-list")
content = content[:y_start] + new_yono_html + content[y_end:]

# Re-calculate colour boundaries because content changed length
c_start, c_end = get_boundaries("colour-sites-list")
content = content[:c_start] + new_colour_html + content[c_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully.")
