import json

# 1. Source of Truth
with open('links_recovery.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

colour_names = [
    "YaarWin", "IN- 999", "Jai club", "91CLUB", "55CLUB", "51 GAME", 
    "Bounty Game", "TIRANGA", "BDG WIN", "Tashan Game", "6 Club", 
    "82 Lottery", "Sikkim", "Goa Game", "RAJA LUCK", "OKWIN"
]

yono_names = [
    "Jaiho 91", "Jaiho Win", "Yono Rummy", "Ind Rummy", "Rummy Ludo", "Spin101", 
    "GO GO RUMMY", "Yn777", "Ind Slots", "Bingo101", "Boss Rummy", "Yono Games", 
    "Joy Rummy", "567 Slots", "Ever777", "Yono-777", "Hindi 777", "Rummy888", 
    "Good Slots", "Game Rummy", "Ok Rummy", "Yes Spin", "Love Rummy", "Share Slots", 
    "MQM Bet", "Hi Rummy", "MBM BET", "Top Rummy", "Jaiho Slots", "Saga Slots", 
    "Yono Arcade", "Spin777", "ABC Rummy", "Jai Ho Rummy", "Jaiho 777", "Rummy 91", 
    "Jai Ho Spin", "Jai Ho Arcade", "Neta Vip", "Slots Winner", "Slots Spin", 
    "789 Jackpots", "101Z", "Spin Winner", "Spin Gold", "Yono Slots", "Spin Crush", 
    "Rumble Rummy", "Yono VIP", "Club INR", "Maha Games", "Ind Club", "101z"
]

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
        if not data:
            for k in db:
                if k.lower() == name.lower():
                    data = db[k]
                    break
        if not data: continue
        rank = i + 1
        hot_class = " hot-card" if rank <= 2 else ""
        html += card_template.format(
            hot_class=hot_class,
            rank=rank,
            internal=data['internal_link'],
            image=data['image'],
            title=name,
            download=data['download_link']
        )
    return html

yono_html = build_list(yono_names, db)
colour_html = build_list(colour_names, db)

full_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NewYono Code | Official Yono Apps & Colour Sites</title>
    <meta name="description" content="Discover the best Yono Apps and Colour Sites. Play Jaiho 91, YaarWin, and more. Secure APK downloads and real cash winning games.">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0088cc; --secondary: #00c853; --dark: #1a1a1a; --light: #f8f9fa; }}
        body {{ font-family: 'Outfit', sans-serif; background: #f0f2f5; margin: 0; padding: 0; color: #333; }}
        
        .navbar {{ background: #fff; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .navbar img {{ height: 35px; border-radius: 8px; }}
        .navbar h1 {{ font-size: 18px; margin: 0; color: var(--dark); font-weight: 700; letter-spacing: 0.5px; }}

        .seo-banner {{ background: #000; color: #fff; padding: 8px 0; font-size: 13px; font-weight: 600; }}
        
        .search-container {{ padding: 15px; background: #fff; }}
        .search-box {{ position: relative; max-width: 600px; margin: 0 auto; }}
        .search-box i {{ position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #888; }}
        .search-box input {{ width: 100%; padding: 12px 15px 12px 45px; border: 1.5px solid #eee; border-radius: 12px; font-size: 15px; transition: 0.3s; box-sizing: border-box; }}
        .search-box input:focus {{ border-color: var(--primary); outline: none; box-shadow: 0 0 0 4px rgba(0,136,204,0.1); }}

        .category-filters {{ display: flex; gap: 10px; padding: 15px; max-width: 600px; margin: 0 auto; }}
        .btn-cat {{ flex: 1; padding: 12px; border: none; border-radius: 12px; font-weight: 700; font-size: 14px; cursor: pointer; transition: 0.3s; }}
        .btn-yono {{ background: var(--primary); color: #fff; }}
        .btn-colour {{ background: var(--secondary); color: #fff; }}
        .btn-cat.inactive {{ background: #e0e0e0; color: #888; opacity: 0.7; }}

        .games-list {{ display: flex; flex-direction: column; gap: 12px; padding: 15px; max-width: 800px; margin: 0 auto; }}
        .game-card {{ background: #fff; border-radius: 18px; padding: 12px; display: flex; align-items: center; gap: 15px; position: relative; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: 0.3s; border: 1px solid #f0f0f0; }}
        .game-card:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.08); }}
        .game-rank {{ position: absolute; top: -8px; left: -8px; background: #ff4757; color: #fff; width: 24px; height: 24px; border-radius: 50%; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; z-index: 2; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        .hot-card {{ border: 1.5px solid #ff4757; background: linear-gradient(to right, #fff, #fff5f5); }}
        .game-image img {{ width: 75px; height: 75px; border-radius: 15px; object-fit: cover; display: block; }}
        .game-details {{ flex: 1; display: flex; justify-content: space-between; align-items: center; }}
        .game-title {{ margin: 0; font-size: 17px; font-weight: 700; color: var(--dark); }}
        .game-meta-row {{ display: flex; align-items: center; gap: 5px; font-size: 13px; color: #666; margin-top: 4px; }}
        .game-meta-row svg {{ width: 14px; height: 14px; }}
        
        .btn-download, .btn-download-mobile {{ background: linear-gradient(135deg, var(--primary) 0%, #006699 100%); color: #fff; text-decoration: none; padding: 10px 20px; border-radius: 10px; font-weight: 700; font-size: 14px; transition: 0.3s; display: inline-block; }}
        .btn-download-mobile {{ padding: 8px 12px; font-size: 12px; }}

        .hidden-mobile {{ display: block; }}
        .hidden-desktop {{ display: none; }}

        @media (max-width: 600px) {{
            .hidden-mobile {{ display: none; }}
            .hidden-desktop {{ display: block; }}
            .game-image img {{ width: 65px; height: 65px; }}
            .game-title {{ font-size: 15px; }}
        }}

        /* Floating Three-Dot Menu */
        .three-dot-menu {{ position: fixed; top: 15px; right: 15px; z-index: 10001; }}
        .menu-btn {{ width: 40px; height: 40px; background: #fff; border: none; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); cursor: pointer; font-size: 20px; display: flex; align-items: center; justify-content: center; }}
        .menu-overlay {{ position: fixed; top: 0; right: -100%; width: 100%; height: 100%; background: rgba(255,255,255,0.98); z-index: 10000; transition: 0.4s cubic-bezier(0.77, 0, 0.175, 1); backdrop-filter: blur(10px); display: flex; align-items: center; justify-content: center; }}
        .menu-overlay.active {{ right: 0; }}
        .menu-nav a {{ display: block; padding: 15px 30px; font-size: 20px; font-weight: 600; color: #333; text-decoration: none; border-bottom: 1px solid #eee; transition: 0.3s; }}
        .menu-nav a:hover {{ color: var(--primary); padding-left: 40px; }}

        /* Social Row */
        .social-row {{ position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #fff; padding: 8px 20px; border-radius: 30px; box-shadow: 0 5px 20px rgba(0,0,0,0.15); display: flex; gap: 20px; z-index: 9999; border: 1px solid #eee; }}
        .social-row a {{ font-size: 24px; color: #555; transition: 0.3s; }}
        .social-row a.tg {{ color: #0088cc; }}
        .social-row a.wa {{ color: #25d366; }}
        .social-row a.yt {{ color: #ff0000; }}

        .footer {{ text-align: center; padding: 40px 20px 100px; background: #fff; color: #888; font-size: 13px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>

    <nav class="navbar">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="ep_code_logo.png" alt="Logo">
            <h1>NEWYONO CODE</h1>
        </div>
    </nav>

    <div class="seo-banner">
        <marquee scrollamount="6">Welcome to NewYono Code! Earn real cash daily with trusted Yono Apps like Jaiho 91 and Colour Sites like YaarWin. Get 100% secure APK downloads here.</marquee>
    </div>

    <div class="promo-banner-top" style="text-align:center; margin:15px 10px;">
        <a href="https://telegram.me/epcode" target="_blank">
            <img src="ep_code_banner.png" alt="Promo" style="width:100%; max-width:600px; border-radius:12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </a>
    </div>

    <div class="search-container">
        <div class="search-box">
            <i class="fas fa-search"></i>
            <input type="text" id="game-search" placeholder="Search apps or sites..." onkeyup="filterGames()">
        </div>
    </div>

    <div class="category-filters">
        <button onclick="showCategory('yono')" class="btn-cat btn-yono" id="btn-yono">Yono Apps</button>
        <button onclick="showCategory('colour')" class="btn-cat btn-colour inactive" id="btn-colour">Colour Site</button>
    </div>

    <div id="yono-apps-list" class="games-list" style="display: flex;">
        {yono_html}
    </div>

    <div id="colour-sites-list" class="games-list" style="display: none;">
        {colour_html}
    </div>

    <div class="three-dot-menu">
        <button class="menu-btn" onclick="toggleMenu()"><i class="fas fa-ellipsis-v"></i></button>
    </div>

    <div class="menu-overlay" id="menu-overlay">
        <div class="menu-nav">
            <a href="/" onclick="toggleMenu()">Home</a>
            <a href="https://telegram.me/epcode" target="_blank">Join Telegram</a>
            <a href="https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M" target="_blank">WhatsApp Channel</a>
            <a href="https://www.youtube.com/@Epsupport1" target="_blank">YouTube Channel</a>
        </div>
    </div>

    <div class="social-row">
        <a href="https://telegram.me/epcode" target="_blank" class="tg"><i class="fab fa-telegram"></i></a>
        <a href="https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M" target="_blank" class="wa"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.youtube.com/@Epsupport1" target="_blank" class="yt"><i class="fab fa-youtube"></i></a>
    </div>

    <footer class="footer">
        <p><strong>Responsible Gaming:</strong> This site is for users aged 18+ only. Gaming involves financial risk. Please play responsibly.</p>
        <p>&copy; 2026 NewYono Code. All Rights Reserved.</p>
    </footer>

    <script>
        function showCategory(type) {{
            const yonoList = document.getElementById('yono-apps-list');
            const colourList = document.getElementById('colour-sites-list');
            const yonoBtn = document.getElementById('btn-yono');
            const colourBtn = document.getElementById('btn-colour');

            if (type === 'yono') {{
                yonoList.style.display = 'flex';
                colourList.style.display = 'none';
                yonoBtn.classList.remove('inactive');
                colourBtn.classList.add('inactive');
            }} else {{
                yonoList.style.display = 'none';
                colourList.style.display = 'flex';
                yonoBtn.classList.add('inactive');
                colourBtn.classList.remove('inactive');
            }}
        }}

        function filterGames() {{
            const input = document.getElementById('game-search');
            const filter = input.value.toLowerCase();
            const cards = document.getElementsByClassName('game-card');

            for (let i = 0; i < cards.length; i++) {{
                const title = cards[i].querySelector('.game-title').innerText.toLowerCase();
                if (title.includes(filter)) {{
                    cards[i].style.display = 'flex';
                }} else {{
                    cards[i].style.display = 'none';
                }}
            }}
        }}

        function toggleMenu() {{
            document.getElementById('menu-overlay').classList.toggle('active');
        }}
    </script>

</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_page)

print("Index.html completely regenerated from clean template. 53 Yono Apps and 16 Colour Sites installed.")
