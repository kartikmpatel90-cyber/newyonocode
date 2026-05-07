import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Floating Buttons CSS
float_wa_css = """
    .float-wa {
        position: fixed;
        bottom: 105px;
        right: 25px;
        width: 65px;
        height: 65px;
        background: #25d366;
        color: #fff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 9999;
        text-decoration: none;
        transition: all 0.3s ease;
        animation: wa-pulse 2s infinite;
    }
    .float-wa:hover { transform: scale(1.1); background: #1ebea5; color: #fff; }
    @keyframes wa-pulse {
        0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(37, 211, 102, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
    }
"""
if '.float-wa' not in content:
    content = content.replace('</style>', f'{float_wa_css}\n    </style>', 1)

# 2. Update Footer HTML to include WhatsApp
wa_link = "https://whatsapp.com/channel/0029VaB2Jr07YSd9ARkGvL2M"
content = content.replace('<a href="https://telegram.me/epcode" target="_blank" class="footer-link">Telegram</a>',
                          f'<a href="https://telegram.me/epcode" target="_blank" class="footer-link">Telegram</a>\n            <a href="{wa_link}" target="_blank" class="footer-link">WhatsApp</a>')

# 3. Add Floating WhatsApp Button HTML before Telegram button
wa_float_html = f"""
<a href="{wa_link}" target="_blank" class="float-wa">
    <i class="fab fa-whatsapp"></i>
</a>
"""

if 'class="float-wa"' not in content:
    content = content.replace('<a href="https://telegram.me/epcode" target="_blank" class="float-tg">',
                              f'{wa_float_html}\n<a href="https://telegram.me/epcode" target="_blank" class="float-tg">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("WhatsApp channel added to both footer and floating buttons.")
