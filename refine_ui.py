import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove redundant mobile secondary menu (ast-below-header-wrap)
mobile_sec_pattern = re.compile(r'<!-- Mobile Header -->.*?<div class="ast-below-header-wrap ">.*?</div>\s*<div class="ast-mobile-header-content', re.DOTALL)
if mobile_sec_pattern.search(html):
    html = mobile_sec_pattern.sub('<!-- Mobile Header -->\n            <div class="ast-mobile-header-content', html)
    print("Removed redundant mobile secondary menu.")

# 2. Fix the banner to be even smaller and more rectangular
img_pattern = re.compile(r'<img[^>]*src="ep_code_banner\.png"[^>]*>')
if img_pattern.search(html):
    new_img = '<img src="ep_code_banner.png" alt="Promo Banner" style="width: 100%; max-width: 600px; margin: 0 auto; max-height: 80px; object-fit: cover; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: block;">'
    html = img_pattern.sub(new_img, html)
    print("Banner updated to be slimmer (80px height).")

# 3. Move the "Important Notice Box" to the bottom (above footer)
notice_pattern = re.compile(r'<!-- Important Notice Box \(Pink\) -->.*?<section class="important-notice-section">.*?</section>', re.DOTALL)
notice_match = notice_pattern.search(html)
if notice_match:
    notice_html = notice_match.group(0)
    html = html.replace(notice_html, "")
    # Place it above the footer
    html = html.replace('<footer class="site-footer">', notice_html + '\n    <footer class="site-footer">')
    print("Moved Important Notice Box to the bottom.")

# 4. Simplify the Footer
footer_pattern = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)
if footer_pattern.search(html):
    simplified_footer = """
    <footer class="site-footer" style="padding: 20px 10px; background: #f8f9fa; border-top: 1px solid #eee; text-align: center;">
        <div style="max-width: 800px; margin: 0 auto;">
            <div style="font-size: 12px; color: #666; margin-bottom: 15px; line-height: 1.6;">
                <strong>Disclaimer:</strong> EP code is an independent platform for app discovery. Online gaming involves financial risk. 
                Rummy is banned in AP, Sikkim, Nagaland, Assam, TN, Odisha, and Telangana. 18+ only.
            </div>
            <div style="margin-bottom: 15px;">
                <a href="https://telegram.me/epcode" target="_blank" style="background: #0088cc; color: #fff; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-size: 14px; display: inline-flex; align-items: center; gap: 8px;">
                    <i class="fab fa-telegram-plane"></i> Join Telegram
                </a>
            </div>
            <div style="font-size: 11px; color: #999;">
                Copyright © 2026 EP code. All rights reserved.
            </div>
        </div>
    </footer>
    """
    html = footer_pattern.sub(simplified_footer, html)
    print("Simplified footer implemented.")

# 5. Remove "Thanks Message" if it exists (it's redundant)
thanks_pattern = re.compile(r'<!-- Thanks Message -->.*?<div class="thanks-message">.*?</div>', re.DOTALL)
if thanks_pattern.search(html):
    html = thanks_pattern.sub('', html)
    print("Removed Thanks Message.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
