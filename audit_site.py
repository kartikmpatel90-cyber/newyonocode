import re
import json
import os
import requests

def extract_games():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the sections
    yono_section_match = re.search(r'id="yono-apps-list".*?</ul>', content, re.DOTALL)
    colour_section_match = re.search(r'id="colour-sites-list".*?</ul>', content, re.DOTALL)

    def extract_from_section(section_text, category):
        if not section_text:
            return []
        # Find all game cards - splitting by </li> or a similar delimiter
        cards = re.findall(r'<li class="game-item".*?</li>', section_text, re.DOTALL)
        results = []
        for card in cards:
            title_match = re.search(r'<h4 class="game-title">(.*?)</h4>', card)
            # Find the first link (usually desktop button or mobile button, they are the same)
            link_match = re.search(r'href="(.*?)"', card)
            rank_match = re.search(r'<div class="game-rank">Rank (\d+)</div>', card)
            
            if title_match and link_match:
                results.append({
                    'title': title_match.group(1).strip(),
                    'link': link_match.group(1).strip(),
                    'rank': rank_match.group(1) if rank_match else None,
                    'category': category
                })
        return results

    yono_apps = extract_from_section(yono_section_match.group(0) if yono_section_match else "", "yono")
    colour_sites = extract_from_section(colour_section_match.group(0) if colour_section_match else "", "colour")
    
    return yono_apps, colour_sites

def check_duplicates(yono_apps, colour_sites):
    yono_titles = {}
    colour_titles = {}
    duplicates = []

    for app in yono_apps:
        title = app['title'].lower()
        if title in yono_titles:
            duplicates.append(f"Duplicate Yono App: {app['title']}")
        yono_titles[title] = True

    for site in colour_sites:
        title = site['title'].lower()
        if title in colour_titles:
            duplicates.append(f"Duplicate Colour Site: {site['title']}")
        colour_titles[title] = True
        
    return duplicates

def check_links(apps):
    results = []
    for app in apps:
        link = app['link']
        title = app['title']
        
        # Check if Telegram
        if "telegram.me" in link or "t.me" in link:
            results.append(f"Link points to Telegram: {title} ({link})")
            continue
            
        # Check if expired (HEAD request for speed)
        try:
            # We use a user-agent to avoid being blocked
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.head(link, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                results.append(f"Expired/Broken Link ({response.status_code}): {title} ({link})")
        except Exception as e:
            results.append(f"Error checking link: {title} ({link}) - {str(e)}")
            
    return results

# Main Execution
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

print("\n--- LINK CHECK (Checking all links, this may take a minute) ---")
all_apps = yono + colour
link_issues = check_links(all_apps)
if not link_issues:
    print("All links seem healthy (or pointing to direct registration).")
else:
    for issue in link_issues:
        print(issue)

# Save results for next step
with open('audit_results.json', 'w') as f:
    json.dump({
        'yono': yono,
        'colour': colour,
        'duplicates': dupes,
        'link_issues': link_issues
    }, f, indent=2)
