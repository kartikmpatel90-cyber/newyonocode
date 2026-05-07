import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Navbar and EP Code Logo
# The user wants EP Code logo ONLY at the top
content = re.sub(r'<div class="site-branding ast-site-identity".*?</div>\s*<!-- \.site-branding -->', 
                 r'''<div class="site-branding ast-site-identity">
                    <span class="site-logo-img">
                        <a href="/" class="custom-logo-link" rel="home"><img src="ep_code_logo.png" alt="EP Code" width="48" height="48"></a>
                    </span>
                    <div class="ast-site-title-wrap">
                        <span class="site-title"><a href="/">NewYono Code</a></span>
                    </div>
                </div>''', content, flags=re.DOTALL)

# 2. Add professional Three-Dot Floating Menu
# The user wants it small, floating, not taking all space.
menu_html = """
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

<script>
    function toggleMenu() {
        const content = document.getElementById('menu-content');
        content.classList.toggle('active');
    }
    // Close menu when clicking outside
    window.onclick = function(event) {
        if (!event.target.matches('.menu-dots') && !event.target.matches('.menu-dots span')) {
            const content = document.getElementById('menu-content');
            if (content.classList.contains('active')) {
                content.classList.remove('active');
            }
        }
    }
</script>

<style>
    .three-dot-menu { position: fixed; top: 15px; right: 15px; z-index: 10001; }
    .menu-dots { width: 40px; height: 40px; background: #fff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; cursor: pointer; box-shadow: 0 2px 10px rgba(0,0,0,0.2); border: 1px solid #eee; }
    .menu-dots span { width: 5px; height: 5px; background: #333; border-radius: 50%; }
    .menu-content { position: absolute; top: 50px; right: 0; background: #fff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); display: none; width: 180px; overflow: hidden; border: 1px solid #eee; }
    .menu-content.active { display: block; animation: slideIn 0.3s ease; }
    .menu-content a { display: flex; align-items: center; gap: 12px; padding: 12px 20px; text-decoration: none; color: #333; font-size: 14px; font-weight: 500; transition: 0.2s; }
    .menu-content a:hover { background: #f8f9fa; color: #d80000; }
    .menu-content a i { width: 20px; font-size: 16px; color: #666; }
    @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>
"""
if 'class="three-dot-menu"' not in content:
    content = content.replace('</body>', f'{menu_html}\n</body>')

# 3. Floating Buttons in a ROW (Telegram, WhatsApp, YouTube)
# Positioned at the bottom center or fixed row
floating_row_html = """
<div class="floating-social-row">
    <a href="https://telegram.me/epcode" target="_blank" class="social-btn tg"><i class="fab fa-telegram-plane"></i></a>
    <a href="https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M" target="_blank" class="social-btn wa"><i class="fab fa-whatsapp"></i></a>
    <a href="https://www.youtube.com/@Epsupport1" target="_blank" class="social-btn yt"><i class="fab fa-youtube"></i></a>
</div>

<style>
    .floating-social-row { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px; z-index: 9999; background: rgba(255,255,255,0.95); padding: 10px 20px; border-radius: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); border: 1px solid #eee; }
    .social-btn { width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #fff; text-decoration: none; transition: 0.3s; }
    .social-btn.tg { background: #0088cc; }
    .social-btn.wa { background: #25d366; }
    .social-btn.yt { background: #ff0000; }
    .social-btn:hover { transform: scale(1.1) translateY(-5px); }
</style>
"""
# Remove old floating buttons first
content = re.sub(r'<a href="https://telegram.me/epcode".*?class="float-tg">.*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="https://whatsapp.com/channel/.*?class="float-wa">.*?</a>', '', content, flags=re.DOTALL)

if 'class="floating-social-row"' not in content:
    content = content.replace('</body>', f'{floating_row_html}\n</body>')

# 4. Fix Search and Category Switching Logic
# Ensure showCategory and filterGames are in global scope
# We'll replace the existing script with a robust one
new_js = """
<script>
    function showCategory(cat) {
        const yonoList = document.getElementById('yono-apps-list');
        const colourList = document.getElementById('colour-sites-list');
        const yonoBtn = document.getElementById('btn-yono');
        const colourBtn = document.getElementById('btn-colour');
        
        if (cat === 'yono') {
            yonoList.style.display = 'flex';
            colourList.style.display = 'none';
            yonoBtn.classList.remove('inactive');
            colourBtn.classList.add('inactive');
        } else {
            yonoList.style.display = 'none';
            colourList.style.display = 'flex';
            yonoBtn.classList.add('inactive');
            colourBtn.classList.remove('inactive');
        }
        filterGames();
    }

    function filterGames() {
        const term = document.getElementById('game-search').value.toLowerCase();
        const cards = document.querySelectorAll('.game-card');
        cards.forEach(card => {
            const title = card.querySelector('.game-title').textContent.toLowerCase();
            if (title.includes(term)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('game-search');
        if (searchInput) {
            searchInput.addEventListener('input', filterGames);
        }
    });
</script>
"""
# Replace the first script block in main content
content = re.sub(r'<script>.*?</script>', new_js, content, flags=re.DOTALL, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("UI Rebuild (Top Logo, Menu, Social Row, Search Fix) completed.")
