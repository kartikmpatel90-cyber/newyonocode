import json
import os
import re

# 1. Update links_recovery.json with missing data for YaarWin and Jaiho 91
with open('links_recovery.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Ensure Jaiho 91 and YaarWin are in the DB with correct data
if "Jaiho 91" not in db:
    db["Jaiho 91"] = {
        "internal_link": "/jaiho91/",
        "download_link": "https://jaiho91.cc/?code=C42XS38APLA&t=1778035618",
        "image": "logo_jaiho91.png"
    }

if "YaarWin" not in db:
    db["YaarWin"] = {
        "internal_link": "/yaarwin/",
        "download_link": "https://11yaarwin.com/#/register?invitationCode=35756104798",
        "image": "logo_yaarwin.jpg"
    }

with open('links_recovery.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2)

print("links_recovery.json updated with Jaiho 91 and YaarWin.")

# 2. Fix Categorization and Duplication in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Separate the games into clean lists
# We'll use the DB to rebuild them from scratch to ensure NO duplication
yono_apps = ["Jaiho 91", "Yono Rummy", "Ind Rummy", "Rummy Ludo", "Spin101", "GO GO RUMMY", "Yn777", "Ind Slots", 
             "Bingo101", "Boss Rummy", "Yono Games", "Joy Rummy", "567 Slots", "Ever777", "Yono-777", "Hindi 777", 
             "Rummy888", "Good Slots", "Game Rummy", "Ok Rummy", "Yes Spin", "Love Rummy", "Share Slots", "MQM Bet", 
             "Hi Rummy", "MBM BET", "Top Rummy", "Jaiho Slots", "Saga Slots", "Yono Arcade", "Spin777", "ABC Rummy", 
             "Jai Ho Rummy", "Jaiho 777", "Rummy 91", "Jai Ho Spin", "Jai Ho Arcade", "Neta Vip", "Slots Winner", 
             "Slots Spin", "789 Jackpots", "101Z", "Spin Winner", "Spin Gold", "Yono Slots", "Spin Crush", 
             "Rumble Rummy", "Yono VIP", "Club INR", "Maha Games", "Ind Club", "Jaiho Win"]

colour_sites = ["YaarWin", "IN- 999", "Jai club", "91CLUB", "55CLUB", "51 game", "Bounty Game", "TIRANGA", 
                "BDG WIN", "Tashan Game", "6 Club", "82 Lottery", "Sikkim", "Goa Game", "RAJA LUCK", "OKWIN"]

# Template for the game card
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
        if not data: continue
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

yono_html = build_list(yono_apps, db)
colour_html = build_list(colour_sites, db)

# Replace the lists in content
content = re.sub(r'<div class="games-list" id="yono-apps-list".*?</div>\s*</div>\s*</div>\s*</div>', 
                 f'<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">\n{yono_html}\n</div>', 
                 content, flags=re.DOTALL)

content = re.sub(r'<div class="games-list" id="colour-sites-list".*?</div>\s*</div>\s*</div>\s*</div>', 
                 f'<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">\n{colour_html}\n</div>', 
                 content, flags=re.DOTALL)

# 3. Move Banner from Footer to Header
banner_m = re.search(r'<a href="https://telegram.me/epcode".*?<img src="ep_code_banner.png".*?</a>', content, re.DOTALL)
if banner_m:
    banner_code = banner_m.group(0)
    content = content.replace(banner_code, '')
    # Insert in header
    content = content.replace('<!-- Rollable / Promotional Banner -->', 
                              f'<div class="promo-banner-top" style="text-align:center; margin:10px 0;">{banner_code}</div>\n<!-- Rollable / Promotional Banner -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html fully cleaned and fixed.")
