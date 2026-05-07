import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Footer CSS
footer_css = """
    .site-footer { background: #1a1a1a; color: #f1f1f1; padding: 40px 20px; text-align: center; margin-top: 50px; border-top: 3px solid #d80000; }
    .footer-content { max-width: 800px; margin: 0 auto; }
    .footer-disclaimer { font-size: 12px; color: #999; margin: 15px 0; line-height: 1.6; }
    .footer-links { margin-top: 20px; display: flex; justify-content: center; gap: 20px; }
    .footer-link { color: #fff; text-decoration: none; font-weight: 700; font-size: 14px; }
    .footer-link:hover { color: #d80000; }
    .footer-copy { font-size: 13px; color: #666; margin-top: 25px; }
"""
content = content.replace('</style>', f'{footer_css}\n    </style>', 1)

# 2. Add Footer HTML before the seo-hidden div
footer_html = """
<footer class="site-footer">
    <div class="footer-content">
        <div class="footer-links">
            <a href="/" class="footer-link">Home</a>
            <a href="https://telegram.me/epcode" target="_blank" class="footer-link">Telegram</a>
            <a href="https://telegram.me/epcode" target="_blank" class="footer-link">Contact Us</a>
        </div>
        <p class="footer-disclaimer">
            <strong>Safety Warning:</strong> This website is intended for users 18 years or older. All games listed are for entertainment and informational purposes. Please play responsibly. We are not responsible for any losses incurred on third-party apps or websites.
        </p>
        <div class="footer-copy">
            © 2026 NewYono Code - Your Trusted Yono Games Hub.
        </div>
    </div>
</footer>
"""

if '<footer' in content:
    content = re.sub(r'<footer.*?</footer>', footer_html, content, flags=re.DOTALL)
else:
    content = content.replace('<div class="seo-hidden">', f'{footer_html}\n<div class="seo-hidden">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Professional safety footer added.")
