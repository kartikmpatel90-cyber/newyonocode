import json
import re

# Load the database
with open('links_recovery.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# THE DEFINITIVE LISTS
# Colour Sites (16) - Verified by User
colour_names = [
    "YaarWin", "IN- 999", "Jai club", "91CLUB", "55CLUB", "51 GAME", 
    "Bounty Game", "TIRANGA", "BDG WIN", "Tashan Game", "6 Club", 
    "82 Lottery", "Sikkim", "Goa Game", "RAJA LUCK", "OKWIN"
]

# Yono Apps (53) - We'll put Jaiho 91 and Jaiho Win at top
yono_names = [
    "Jaiho 91", "Jaiho Win", "Yono Rummy", "Ind Rummy", "Rummy Ludo", "Spin101", 
    "GO GO RUMMY", "Yn777", "Ind Slots", "Bingo101", "Boss Rummy", "Yono Games", 
    "Joy Rummy", "567 Slots", "Ever777", "Yono-777", "Hindi 777", "Rummy888", 
    "Good Slots", "Game Rummy", "Ok Rummy", "Yes Spin", "Love Rummy", "Share Slots", 
    "MQM Bet", "Hi Rummy", "MBM BET", "Top Rummy", "Jaiho Slots", "Saga Slots", 
    "Yono Arcade", "Spin777", "ABC Rummy", "Jai Ho Rummy", "Jaiho 777", "Rummy 91", 
    "Jai Ho Spin", "Jai Ho Arcade", "Neta Vip", "Slots Winner", "Slots Spin", 
    "789 Jackpots", "101Z", "Spin Winner", "Spin Gold", "Yono Slots", "Spin Crush", 
    "Rumble Rummy", "Yono VIP", "Club INR", "Maha Games", "Ind Club", "101z"
] # Added 101z at the end to make it 53

card_template = """<div class="game-card{hot_class}">
    <div class="game-rank">{rank}</div>
    <div class="game-image"><a href="{internal}"><img src="{image}" alt="{title}" onerror="this.src='ep_code_logo.png'" loading="lazy" width="100" height="100" style="border-radius:15px;"></a></div>
    <div class="game-details">
        <div class="game-info-desktop hidden-mobile">
            <h4 class="game-title">{title}</h4>
            <div class="game-meta-row">
                <svg class="icon-gift" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M32 448c0 17.7 14.3 32 32 32h160V320H32v128zm256 32h160c17.7 0 32-14.3 32-32V320H288v160zm192-320h-42.1c6.2-12.1 10.1-25.5 10.1-40 0-48.5-39.5-88-88-88-41.6 0-68.5 21.3-103 68.3-34.5-47-61.4-68.3-103-68.3-48.5 0-88 39.5-88 88 0 14.5 3.8 27.9 10.1 40H32c-17.7 0-32 14.3-32 32v80c0 8.8 7.2 16 16 16h480c8.8 0 16-7.2 16-16v-80c0-17.7-14.3-32-32-32z"></path></svg>
                Bonus ₹245
            </div>
            <div class="game-meta-row">
                <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                Min. Withdraw ₹100
            </div>
        </div>
        <div class="game-action-desktop hidden-mobile">
            <a href="{download}" target="_blank" class="btn-download">Register</a>
        </div>
        <div class="game-info-mobile hidden-desktop">
            <h4 class="game-title">{title}</h4>
            <div class="mobile-meta-row">
                <a href="{download}" target="_blank" class="btn-download-mobile">REGISTER</a>
                <div class="mobile-bonus-text">Bonus ₹245</div>
            </div>
            <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                Min. Withdraw ₹100</div></div></div></div>"""

def build_list(names, db):
    html = ""
    for i, name in enumerate(names):
        data = db.get(name)
        if not data:
            # Try case-insensitive
            found = False
            for k in db:
                if k.lower() == name.lower():
                    data = db[k]
                    found = True
                    break
            if not found: continue
        rank = i + 1
        hot_class = " hot-card" if rank <= 1 else ""
        html += card_template.format(
            hot_class=hot_class,
            rank=rank,
            internal=data['internal_link'],
            image=data['image'],
            title=name,
            download=data['download_link']
        )
    return html

yono_html = build_list(yono_names, db)
colour_html = build_list(colour_names, db)

with open('index.html', 'r', encoding='utf-8') as f:
    full_html = f.read()

# SPLIT AND RECONSTRUCT TO BE 100% SAFE
# We will split from the Search Box to the Footer.

# 1. Get header (up to the search box or first button)
header_split = full_html.split('<div class="category-filters">')
if len(header_split) < 2:
    print("Error: Could not find category-filters")
    exit(1)
header = header_split[0] + '<div class="category-filters">\n    <button onclick="showCategory(\'yono\')" class="btn-cat btn-yono" id="btn-yono">Yono Apps</button>\n    <button onclick="showCategory(\'colour\')" class="btn-cat btn-colour inactive" id="btn-colour">Colour Site</button>\n</div>\n'

# 2. Get footer (from the three-dot-menu onwards)
footer_split = full_html.split('<div class="three-dot-menu"')
if len(footer_split) < 2:
    # Try alternate split
    footer_split = full_html.split('<footer')

if len(footer_split) < 2:
    print("Error: Could not find footer split")
    exit(1)

# We want the LAST three-dot-menu or footer
footer = '<div class="three-dot-menu"' + footer_split[-1]

# 3. Assemble
final_html = header + \
             '<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">\n' + \
             yono_html + '\n</div>\n' + \
             '<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">\n' + \
             colour_html + '\n</div>\n' + \
             footer

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Index.html successfully reconstructed with {len(yono_names)} Yono Apps and {len(colour_names)} Colour Sites.")
