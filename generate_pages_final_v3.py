import json
import os

# Load recovered links
with open('links_recovery.json', 'r', encoding='utf-8') as f:
    links_db = json.load(f)

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} APK Download - Official {title} App</title>
    <meta name="description" content="Download {title} APK and get a sign-up bonus of ₹245. Play Rummy, Teen Patti, and Slots on {title}.">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f4f7f6; margin: 0; padding: 0; color: #333; }}
        .header {{ background: #fff; padding: 15px 20px; display: flex; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 100; }}
        .header img {{ height: 40px; margin-right: 15px; border-radius: 8px; }}
        .header h1 {{ font-size: 18px; margin: 0; text-transform: uppercase; letter-spacing: 1px; }}
        .container {{ max-width: 600px; margin: 20px auto; background: #fff; padding: 30px 20px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }}
        .app-hero {{ display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }}
        .app-icon {{ width: 100px; height: 100px; border-radius: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); object-fit: cover; }}
        .app-info h2 {{ margin: 0; font-size: 24px; }}
        .app-info p {{ margin: 5px 0; color: #007bff; font-weight: 600; font-size: 16px; }}
        .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 20px 0; margin-bottom: 30px; text-align: center; }}
        .meta-item i {{ display: block; font-size: 18px; color: #555; margin-bottom: 5px; }}
        .meta-item .value {{ font-weight: 700; font-size: 14px; }}
        .meta-item .label {{ font-size: 11px; color: #888; }}
        .btn {{ display: block; text-align: center; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 15px; margin-bottom: 15px; transition: 0.3s; }}
        .btn-download {{ background: #007bff; color: #fff; box-shadow: 0 4px 15px rgba(0,123,255,0.3); }}
        .btn-home {{ background: #333; color: #fff; display: flex; align-items: center; justify-content: center; gap: 10px; }}
        .btn-tg {{ background: #fff; color: #333; border: 1px solid #eee; display: flex; align-items: center; justify-content: center; gap: 10px; }}
        .btn-tg i {{ color: #0088cc; font-size: 20px; }}
        .description {{ line-height: 1.6; color: #666; font-size: 14px; }}
        .footer {{ text-align: center; padding: 30px; color: #999; font-size: 12px; }}
        @media (max-width: 480px) {{ .meta-grid {{ grid-template-columns: 1fr 1fr; }} }}
    </style>
</head>
<body>
    <header class="header">
        <a href="../index.html" style="text-decoration: none; color: inherit; display: flex; align-items: center;">
            <img src="../ep_code_logo.png" alt="Yono Logo">
            <h1>NEWYONO CODE</h1>
        </a>
    </header>

    <div class="container">
        <div class="app-hero">
            <img src="{icon_url}" alt="{title}" class="app-icon" onerror="this.src='../ep_code_logo.png'">
            <div class="app-info">
                <h2>{title}</h2>
                <p>{title} Official APK</p>
            </div>
        </div>

        <div class="meta-grid">
            <div class="meta-item"><i class="fas fa-star"></i><div class="value">4.8</div><div class="label">Rating</div></div>
            <div class="meta-item"><i class="fas fa-cloud-download-alt"></i><div class="value">50-100 MB</div><div class="label">Size</div></div>
            <div class="meta-item"><i class="fas fa-shopping-cart"></i><div class="value">Free</div><div class="label">Price</div></div>
            <div class="meta-item"><i class="fas fa-gift"></i><div class="value">₹245</div><div class="label">Upto Bonus</div></div>
        </div>

        <a href="{download_link}" target="_blank" class="btn btn-download">DOWNLOAD {title_upper} APK</a>
        
        <a href="../index.html" class="btn btn-home">
            <i class="fas fa-arrow-left"></i> BACK TO HOME
        </a>

        <a href="https://telegram.me/epcode" target="_blank" class="btn btn-tg">
            <i class="fab fa-telegram"></i> JOIN OUR TELEGRAM
        </a>

        <div class="description">
            <p>Download the latest official <strong>{title}</strong> app and start earning real cash. Get an instant sign-up bonus of up to ₹245. Fast withdrawals and 24/7 support.</p>
        </div>
    </div>

    <div class="footer">
        &copy; 2026 NewYono Code. All Rights Reserved.
    </div>
</body>
</html>
"""

count = 0
for title, data in links_db.items():
    slug = data['internal_link'].strip('/')
    if not slug: continue
    
    if not os.path.exists(slug):
        os.makedirs(slug)
    
    icon_url = data['image']
    if not icon_url.startswith('http'):
        icon_url = "../" + icon_url
        
    html = template.format(
        title=title,
        title_upper=title.upper(),
        download_link=data['download_link'],
        icon_url=icon_url
    )
    
    with open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    count += 1

print(f"Successfully generated {count} personal app pages with correct logos, download links, and BACK buttons.")
