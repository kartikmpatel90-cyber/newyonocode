import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Floating Button CSS
float_css = """
    .float-tg {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 65px;
        height: 65px;
        background: #0088cc;
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
        animation: tg-pulse 2s infinite;
    }
    .float-tg:hover { transform: scale(1.1); background: #0099ff; color: #fff; }
    @keyframes tg-pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 136, 204, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(0, 136, 204, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 136, 204, 0); }
    }
"""
content = content.replace('</style>', f'{float_css}\n    </style>', 1)

# 2. Add Floating Button HTML before </body>
float_html = """
<a href="https://telegram.me/epcode" target="_blank" class="float-tg">
    <i class="fab fa-telegram-plane"></i>
</a>
"""

if '<a href="https://telegram.me/epcode" target="_blank" class="float-tg">' not in content:
    content = content.replace('</body>', f'{float_html}\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Floating Telegram button added back.")
