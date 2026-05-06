import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def super_fix(html):
    # 1. Split into 3 parts: Header, Yono List, Colour List, Footer
    yono_id = 'id="yono-apps-list"'
    colour_id = 'id="colour-sites-list"'
    section_title = '<div class="section-title"'
    
    y_start = html.find(yono_id)
    c_start = html.find(colour_id)
    
    if y_start == -1 or c_start == -1: return html
    
    # Locate ends
    # Yono list ends where Colour List header starts (roughly)
    y_end = html.find('<div class="section-title"', y_start)
    if y_end == -1: y_end = c_start
    
    # Colour list ends where next section or footer starts
    c_end = html.find('<div class="footer-marquee"', c_start)
    if c_end == -1: c_end = len(html)
    
    header = html[:y_start]
    yono_text = html[y_start:y_end]
    mid = html[y_end:c_start]
    colour_text = html[c_start:c_end]
    footer = html[c_end:]

    def extract_cards(text):
        # Find all game-card blocks
        return re.findall(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', text, flags=re.DOTALL)

    y_cards = extract_cards(yono_text)
    c_cards = extract_cards(colour_text)
    
    # 2. Separate and Clean
    y_final = []
    c_final = []
    seen_y = set()
    seen_c = set()
    
    def get_title(card):
        m = re.search(r'class="game-title">.*?>(.*?)</a>', card)
        if not m: m = re.search(r'class="game-title">(.*?)</h4>', card)
        return m.group(1).strip() if m else ""

    # Process Yono Cards
    for card in y_cards:
        title = get_title(card)
        if not title: continue
        t_low = title.lower().replace(" ", "")
        if t_low in seen_y: continue
        seen_y.add(t_low)
        y_final.append(card)
        
    # Process Colour Cards
    for card in c_cards:
        title = get_title(card)
        if not title: continue
        t_low = title.lower().replace(" ", "")
        
        # If it's a Yono app, move it to seen_y if not already there
        if "yono" in t_low and t_low not in seen_y:
            y_final.append(card)
            seen_y.add(t_low)
            continue
        
        if t_low in seen_c: continue
        seen_c.add(t_low)
        c_final.append(card)

    # 3. Ensure Jaiho 91 and YaarWin are at the top of BOTH
    # We'll create perfect templates for them
    def create_card(title, link, icon, rank, is_hot=False):
        slug = re.sub(r'[^a-z0-9]', '', title.lower())
        hot_class = ' hot-card' if is_hot else ''
        return f"""
        <div class="game-card{hot_class}">
            <div class="game-rank">{rank}</div>
            <div class="game-image"><a href="/{slug}/"><img src="{icon}" alt="{title}" loading="lazy" width="100" height="100" style="border-radius:15px;"></a></div>
            <div class="game-details">
                <div class="game-info-desktop hidden-mobile">
                    <h4 class="game-title"><a href="/{slug}/" style="text-decoration:none; color:inherit;">{title}</a></h4>
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
                    <a href="{link}" target="_blank" class="btn-download">Register</a>
                </div>
                <div class="game-info-mobile hidden-desktop">
                    <h4 class="game-title"><a href="/{slug}/" style="text-decoration:none; color:inherit;">{title}</a></h4>
                    <div class="mobile-meta-row">
                        <a href="{link}" target="_blank" class="btn-download-mobile">REGISTER</a>
                        <div class="mobile-bonus-text">Bonus ₹245</div>
                    </div>
                    <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                        <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                        Min. Withdraw ₹100
                    </div>
                </div>
            </div>
        </div>"""

    jaiho_link = "https://jaiho91.cc/?code=C42XS38APLA&t=1778035618"
    yaarwin_link = "https://11yaarwin.com/#/register?invitationCode=35756104798"
    
    # Rebuild Lists
    def clean_and_reorder(cards_list, is_yono):
        final = []
        seen = set()
        
        # Force Jaiho and YaarWin at top
        final.append(create_card("Jaiho 91", jaiho_link, "logo_jaiho91.png", 1, is_hot=(is_yono)))
        final.append(create_card("YaarWin", yaarwin_link, "logo_yaarwin.jpg", 2, is_hot=False))
        seen.add("jaiho91")
        seen.add("yaarwin")
        
        rank = 3
        for c in cards_list:
            t = get_title(c)
            t_low = t.lower().replace(" ", "")
            if t_low in seen: continue
            seen.add(t_low)
            
            # Update rank in existing card
            c = re.sub(r'class="game-rank">\d+</div>', f'class="game-rank">{rank}</div>', c)
            # Ensure it doesn't have hot-card
            c = c.replace('hot-card', '')
            
            final.append(c)
            rank += 1
        return "".join(final)

    new_yono_content = 'id="yono-apps-list">\n' + clean_and_reorder(y_final, True)
    new_colour_content = 'id="colour-sites-list" style="display: none;">\n' + clean_and_reorder(c_final, False)

    return header + new_yono_content + mid + new_colour_content + footer

content = super_fix(content)

# Final CSS check
css_patch = """
    <style>
    .hot-card { border: 2px solid #ff4757 !important; animation: glow 2s infinite alternate; background: #fff5f6 !important; }
    @keyframes glow { from { box-shadow: 0 0 5px #ff4757; } to { box-shadow: 0 0 20px #ff4757; } }
    .games-list { min-height: 100vh; padding-bottom: 50px; }
    </style>
"""
if "</head>" in content:
    content = re.sub(r'<style>\s*\.hot-card.*?</style>', '', content, flags=re.DOTALL)
    content = content.replace("</head>", css_patch + "</head>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Super Fix complete.")
