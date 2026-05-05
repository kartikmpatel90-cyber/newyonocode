import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove Secondary Navigation
nav_pattern = re.compile(r'<!-- Secondary Navigation -->.*?<!-- SEO Banner -->', re.DOTALL)
if nav_pattern.search(html):
    html = nav_pattern.sub('<!-- SEO Banner -->', html)
    print("Secondary Navigation removed.")

# 2. Modify Banner
img_pattern = re.compile(r'<img[^>]*src="ep_code_banner\.png"[^>]*>')
if img_pattern.search(html):
    new_img = '<img src="ep_code_banner.png" alt="Promo Banner" style="width: 100%; max-width: 600px; margin: 0 auto; max-height: 120px; object-fit: cover; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: block;">'
    html = img_pattern.sub(new_img, html)
    print("Banner updated to be smaller and rectangular.")

# 3. Remove About Section
about_pattern = re.compile(r'<!-- About Section \(Long Content\) -->.*?</section>', re.DOTALL)
if about_pattern.search(html):
    html = about_pattern.sub('', html)
    print("About Section removed.")

# 4. Move Warning Text in Colour Sites List
# Let's find the warning text block. Usually I put it in an "info-alert" or similar style block at the top.
# Let's search for the colour sites list id.
list_match = re.search(r'<div class="games-list" id="colour-sites-list" style="display: none;">(.*?)</div>\s*<!-- Scrolling Marquee -->', html, re.DOTALL)

if list_match:
    content = list_match.group(1)
    # The warning block was added as <div style="background-color: #fff3cd...
    warning_match = re.search(r'(<div style="background-color: #fff3cd; color: #856404; padding: 12px; margin-bottom: 15px; border-radius: 8px; border-left: 5px solid #ffeeba; font-size: 14px; line-height: 1.5;">.*?</div>)', content, re.DOTALL)
    if warning_match:
        warning_block = warning_match.group(1)
        # remove it from its current position
        content_without_warning = content.replace(warning_block, "")
        # append it to the end
        new_content = content_without_warning + "\n" + warning_block
        
        # substitute back
        html = html.replace(list_match.group(1), new_content)
        print("Warning moved to bottom.")
    else:
        print("Warning block not found exactly as expected.")
else:
    print("Colour sites list not found.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
