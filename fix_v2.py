import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def fix_content(html):
    # 1. Remove all existing hot-card classes and glows
    html = html.replace('hot-card', '')
    
    # 2. Add hot-card ONLY to the Rank 1 of Yono Apps
    yono_start = html.find('id="yono-apps-list"')
    if yono_start != -1:
        # Find the first game-card in this section
        first_card_start = html.find('class="game-card"', yono_start)
        if first_card_start != -1:
            html = html[:first_card_start] + 'class="game-card hot-card"' + html[first_card_start + len('class="game-card"'):]

    # 3. Add Withdrawal Info to Rank 1 and 2 of BOTH lists if missing
    def add_meta(section_id):
        nonlocal html
        start = html.find(f'id="{section_id}"')
        if start == -1: return
        
        # Split by game cards
        cards = re.split(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', html[start:], flags=re.DOTALL)
        
        for i in range(min(5, len(cards))): # Check first few cards
            card = cards[i]
            if '<div class="game-card"' in card:
                # Add Desktop Withdraw Row if missing
                if "Min. Withdraw" not in card and "Fast Withdrawals" not in card:
                    withdraw_row = """
                    <div class="game-meta-row">
                        <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                        Min. Withdraw ₹100
                    </div>"""
                    card = card.replace('<div class="game-action-desktop', withdraw_row + '<div class="game-action-desktop')
                    
                    mobile_withdraw = """
                    <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                        <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                        Min. Withdraw ₹100
                    </div>"""
                    card = card.replace('</div>\n                </div>\n            </div>', mobile_withdraw + '</div></div></div>')
                cards[i] = card
        
        # Join section back
        section_end = html.find('<div class="section-title"', start + 1)
        if section_end == -1: section_end = len(html)
        
        html = html[:start] + "".join(cards) + html[section_end:]

    add_meta("yono-apps-list")
    add_meta("colour-sites-list")
    
    return html

new_html = fix_content(content)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Fix v2 complete.")
