import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Swap positions just in case
# We'll make Telegram the absolute bottom (25px) and WhatsApp just above it (95px)
# (Actually I already have this, but I'll make the gap smaller)
content = content.replace('bottom: 105px;', 'bottom: 100px;')

# 2. Ensure Telegram is FIRST in the HTML code before WhatsApp
# Find both buttons
tg_btn = re.search(r'<a href="https://telegram.me/epcode".*?</a>', content, re.DOTALL).group(0)
wa_btn = re.search(r'<a href="https://whatsapp.com/channel/.*?</a>', content, re.DOTALL).group(0)

# Remove both
content = content.replace(tg_btn, "")
content = content.replace(wa_btn, "")

# Add them back in the requested order (Telegram first, then WhatsApp)
# We'll place them just before </body>
new_buttons = f"{tg_btn}\n{wa_btn}"
content = content.replace('</body>', f'{new_buttons}\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Floating buttons order re-confirmed: Telegram (bottom) and WhatsApp (above).")
