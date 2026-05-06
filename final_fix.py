import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def final_fix(html):
    # 1. REMOVE ALL GLOWS
    html = html.replace('hot-card', '')
    
    # 2. ADD GLOW ONLY TO RANK 1 (YONO APPS)
    yono_start = html.find('id="yono-apps-list"')
    if yono_start != -1:
        first_card = html.find('class="game-card"', yono_start)
        if first_card != -1:
            html = html[:first_card] + 'class="game-card hot-card"' + html[first_card + len('class="game-card"'):]

    # 3. ADD WITHDRAWAL INFO (ROBUST)
    # Define the rows to add
    withdraw_row = """
                    <div class="game-meta-row">
                        <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                        Min. Withdraw ₹100
                    </div>"""
    
    mobile_withdraw = """
                            <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                                <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                                Min. Withdraw ₹100
                            </div>"""

    # We only apply this to Jaiho 91 and YaarWin in the Yono list
    # Splitting into cards
    cards = re.split(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', html, flags=re.DOTALL)
    
    new_cards = []
    for card in cards:
        if '<div class="game-card"' in card:
            # Check if it's Jaiho 91 or YaarWin
            if 'Jaiho 91' in card or 'YaarWin' in card:
                # Add withdrawal row if missing
                if 'Min. Withdraw' not in card:
                    # Desktop
                    card = re.sub(r'(<div class="game-action-desktop)', withdraw_row + r'\1', card)
                    # Mobile (insert before the last two closing divs of the details section)
                    # The structure is ...mobile-meta-row... </div> </div> </div>
                    card = re.sub(r'(</div>\s*</div>\s*</div>)$', mobile_withdraw + r'\1', card, flags=re.DOTALL)
        new_cards.append(card)
    
    html = "".join(new_cards)
    
    # 4. FIX COLOUR LIST TITLES
    # Ensure Colour List starts with a proper header and doesn't overlap
    # We already have separate lists. I will just make the transition clearer in CSS.
    
    return html

# Update CSS for Hot Card and List Spacing
css_patch = """
    <style>
    .hot-card { border: 2px solid #ff4757 !important; animation: glow 2s infinite alternate; background: #fff5f6 !important; }
    @keyframes glow { from { box-shadow: 0 0 5px #ff4757; } to { box-shadow: 0 0 20px #ff4757; } }
    .games-list { min-height: 100vh; padding-bottom: 50px; } /* Ensure list doesn't collapse */
    </style>
"""

# Apply the fixes
content = final_fix(content)
if "</head>" in content:
    # Remove old style patch if exists
    content = re.sub(r'<style>\s*\.hot-card.*?</style>', '', content, flags=re.DOTALL)
    content = content.replace("</head>", css_patch + "</head>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Final cleanup complete.")
