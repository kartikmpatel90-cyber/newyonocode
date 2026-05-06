import os
import re

print("--- FINAL AUDIT START ---")

# 1. Check index.html structure
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

# Check Jaiho 91 in Yono section
yono_match = re.search(r'id="yono-apps-list".*?(<div class="game-card.*?</div>\s*</div>\s*</div>)', index, flags=re.DOTALL)
if yono_match:
    card1 = yono_match.group(1)
    if 'hot-card' in card1 and 'Jaiho 91' in card1 and 'Min. Withdraw' in card1:
        print("[PASS] Rank 1 (Jaiho 91) in Yono list is perfect.")
    else:
        print("[FAIL] Rank 1 in Yono list issue.")

# Check Rank 2 (YaarWin)
yaarwin_match = re.search(r'Rank">2</div>.*?YaarWin', index, flags=re.DOTALL)
if yaarwin_match:
    if 'hot-card' not in index[yaarwin_match.start():yaarwin_match.start()+500]:
        print("[PASS] Rank 2 (YaarWin) has no glow (correct).")
    else:
        print("[FAIL] Rank 2 has glow.")

# Check Colour List Duplicates/Yono
colour_start = index.find('id="colour-sites-list"')
if colour_start != -1:
    colour_section = index[colour_start:]
    yono_in_colour = re.findall(r'class="game-title">.*?Yono.*?</a>', colour_section, re.I)
    if not yono_in_colour:
        print("[PASS] No 'Yono' apps found in Colour section.")
    else:
        print(f"[FAIL] Found Yono apps in Colour section: {yono_in_colour}")

# 2. Check personal pages
failed_icons = []
all_slugs = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, 'index.html')) and d not in ['assets', '.gemini']]

for slug in all_slugs:
    with open(os.path.join(slug, 'index.html'), 'r', encoding='utf-8') as f:
        content = f.read()
        if 'ep_code_logo.png' in content and 'onerror' not in content:
            # Note: onerror uses ep_code_logo, but the main src should be different
            src_match = re.search(r'<img src="(.*?)"', content[content.find('app-hero'):])
            if src_match and 'ep_code_logo.png' in src_match.group(1):
                failed_icons.append(slug)
        
        if 'BACK TO ALL APPS' not in content:
            print(f"[FAIL] Home button missing in {slug}")

if not failed_icons:
    print(f"[PASS] All {len(all_slugs)} personal pages have unique icons.")
else:
    print(f"[FAIL] These pages still have placeholder icons: {failed_icons}")

print("--- FINAL AUDIT END ---")
