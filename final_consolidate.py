import json
import re

# Load source of truth
with open('links_recovery.json', 'r', encoding='utf-8') as f:
    links_db = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update all cards in index.html to use correct internal and download links
# We'll do this by matching the titles (alt text)
def update_card_links(match):
    block = match.group(0)
    title_m = re.search(r'alt="(.*?)"', block)
    if title_m:
        title = title_m.group(1)
        if title in links_db:
            data = links_db[title]
            # Replace internal links (e.g. href="/jaiho91/")
            # We look for hrefs starting with / and not followed by http
            block = re.sub(r'href="/(?!https).*?"', f'href="{data["internal_link"]}"', block)
            # Replace download links (Register buttons)
            # These are hrefs starting with http
            block = re.sub(r'href="https?://.*?"', f'href="{data["download_link"]}"', block)
    return block

content = re.sub(r'<div class="game-card.*?</div>\s*</div>\s*</div>\s*</div>', update_card_links, content, flags=re.DOTALL)

# 2. Consolidate JS and ensure search works
# We'll remove all script blocks from the middle of the file and put one clean one in the head or top of main.
# First, remove all existing script blocks related to search/category
content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)

final_js = """
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

    function toggleMenu() {
        const content = document.getElementById('menu-content');
        content.classList.toggle('active');
    }

    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('game-search');
        if (searchInput) {
            searchInput.addEventListener('input', filterGames);
        }
        
        // Swiper Initialization
        if (typeof Swiper !== 'undefined') {
            new Swiper(".mySwiper", {
                spaceBetween: 15,
                centeredSlides: true,
                loop: true,
                autoplay: { delay: 2500, disableOnInteraction: false },
                pagination: { el: ".swiper-pagination", clickable: true },
            });
        }
    });

    window.onclick = function(event) {
        if (!event.target.matches('.menu-dots') && !event.target.matches('.menu-dots span')) {
            const content = document.getElementById('menu-content');
            if (content && content.classList.contains('active')) {
                content.classList.remove('active');
            }
        }
    }
</script>
"""

# Insert the consolidated script before the closing </head> or at start of main
content = content.replace('</head>', f'{final_js}\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Consolidated JS and updated all game links in index.html.")
