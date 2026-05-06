from bs4 import BeautifulSoup
import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

yono_apps = []
yono_list = soup.find(id='yono-apps-list')
if yono_list:
    cards = yono_list.find_all(class_='game-card')
    for card in cards:
        title = card.find(class_='game-title').text.strip()
        link_tag = card.find('a', href=True)
        link = link_tag['href'] if link_tag else None
        yono_apps.append({'title': title, 'link': link, 'category': 'yono'})

colour_sites = []
colour_list = soup.find(id='colour-sites-list')
if colour_list:
    cards = colour_list.find_all(class_='game-card')
    for card in cards:
        title = card.find(class_='game-title').text.strip()
        link_tag = card.find('a', href=True)
        link = link_tag['href'] if link_tag else None
        colour_sites.append({'title': title, 'link': link, 'category': 'colour'})

print(json.dumps({'yono': yono_apps, 'colour': colour_sites}, indent=2))
