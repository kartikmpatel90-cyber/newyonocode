import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Generator for Personal Pages (Add Home Button)
def update_generator():
    gen_file = 'generate_pages_v4.py'
    if os.path.exists(gen_file):
        with open(gen_file, 'r', encoding='utf-8') as f:
            gen_content = f.read()
        
        # Add a more prominent home button in the template
        new_home_btn = """
        <a href="../index.html" class="btn btn-tg" style="background: #333; color: #fff;">
            <i class="fas fa-home"></i> BACK TO ALL APPS
        </a>
        """
        # Insert before the Join Telegram button
        gen_content = gen_content.replace('<a href="https://telegram.me/epcode" target="_blank" class="btn btn-tg">', 
                                         new_home_btn + '<a href="https://telegram.me/epcode" target="_blank" class="btn btn-tg">')
        
        with open('generate_pages_v5.py', 'w', encoding='utf-8') as f:
            f.write(gen_content)

update_generator()

# 2. Fix index.html
def fix_index(html):
    # Split into sections to keep Yono and Colour separate
    yono_start = html.find('id="yono-apps-list"')
    colour_start = html.find('id="colour-sites-list"')
    
    parts = []
    if yono_start != -1 and colour_start != -1:
        parts.append(html[:yono_start])
        parts.append(html[yono_start:colour_start])
        parts.append(html[colour_start:])
    else:
        return html # Something is wrong

    def slugify(text):
        return re.sub(r'[^a-z0-9]', '', text.lower().strip())

    def process_section(section_text):
        # Find all game cards
        cards = re.split(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', section_text, flags=re.DOTALL)
        
        new_cards = []
        rank_counter = 1
        for card in cards:
            if '<div class="game-card"' in card:
                title_match = re.search(r'class="game-title">(.*?)</h4>', card)
                if not title_match:
                    title_match = re.search(r'alt="(.*?)"', card)
                
                if title_match:
                    title = title_match.group(1).strip()
                    slug = slugify(title)
                    
                    # Update Rank
                    card = re.sub(r'class="game-rank">(\d+)</div>', f'class="game-rank">{rank_counter}</div>', card)
                    rank_counter += 1
                    
                    # Add withdrawal info to Jaiho 91 and YaarWin if missing
                    if title in ["Jaiho 91", "YaarWin"]:
                        # Add a "Hot" effect (glowing border)
                        card = card.replace('class="game-card"', 'class="game-card hot-card"')
                        
                        # Check if withdrawal info is missing
                        if "Min. Withdraw" not in card:
                            withdraw_info = """
                            <div class="game-meta-row">
                                <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                                Min. Withdraw ₹100
                            </div>"""
                            # Insert before game-action-desktop
                            card = card.replace('<div class="game-action-desktop', withdraw_info + '<div class="game-action-desktop')
                            
                            mobile_withdraw = """
                            <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                                <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                                Min. Withdraw ₹100
                            </div>"""
                            # Insert before the closing mobile div
                            card = card.replace('</div>\s*</div>\s*</div>', mobile_withdraw + '</div></div></div>', 1)

                    # 3. Make Image and Title clickable to the personal page
                    # Wrap title
                    card = card.replace(f'class="game-title">{title}</h4>', 
                                      f'class="game-title"><a href="/{slug}/" style="text-decoration:none; color:inherit;">{title}</a></h4>')
                    
                    # Wrap image (replace the existing link which might go to external site)
                    # We only want the image to go to the internal page
                    card = re.sub(r'<div class="game-image">.*?<a href=".*?".*?>(.*?)</a>.*?</div>', 
                                 f'<div class="game-image"><a href="/{slug}/">\\1</a></div>', card, flags=re.DOTALL)

            new_cards.append(card)
        
        return "".join(new_cards)

    parts[1] = process_section(parts[1])
    parts[2] = process_section(parts[2])
    
    # Add CSS for Hot cards
    css_patch = """
    <style>
    .hot-card { border: 2px solid #ff4757 !important; animation: glow 2s infinite alternate; }
    @keyframes glow { from { box-shadow: 0 0 5px #ff4757; } to { box-shadow: 0 0 20px #ff4757; } }
    </style>
    """
    if "</head>" in parts[0]:
        parts[0] = parts[0].replace("</head>", css_patch + "</head>")
        
    return "".join(parts)

fixed_content = fix_index(content)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Index fix complete.")
