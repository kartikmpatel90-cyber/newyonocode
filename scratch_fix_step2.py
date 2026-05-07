import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix CSS
new_styles = """
    .search-container { padding: 10px 15px; margin-bottom: 5px; display: flex; justify-content: center; }
    .search-box { position: relative; width: 100%; max-width: 400px; }
    .search-box input { width: 100%; padding: 12px 15px 12px 40px; border-radius: 10px; border: 1px solid #ddd; font-size: 16px; outline: none; box-sizing: border-box; }
    .search-icon { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #666; pointer-events: none; }
    
    .category-filters { display: flex; justify-content: center; gap: 10px; margin: 20px 0; padding: 0 10px; }
    .btn-cat { flex: 1; max-width: 200px; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: 700; color: #fff; transition: 0.3s; text-align: center; cursor: pointer; border: none; }
    .btn-yono { background: #d80000; }
    .btn-colour { background: #009c18; }
    .btn-cat.inactive { opacity: 0.4; filter: grayscale(0.8); }
"""

# Insert the styles before the closing </style> tag in the head
content = content.replace('</style>', f'{new_styles}\n    </style>', 1)

# 2. Fix HTML for buttons
content = re.sub(r'<div class="category-filters">.*?</div>', 
                r'<div class="category-filters">\n    <button onclick="showCategory(\'yono\')" class="btn-cat btn-yono">Yono Apps</button>\n    <button onclick="showCategory(\'colour\')" class="btn-cat btn-colour inactive">Colour Site</button>\n</div>', 
                content, flags=re.DOTALL)

# 3. Fix JS for switching
switch_js = """
    function showCategory(cat) {
        const yonoList = document.getElementById('yono-apps-list');
        const colourList = document.getElementById('colour-sites-list');
        const yonoBtn = document.querySelector('.btn-yono');
        const colourBtn = document.querySelector('.btn-colour');
        
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
    }
"""

# Insert JS into the script block
content = content.replace('document.addEventListener', f'{switch_js}\n    document.addEventListener', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Search bar and category switching logic fixed.")
