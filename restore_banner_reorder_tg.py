import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Restore the Banner and Search Bar at the TOP of <main>
# We'll insert them after the </script> and before <div class="category-filters">
banner_search_html = """
<div class="rollable-banner-container">
    <div class="swiper bannerSwiper">
        <div class="swiper-wrapper">
            <div class="swiper-slide"><a href="https://telegram.me/epcode" target="_blank"><img src="ep_code_banner.png" alt="Join EP Code Telegram" loading="lazy"></a></div>
        </div>
        <div class="swiper-pagination"></div>
    </div>
</div>

<div class="game-search-container">
    <div class="search-wrapper">
        <i class="fas fa-search search-icon"></i>
        <input type="text" id="game-search" placeholder="Search apps or sites..." aria-label="Search">
    </div>
</div>
"""

# Insert after the closing script tag of the search/category logic
content = content.replace('</script>\n<div class="category-filters">', f'</script>\n{banner_search_html}\n<div class="category-filters">')

# 2. Fix Floating Buttons Order: Telegram FIRST (Top), WhatsApp SECOND (Bottom)
# We'll swap their bottom positions
content = content.replace('.float-tg {\n        position: fixed;\n        bottom: 25px;', 
                          '.float-tg {\n        position: fixed;\n        bottom: 105px;')
content = content.replace('.float-wa {\n        position: fixed;\n        bottom: 105px;', 
                          '.float-wa {\n        position: fixed;\n        bottom: 25px;')

# 3. Footer Links: Use Logos/Icons instead of text, or just clean up as requested
# User said "i asked for telegram logo or watsep logo no any benner ?"
# I'll replace the text links with Font Awesome icons in the footer
footer_links_new = """
        <div class="footer-links">
            <a href="/" class="footer-link">Home</a>
            <a href="https://telegram.me/epcode" target="_blank" class="footer-link"><i class="fab fa-telegram"></i> Telegram</a>
            <a href="https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M" target="_blank" class="footer-link"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        </div>
"""
content = re.sub(r'<div class="footer-links">.*?</div>', footer_links_new, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Banner and Search restored to the top. Floating buttons order swapped. Footer updated with icons.")
