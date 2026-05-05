import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Completely remove the standard Astra menu structure to start fresh with a floating menu
# We'll remove the <ul> menus and their containers
menu_pattern = re.compile(r'<nav[^>]*id="primary-site-navigation-desktop".*?</nav>', re.DOTALL)
html = menu_pattern.sub('', html)

mobile_menu_pattern = re.compile(r'<div class="ast-mobile-header-content.*?</nav>\s*</div>\s*</div>', re.DOTALL)
html = mobile_menu_pattern.sub('', html)

# Remove the default hamburger button as well
hamburger_pattern = re.compile(r'<div class="ast-builder-layout-element ast-flex site-header-focus-item" data-section="section-header-mobile-trigger">.*?</div>', re.DOTALL)
html = hamburger_pattern.sub('', html)

# 2. Add the Floating 3-Dots Button and Menu Overlay
floating_menu_html = """
    <!-- Floating 3-Dots Menu Button -->
    <button id="floating-menu-btn" class="floating-menu-btn" aria-label="Open Menu">
        <i class="fas fa-ellipsis-v"></i>
    </button>

    <!-- Fullscreen Menu Overlay -->
    <div id="menu-overlay" class="menu-overlay">
        <div class="menu-content">
            <button id="close-menu-btn" class="close-menu-btn">&times;</button>
            <nav class="overlay-nav">
                <a href="/">Home</a>
                <a href="https://telegram.me/epcode" target="_blank">About</a>
                <a href="https://telegram.me/epcode" target="_blank">Contact Us</a>
                <a href="https://telegram.me/epcode" target="_blank">Disclaimer</a>
                <a href="https://telegram.me/epcode" target="_blank">Join Telegram</a>
            </nav>
        </div>
    </div>

    <style>
        .floating-menu-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background: #ffffff;
            color: #333;
            border: none;
            border-radius: 50%;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            font-size: 20px;
            z-index: 10001;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        .floating-menu-btn:hover { transform: scale(1.1); background: #f0f0f0; }

        .menu-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.98);
            z-index: 10002;
            display: none;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(10px);
        }
        .menu-content { text-align: center; position: relative; width: 100%; }
        .close-menu-btn {
            position: absolute; top: -100px; right: 30px;
            font-size: 50px; background: none; border: none; cursor: pointer; color: #333;
        }
        .overlay-nav a {
            display: block; font-size: 24px; color: #333; text-decoration: none;
            margin: 25px 0; font-weight: 600; transition: color 0.3s;
        }
        .overlay-nav a:hover { color: #0088cc; }
    </style>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const btn = document.getElementById('floating-menu-btn');
            const overlay = document.getElementById('menu-overlay');
            const closeBtn = document.getElementById('close-menu-btn');
            
            btn.addEventListener('click', () => overlay.style.display = 'flex');
            closeBtn.addEventListener('click', () => overlay.style.display = 'none');
            overlay.addEventListener('click', (e) => { if(e.target === overlay) overlay.style.display = 'none'; });
        });
    </script>
"""
html = html.replace('</body>', floating_menu_html + '\n</body>')

# 3. Add Search Bar
# We'll place it above the Category Filters
search_bar_html = """
    <!-- Search Box -->
    <div class="search-container">
        <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="game-search" placeholder="Search apps or sites..." aria-label="Search">
        </div>
    </div>

    <style>
        .search-container { padding: 10px 15px; margin-bottom: 5px; }
        .search-box {
            background: #f1f3f4;
            border-radius: 25px;
            padding: 8px 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            border: 1px solid #ddd;
            transition: all 0.3s ease;
        }
        .search-box:focus-within { background: #fff; border-color: #0088cc; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .search-box input {
            border: none; background: transparent; outline: none; width: 100%;
            font-size: 15px; color: #333;
        }
        .search-icon { color: #888; }
    </style>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.getElementById('game-search');
            
            searchInput.addEventListener('input', function(e) {
                const term = e.target.value.toLowerCase();
                const cards = document.querySelectorAll('.game-card');
                
                cards.forEach(card => {
                    const title = card.querySelector('.game-title').textContent.toLowerCase();
                    if (title.includes(term)) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
"""
html = html.replace('<div class="category-filters">', search_bar_html + '\n        <div class="category-filters">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Floating menu and search option implemented.")
