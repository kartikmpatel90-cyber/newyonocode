import re
import json
import requests

def extract_games():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the file into two main parts based on the IDs
    yono_part = ""
    colour_part = ""
    
    yono_start = content.find('id="yono-apps-list"')
    colour_start = content.find('id="colour-sites-list"')
    
    if yono_start != -1:
        if colour_start != -1:
            yono_part = content[yono_start:colour_start]
            colour_part = content[colour_start:]
        else:
            yono_part = content[yono_start:]

    def extract_from_part(part_text, category):
        if not part_text:
            return []
        # Find all game-card divs
        # We look for the start of a card and then the title/link inside
        cards = re.split(r'<div class="game-card"', part_text)[1:] # Skip the first bit before first card
        results = []
        for card in cards:
            title_match = re.search(r'class="game-title">(.*?)</h4>', card, re.DOTALL)
            if not title_match:
                title_match = re.search(r'alt="(.*?)"', card) # Fallback to alt text
            
            if title_match:
                title = title_match.group(1).strip()
                title = re.sub(r'<.*?>', '', title) # Strip HTML tags
            else:
                title = None
            
            link_match = re.search(r'href="(.*?)"', card)
            rank_match = re.search(r'class="game-rank">(\d+)</div>', card)
            
            if title and link_match:
                results.append({
                    'title': title,
                    'link': link_match.group(1).strip(),
                    'rank': rank_match.group(1) if rank_match else None,
                    'category': category
                })
        return results

    yono_apps = extract_from_part(yono_part, "yono")
    colour_sites = extract_from_part(colour_part, "colour")
    
    return yono_apps, colour_sites

def check_duplicates(yono_apps, colour_sites):
    yono_titles = {}
    colour_titles = {}
    duplicates = []

    for app in yono_apps:
        title = app['title'].lower().replace(" ", "").replace("-", "")
        if title in yono_titles:
            duplicates.append(f"Duplicate Yono App: {app['title']}")
        yono_titles[title] = True

    for site in colour_sites:
        title = site['title'].lower().replace(" ", "").replace("-", "")
        if title in colour_titles:
            duplicates.append(f"Duplicate Colour Site: {site['title']}")
        colour_titles[title] = True
        
    return duplicates

def check_links(apps):
    results = []
    for app in apps:
        link = app['link']
        title = app['title']
        
        if "telegram.me" in link or "t.me" in link:
            results.append(f"Link points to Telegram: {title} ({link})")
            continue
            
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            # Using GET with stream=True to avoid downloading large files
            response = requests.get(link, headers=headers, timeout=5, allow_redirects=True, stream=True)
            if response.status_code >= 400:
                results.append(f"Expired/Broken Link ({response.status_code}): {title} ({link})")
            response.close()
        except Exception as e:
            results.append(f"Error checking link: {title} ({link}) - {str(e)}")
            
    return results

print("Scanning index.html...")
yono, colour = extract_games()
print(f"Found {len(yono)} Yono Apps and {len(colour)} Colour Sites.")

print("\n--- DUPLICATES CHECK ---")
dupes = check_duplicates(yono, colour)
if not dupes:
    print("No duplicates found.")
else:
    for d in dupes:
        print(d)

print("\n--- LINK CHECK ---")
all_apps = yono + colour
link_issues = check_links(all_apps)
if not link_issues:
    print("All links seem healthy.")
else:
    for issue in link_issues:
        print(issue)

with open('audit_results.json', 'w') as f:
    json.dump({
        'yono': yono,
        'colour': colour,
        'duplicates': dupes,
        'link_issues': link_issues
    }, f, indent=2)
