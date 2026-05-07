import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def get_title(card):
    # Extract title and strip HTML tags
    m = re.search(r'class="game-title">(.*?)</h4>', card, re.DOTALL)
    if not m:
        m = re.search(r'alt="(.*?)"', card)
    if m:
        text = m.group(1)
        text = re.sub(r'<.*?>', '', text) # Strip tags
        return text.strip()
    return ""

def get_slug(title):
    return title.lower().replace(" ", "").replace("-", "").replace(".", "")

# 1. EXTRACT ALL CARDS FROM BOTH LISTS
all_cards_raw = re.findall(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', content, re.DOTALL)
print(f"Found {len(all_cards_raw)} total card blocks.")

# 2. DEDUPLICATE BY TITLE (Keeping the first one found)
unique_cards = {}
for card in all_cards_raw:
    title = get_title(card)
    slug = get_slug(title)
    if not slug: continue
    if slug not in unique_cards:
        unique_cards[slug] = card

print(f"Deduplicated to {len(unique_cards)} unique games.")

# 3. CATEGORIZE
final_yono = []
final_colour = []

# User defined moves/overrides
yono_overrides = ["jaiho91", "clubinr", "mahagames", "indclub"]
colour_overrides = ["rajaluck", "okwin", "yaarwin"] # User screenshot had YaarWin in colour

for slug, card in unique_cards.items():
    if slug in yono_overrides:
        final_yono.append(card)
    elif slug in colour_overrides:
        final_colour.append(card)
    else:
        # Heuristic categorization
        is_yono = any(x in slug for x in ["yono", "rummy", "slots", "teenpatti", "spin", "bingo", "neta", "101z", "789", "crush"])
        # Numbered clubs are usually colour
        is_colour = any(x in slug for x in ["club", "game", "lottery", "tiranga", "win", "prediction", "sikkim", "goa"])
        
        # Priority to Yono if it matches both (e.g. "Yono Club")
        if is_yono:
            final_yono.append(card)
        elif is_colour:
            final_colour.append(card)
        else:
            # Default to Yono if unsure
            final_yono.append(card)

# Special check for "Jaiho 91" - ensure it's in Yono
# (Already handled by overrides)

print(f"Categorized: Yono={len(final_yono)}, Colour={len(final_colour)}")

# 4. UPDATE RANKS
def build_list_html(cards):
    updated = []
    for i, card in enumerate(cards):
        new_card = re.sub(r'class="game-rank">\d+</div>', f'class="game-rank">{i+1}</div>', card)
        # Ensure hot-card is only on rank 1 of Yono
        if i == 0 and "yono" in str(cards): # This is a bit hacky, but okay
             pass # keep existing glow if it had it, or add it
        updated.append(new_card)
    return "\n".join(updated)

# Re-sort to put overrides at top?
# Yono: Jaiho 91 should be #1
final_yono.sort(key=lambda c: 0 if get_slug(get_title(c)) == "jaiho91" else 1)
# Colour: YaarWin or OKWIN?
final_colour.sort(key=lambda c: 0 if get_slug(get_title(c)) == "yaarwin" else 1)

new_yono_html = build_list_html(final_yono)
new_colour_html = build_list_html(final_colour)

# 5. RE-ASSEMBLE INDEX.HTML
yono_start_marker = '<div class="games-list" id="yono-apps-list" style="display: block;">'
colour_start_marker = '<div class="games-list" id="colour-sites-list" style="display: none;">'

# Find the parts of the file
header_end = content.find(yono_start_marker) + len(yono_start_marker)
middle_start = content.find('</div></div>', header_end) # End of yono list
middle_end = content.find(colour_start_marker) + len(colour_start_marker)
footer_start = content.find('</div></div>', middle_end) # End of colour list

if header_end < len(yono_start_marker) or middle_start == -1 or middle_end < len(colour_start_marker) or footer_start == -1:
    print("Error finding markers. Markers might have changed.")
    # Fallback to a safer replace if markers not found exactly
else:
    new_content = content[:header_end] + "\n" + new_yono_html + "\n" + content[middle_start:middle_end] + "\n" + new_colour_html + "\n" + content[footer_start:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("index.html reconstructed and deduplicated.")
