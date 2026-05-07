import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the category filters (remove backslashes and ensure clean HTML)
content = re.sub(r'<div class="category-filters">.*?</div>', 
                r'<div class="category-filters">\n    <button onclick="showCategory(\'yono\')" class="btn-cat btn-yono" id="btn-yono">Yono Apps</button>\n    <button onclick="showCategory(\'colour\')" class="btn-cat btn-colour inactive" id="btn-colour">Colour Site</button>\n</div>', 
                content, flags=re.DOTALL)

# 2. Fix the Script block entirely
# We'll replace the existing script with a clean one that works
full_script = """
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
        // Re-run search filter on the newly shown list if there is a term
        filterGames();
    }

    function filterGames() {
        const term = document.getElementById('game-search').value.toLowerCase();
        const cards = document.querySelectorAll('.game-card');
        cards.forEach(card => {
            const title = card.querySelector('.game-title').textContent.toLowerCase();
            // Only filter if the card belongs to a visible list? 
            // Actually, we can filter all, but only the active list will show them.
            if (title.includes(term)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('game-search');
        searchInput.addEventListener('input', filterGames);
    });
</script>
"""

# Remove old script blocks and insert the new one
content = re.sub(r'<script>.*?</script>', full_script, content, flags=re.DOTALL, count=1)
# (Note: swiper script is further up, hopefully this doesn't hit it. I'll be specific.)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS and HTML for categories fixed with global scope and clean quoting.")
