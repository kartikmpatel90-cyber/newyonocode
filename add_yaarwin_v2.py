import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the YaarWin card for Yono List (with Bonus info)
yaarwin_yono_card = """
        <div class="game-card" style="position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; background: #ff4757; color: white; padding: 2px 10px; font-size: 10px; font-weight: bold; border-bottom-left-radius: 8px; z-index: 10;">NEW</div>
            <div class="game-rank">1</div>
            <div class="game-image">
                <a href="https://11yaarwin.com/#/register?invitationCode=35756104798" target="_blank">
                    <img src="logo_yaarwin.jpg" alt="YaarWin" loading="lazy" decoding="async" width="100" height="100" style="border-radius:15px;">
                </a>
            </div>
            <div class="game-details">
                <div class="game-info-desktop hidden-mobile">
                    <h4 class="game-title">YaarWin</h4>
                    <div class="game-meta-row">
                        <svg class="icon-gift" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M32 448c0 17.7 14.3 32 32 32h160V320H32v128zm256 32h160c17.7 0 32-14.3 32-32V320H288v160zm192-320h-42.1c6.2-12.1 10.1-25.5 10.1-40 0-48.5-39.5-88-88-88-41.6 0-68.5 21.3-103 68.3-34.5-47-61.4-68.3-103-68.3-48.5 0-88 39.5-88 88 0 14.5 3.8 27.9 10.1 40H32c-17.7 0-32 14.3-32 32v80c0 8.8 7.2 16 16 16h480c8.8 0 16-7.2 16-16v-80c0-17.7-14.3-32-32-32z"></path></svg>
                        Sign Up Bonus ₹245
                    </div>
                    <div class="game-meta-row">
                        <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                        Min. Withdraw ₹100
                    </div>
                </div>
                <div class="game-action-desktop hidden-mobile">
                    <a href="https://11yaarwin.com/#/register?invitationCode=35756104798" target="_blank" class="btn-download">Register</a>
                </div>
                <div class="game-info-mobile hidden-desktop">
                    <h4 class="game-title">YaarWin</h4>
                    <div class="mobile-meta-row">
                        <a href="https://11yaarwin.com/#/register?invitationCode=35756104798" target="_blank" class="btn-download-mobile">REGISTER</a>
                        <div class="mobile-bonus-text">Bonus ₹245</div>
                    </div>
                </div>
            </div>
        </div>"""

# Define the YaarWin card for Colour List (with Win Rate info)
yaarwin_colour_card = yaarwin_yono_card.replace("Sign Up Bonus ₹245", "High Winning Rate").replace("Min. Withdraw ₹100", "Instant Withdrawals").replace("Bonus ₹245", "High Winning")

def increment_ranks(content):
    def repl(m):
        rank = int(m.group(1))
        return f'<div class="game-rank">{rank + 1}</div>'
    return re.sub(r'<div class="game-rank">(\d+)</div>', repl, content)

# 1. Insert into Yono List
yono_start = html.find('id="yono-apps-list">')
if yono_start != -1:
    yono_end = html.find('</div>', yono_start + 20) # Find the first closing tag after rank 1 or search box?
    # Better: find the first <div class="game-card"> inside the list
    card_start = html.find('<div class="game-card"', yono_start)
    # Increment all ranks in the yono list
    # The yono list ends at '</div>\s*<main>' or similar. 
    # Actually, it ends where 'id="colour-sites-list"' begins.
    colour_list_start = html.find('id="colour-sites-list"')
    yono_list_content = html[card_start:colour_list_start]
    new_yono_list_content = increment_ranks(yono_list_content)
    
    html = html[:card_start] + yaarwin_yono_card + new_yono_list_content + html[colour_list_start:]

# 2. Insert into Colour List
# Re-find colour list start because html changed
colour_list_start = html.find('id="colour-sites-list"')
if colour_list_start != -1:
    card_start = html.find('<div class="game-card"', colour_list_start)
    # The colour list ends at '</div>\s*<!-- Scrolling Marquee -->'
    marquee_start = html.find('<!-- Scrolling Marquee -->')
    colour_list_content = html[card_start:marquee_start]
    new_colour_list_content = increment_ranks(colour_list_content)
    
    html = html[:card_start] + yaarwin_colour_card + new_colour_list_content + html[marquee_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("YaarWin successfully added to both lists with 'NEW' badge.")
