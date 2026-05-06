import json
import os
import re

# Load the audit data
with open('audit_results.json', 'r') as f:
    data = json.load(f)

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} APK Download - Official {title} App</title>
    <meta name="description" content="Download {title} APK and get a sign-up bonus of ₹245. Play Rummy, Teen Patti, and Slots on {title}.">
    <link rel="stylesheet" href="../style.css"> <!-- Assuming a main style exists, otherwise we inline -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f4f7f6; margin: 0; padding: 0; color: #333; }}
        .header {{ background: #fff; padding: 15px 20px; display: flex; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 100; }}
        .header img {{ height: 40px; margin-right: 15px; border-radius: 8px; }}
        .header h1 {{ font-size: 20px; margin: 0; text-transform: uppercase; letter-spacing: 1px; }}
        .container {{ max-width: 600px; margin: 20px auto; background: #fff; padding: 30px 20px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }}
        .app-hero {{ display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }}
        .app-icon {{ width: 120px; height: 120px; border-radius: 24px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .app-info h2 {{ margin: 0; font-size: 28px; }}
        .app-info p {{ margin: 5px 0; color: #007bff; font-weight: 600; font-size: 18px; }}
        .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 20px 0; margin-bottom: 30px; text-align: center; }}
        .meta-item i {{ display: block; font-size: 20px; color: #555; margin-bottom: 8px; }}
        .meta-item .value {{ font-weight: 700; font-size: 15px; }}
        .meta-item .label {{ font-size: 12px; color: #888; }}
        .btn {{ display: block; text-align: center; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 16px; margin-bottom: 15px; transition: 0.3s; }}
        .btn-download {{ background: #007bff; color: #fff; box-shadow: 0 4px 15px rgba(0,123,255,0.3); }}
        .btn-tg {{ background: #fff; color: #333; border: 1px solid #eee; display: flex; align-items: center; justify-content: center; gap: 10px; }}
        .btn-tg i {{ color: #0088cc; font-size: 20px; }}
        .description {{ line-height: 1.6; color: #666; font-size: 15px; }}
        .footer {{ text-align: center; padding: 30px; color: #999; font-size: 12px; }}
        @media (max-width: 480px) {{ .meta-grid {{ grid-template-columns: 1fr 1fr; }} }}
    </style>
</head>
<body>
    <header class="header">
        <img src="../ep_code_logo.png" alt="Yono Logo">
        <h1>YONO GAMES</h1>
    </header>

    <div class="container">
        <div class="app-hero">
            <img src="../{icon}" alt="{title}" class="app-icon" onerror="this.src='../ep_code_logo.png'">
            <div class="app-info">
                <h2>{title}</h2>
                <p>{title} APK</p>
            </div>
        </div>

        <div class="meta-grid">
            <div class="meta-item">
                <i class="fas fa-star"></i>
                <div class="value">4.8</div>
                <div class="label">Rating</div>
            </div>
            <div class="meta-item">
                <i class="fas fa-cloud-download-alt"></i>
                <div class="value">58-100 MB</div>
                <div class="label">Size</div>
            </div>
            <div class="meta-item">
                <i class="fas fa-shopping-cart"></i>
                <div class="value">Free</div>
                <div class="label">Price</div>
            </div>
            <div class="meta-item">
                <i class="fas fa-gift"></i>
                <div class="value">₹245</div>
                <div class="label">Upto Bonus</div>
            </div>
        </div>

        <a href="{link}" target="_blank" class="btn btn-download">DOWNLOAD {title_upper}</a>
        <a href="https://telegram.me/epcode" target="_blank" class="btn btn-tg">
            <i class="fab fa-telegram"></i> Join Our Telegram Team
        </a>

        <div class="description">
            <p>Welcome to <strong>{title}</strong>! This is currently one of the most trending online earning applications where you can play games and win real cash.</p>
            <p>Download the <strong>{title} APK</strong> today and get an instant sign-up bonus of ₹245. The app offers a variety of card games like Rummy, Teen Patti, and Slots.</p>
        </div>
    </div>

    <div class="footer">
        &copy; 2024 Yono Games Official. All Rights Reserved.
    </div>
</body>
</html>
"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

# Create pages for Yono Apps
for app in data['yono']:
    slug = slugify(app['title'])
    if not slug: continue
    
    # Check if folder exists
    if not os.path.exists(slug):
        os.makedirs(slug)
    
    # Try to find the icon name
    icon_name = "logo_" + slug + ".png" # Basic guess
    
    html = template.format(
        title=app['title'],
        title_upper=app['title'].upper(),
        link=app['link'],
        icon=icon_name,
        slug=slug
    )
    
    with open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

print(f"Generated {len(data['yono'])} app pages.")
