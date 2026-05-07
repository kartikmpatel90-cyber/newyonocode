import json
import re

# Source of Truth
with open('audit_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_card_html(game, rank):
    is_hot = ' hot-card' if rank == 1 else ''
    # Determine which icon set to use (we'll use the one from index.html)
    # For now, we'll use a standard template based on the user's design
    return f'''
<div class="game-card{is_hot}">
    <div class="game-rank">{rank}</div>
    <div class="game-image"><a href="{game['link']}"><img src="{game['image']}" alt="{game['title']}" onerror="this.src='ep_code_logo.png'" loading="lazy" width="100" height="100" style="border-radius:15px;"></a></div>
    <div class="game-details">
        <div class="game-info-desktop hidden-mobile">
            <h4 class="game-title"><a href="{game['link']}" style="text-decoration:none; color:inherit;">{game['title']}</a></h4>
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
            <a href="{game['download_link']}" target="_blank" class="btn-download">Register</a>
        </div>
        <div class="game-info-mobile hidden-desktop">
            <h4 class="game-title"><a href="{game['link']}" style="text-decoration:none; color:inherit;">{game['title']}</a></h4>
            <div class="mobile-meta-row">
                <a href="{game['download_link']}" target="_blank" class="btn-download-mobile">REGISTER</a>
                <div class="mobile-bonus-text">Bonus ₹245</div>
            </div>
            <div class="mobile-withdraw-text" style="display:flex; align-items:center; gap:5px; margin-top:3px;">
                <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="#009C18" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                Min. Withdraw ₹100
            </div>
        </div>
    </div>
</div>'''

yono_html = '\n'.join([get_card_html(g, i+1) for i, g in enumerate(data['yono'])])
colour_html = '\n'.join([get_card_html(g, i+1) for i, g in enumerate(data['colour'])])

full_lists_html = f'''
<div class="games-list" id="yono-apps-list" style="display: flex; flex-direction: column;">
{yono_html}
</div>
<div class="games-list" id="colour-sites-list" style="display: none; flex-direction: column;">
{colour_html}
</div>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old list section
# We'll look for the start of yono-apps-list and end after colour-sites-list
pattern = r'<div class="games-list" id="yono-apps-list".*?</div>\s*</div>'
content = re.sub(pattern, full_lists_html, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html lists rebuilt from source of truth.")
