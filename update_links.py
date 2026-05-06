import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

updates = {
    "RAJA LUCK": "http://iIHpI72481.rajaluckelite.com/#/wheelspinevent?invitationCode=iIHpI72481",
    "Jai club": "https://www.jaiclub27.com/#/register?invitationCode=74165105915",
    "Jai Club": "https://www.jaiclub27.com/#/register?invitationCode=74165105915",
    "Ind Rummy": "https://indrummyvip7.com/?code=2BAFA7C2NBR&t=1778086890",
    "Rummy Ludo": "https://rummyludo14.com/?code=UWPYNMAJYGB&t=1778086957",
    "GO GO RUMMY": "https://www.gorummynow.com/?code=8FWC5NAXS52&t=1778086986",
    "Yn777": "https://www.y754.com/?code=4SWDFTJSUGB&t=1778087053",
    "Club INR": "https://clubinrvip.cc/?code=9VCW8CFXK5S&t=1778087136",
    "Maha Games": "https://s-mahagames.com/?code=J24HT78EKHV&t=1778087197",
    "Top Rummy": "https://www.toprummy.cc/?code=7K9E8SHZ7JX&t=1778087229",
    "Yono Arcade": "https://yonoarcadeapk30.com/?code=F55LVS2E1DS&t=1778087256",
    "Slots Winner": "https://slotswinnert.com/?code=K4EEPMSLZ9K&t=1778087287",
    "Yono Slots": "https://www.yonoslotsu.com/?code=PJBPR34BZQ1&t=1778087320"
}

removals = ["Bet213", "Bet 213", "777 Game", "Gogo Rummy"]

# Process removals and updates
def process_html(html_content):
    # Split by game cards
    cards = re.split(r'(<div class="game-card".*?</div>\s*</div>\s*</div>)', html_content, flags=re.DOTALL)
    
    new_cards = []
    for card in cards:
        if '<div class="game-card"' in card:
            title_match = re.search(r'class="game-title">(.*?)</h4>', card)
            if not title_match:
                title_match = re.search(r'alt="(.*?)"', card)
            
            if title_match:
                title = title_match.group(1).strip()
                
                # Check for removals
                if any(r.lower() == title.lower() for r in removals):
                    print(f"Removing blank/requested game: {title}")
                    continue
                
                # Check for updates
                for u_title, u_link in updates.items():
                    if u_title.lower() == title.lower():
                        print(f"Updating link for: {title}")
                        # Replace all hrefs in this card
                        card = re.sub(r'href="(.*?)"', f'href="{u_link}"', card)
        
        new_cards.append(card)
    
    return "".join(new_cards)

updated_content = process_html(content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("HTML update complete.")
