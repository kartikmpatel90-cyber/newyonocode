import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the game block once
yaarwin_block = """
        <div class="game-card">
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
                        High Winning Rate
                    </div>
                    <div class="game-meta-row">
                        <svg class="icon-home" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31.076a12 12 0 0 0 16.9 1.6l234.87-193.45a16 16 0 0 1 20.14 0l234.87 193.45a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"></path></svg>
                        Instant Withdrawals
                    </div>
                </div>
                <div class="game-action-desktop hidden-mobile">
                    <a href="https://11yaarwin.com/#/register?invitationCode=35756104798" target="_blank" class="btn-download">Register</a>
                </div>
                <div class="game-info-mobile hidden-desktop">
                    <h4 class="game-title">YaarWin</h4>
                    <div class="mobile-meta-row">
                        <a href="https://11yaarwin.com/#/register?invitationCode=35756104798" target="_blank" class="btn-download-mobile">REGISTER</a>
                        <div class="mobile-bonus-text">High Winning Rate</div>
                    </div>
                </div>
            </div>
        </div>"""

def increment_ranks(content):
    def repl(m):
        rank = int(m.group(1))
        return f'<div class="game-rank">{rank + 1}</div>'
    return re.sub(r'<div class="game-rank">(\d+)</div>', repl, content)

# 1. Update Yono Apps
yono_match = re.search(r'(<div class="games-list" id="yono-apps-list">)(.*?)(</div>\s*<!-- Search Box -->)', html, re.DOTALL)
if yono_match:
    yono_header = yono_match.group(1)
    yono_content = yono_match.group(2)
    yono_footer = yono_match.group(3)
    yono_content = increment_ranks(yono_content)
    new_yono_content = yaarwin_block + yono_content
    html = html.replace(yono_match.group(0), yono_header + new_yono_content + yono_footer)

# 2. Update Colour Sites
colour_match = re.search(r'(<div class="games-list" id="colour-sites-list" style="display: none;">)(.*?)(</div>\s*<!-- Scrolling Marquee -->)', html, re.DOTALL)
if colour_match:
    colour_header = colour_match.group(1)
    colour_content = colour_match.group(2)
    colour_footer = colour_match.group(3)
    colour_content = increment_ranks(colour_content)
    new_colour_content = yaarwin_block + colour_content
    html = html.replace(colour_match.group(0), colour_header + new_colour_content + colour_footer)

# 3. Professionalize the Floating Menu
menu_style_pattern = re.compile(r'<style>\s*\.floating-menu-btn.*?\.overlay-nav a:hover { color: #0088cc; }\s*</style>', re.DOTALL)
new_menu_style = """
    <style>
        .floating-menu-btn {
            position: fixed;
            top: 15px;
            right: 15px;
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #0088cc 0%, #005580 100%);
            color: white;
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,136,204,0.3);
            font-size: 22px;
            z-index: 10001;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .floating-menu-btn:active { transform: scale(0.9); }
        .floating-menu-btn i { transition: transform 0.4s; }
        .floating-menu-btn.active i { transform: rotate(90deg); }

        .menu-overlay {
            position: fixed;
            top: 0; right: -100%; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.98);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: right 0.5s cubic-bezier(0.77, 0, 0.175, 1);
            backdrop-filter: blur(15px);
        }
        .menu-overlay.active { right: 0; }

        .menu-content { 
            width: 100%; 
            max-width: 400px; 
            padding: 40px;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.4s 0.3s;
        }
        .menu-overlay.active .menu-content { opacity: 1; transform: translateY(0); }

        .overlay-nav a {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 20px;
            color: #333;
            text-decoration: none;
            margin: 15px 0;
            padding: 15px 25px;
            font-weight: 600;
            background: #f8f9fa;
            border-radius: 15px;
            transition: all 0.3s;
            border: 1px solid transparent;
        }
        .overlay-nav a i { color: #0088cc; font-size: 1.2em; width: 30px; text-align: center; }
        .overlay-nav a:hover { 
            background: #fff; 
            border-color: #0088cc; 
            color: #0088cc; 
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(0,136,204,0.1);
        }
    </style>
"""
html = menu_style_pattern.sub(new_menu_style, html)

# 4. Update JS for Menu Logic
menu_js_old = re.compile(r"btn\.addEventListener\('click', \(\) => overlay\.style\.display = 'flex'\);\s*closeBtn\.addEventListener\('click', \(\) => overlay\.style\.display = 'none'\);", re.DOTALL)
new_menu_js = """
            btn.addEventListener('click', () => {
                overlay.classList.toggle('active');
                btn.classList.toggle('active');
            });
            closeBtn.addEventListener('click', () => {
                overlay.classList.remove('active');
                btn.classList.remove('active');
            });
"""
html = menu_js_old.sub(new_menu_js, html)

# 5. Update Menu Links with Icons
nav_old = """<nav class="overlay-nav">
                <a href="/">Home</a>
                <a href="https://telegram.me/epcode" target="_blank">About</a>
                <a href="https://telegram.me/epcode" target="_blank">Contact Us</a>
                <a href="https://telegram.me/epcode" target="_blank">Disclaimer</a>
                <a href="https://telegram.me/epcode" target="_blank">Join Telegram</a>
            </nav>"""
nav_new = """<nav class="overlay-nav">
                <a href="/"><i class="fas fa-home"></i> Home</a>
                <a href="https://telegram.me/epcode" target="_blank"><i class="fas fa-info-circle"></i> About Us</a>
                <a href="https://telegram.me/epcode" target="_blank"><i class="fas fa-envelope"></i> Contact Us</a>
                <a href="https://telegram.me/epcode" target="_blank"><i class="fas fa-shield-alt"></i> Disclaimer</a>
                <a href="https://telegram.me/epcode" target="_blank"><i class="fab fa-telegram"></i> Join Telegram</a>
            </nav>"""
html = html.replace(nav_old, nav_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("YaarWin added and Menu professionalized.")
