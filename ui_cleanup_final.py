import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove misplaced elements from the footer/middle area
# We'll search for the end of the lists and start of the footer
# Everything between </div>\n</div> (end of lists) and <div class="seo-hidden"> will be replaced.
pattern = r'</div>\s*</div>\s*<footer.*?</style>\s*<div class="floating-social-row">.*?</div>'
# That's too specific. Let's just target the bad parts.

# Remove the duplicated three-dot menu and styles from the footer
content = re.sub(r'<footer.*?</footer>', '', content, flags=re.DOTALL)
content = re.sub(r'<style>\s*\.three-dot-menu.*?</style>', '', content, flags=re.DOTALL)
content = re.sub(r'<div class="three-dot-menu".*?</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<div class="floating-social-row".*?</div>', '', content, flags=re.DOTALL)

# 2. Re-add the CLEAN UI elements correctly before </body>
final_ui = """
<div class="three-dot-menu" id="three-dot-menu">
    <div class="menu-dots" onclick="toggleMenu()">
        <span></span><span></span><span></span>
    </div>
    <div class="menu-content" id="menu-content">
        <a href="/"><i class="fas fa-home"></i> Home</a>
        <a href="https://telegram.me/epcode" target="_blank"><i class="fab fa-telegram"></i> Telegram</a>
        <a href="https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        <a href="https://www.youtube.com/@Epsupport1" target="_blank"><i class="fab fa-youtube"></i> YouTube</a>
        <a href="#"><i class="fas fa-info-circle"></i> About</a>
    </div>
</div>

<div class="floating-social-row">
    <a href="https://telegram.me/epcode" target="_blank" class="social-btn tg"><i class="fab fa-telegram-plane"></i></a>
    <a href="https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M" target="_blank" class="social-btn wa"><i class="fab fa-whatsapp"></i></a>
    <a href="https://www.youtube.com/@Epsupport1" target="_blank" class="social-btn yt"><i class="fab fa-youtube"></i></a>
</div>

<footer class="site-footer">
    <div class="footer-content">
        <p class="footer-warning">🔞 18+ Responsible Gaming</p>
        <p class="footer-disclaimer">
            Disclaimer: This site is for information purposes only. We do not promote illegal activities. 
            Playing games involves financial risk. Please play responsibly.
        </p>
        <div class="footer-copy">© 2026 NewYono Code. All Rights Reserved.</div>
    </div>
</footer>

<style>
    .three-dot-menu { position: fixed; top: 20px; right: 20px; z-index: 10001; }
    .menu-dots { width: 45px; height: 45px; background: #fff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border: 1px solid #eee; }
    .menu-dots span { width: 6px; height: 6px; background: #333; border-radius: 50%; }
    .menu-content { position: absolute; top: 55px; right: 0; background: #fff; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); display: none; width: 200px; overflow: hidden; border: 1px solid #eee; }
    .menu-content.active { display: block; }
    .menu-content a { display: flex; align-items: center; gap: 15px; padding: 15px 25px; text-decoration: none; color: #333; font-size: 15px; border-bottom: 1px solid #f5f5f5; transition: 0.2s; }
    .menu-content a:hover { background: #f8f9fa; color: #d80000; }
    
    .floating-social-row { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 10000; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); padding: 12px 25px; border-radius: 50px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.5); }
    .social-btn { width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #fff; text-decoration: none; transition: 0.3s; }
    .social-btn.tg { background: #0088cc; }
    .social-btn.wa { background: #25d366; }
    .social-btn.yt { background: #ff0000; }
    .social-btn:hover { transform: scale(1.1) translateY(-5px); }

    .site-footer { background: #111; color: #aaa; padding: 50px 20px 100px; text-align: center; border-top: 1px solid #222; }
    .footer-warning { color: #d80000; font-weight: bold; font-size: 18px; margin-bottom: 15px; }
    .footer-disclaimer { font-size: 12px; line-height: 1.6; max-width: 600px; margin: 0 auto 20px; }
    .footer-copy { font-size: 13px; color: #555; }
</style>
"""

# Insert before </body> and after the seo-hidden div
content = content.replace('</body>', f'{final_ui}\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Site UI cleaned and professionalized.")
