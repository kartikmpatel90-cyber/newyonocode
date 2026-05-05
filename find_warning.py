import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for "colour-sites-list" and print the first 1000 characters inside it to see the warning block
list_match = re.search(r'<div class="games-list" id="colour-sites-list" style="display: none;">(.*?)</div>\s*<!-- Scrolling Marquee -->', html, re.DOTALL)
if list_match:
    print("Found list. First 500 chars:")
    print(list_match.group(1)[:500])
    
    # Or let's look for "warning" or "note" in the whole HTML
    for m in re.finditer(r'<div[^>]*>.*?Note.*?</div>', list_match.group(1), re.IGNORECASE | re.DOTALL):
        print("\nPossible warning block:")
        print(m.group(0)[:300])
        break
