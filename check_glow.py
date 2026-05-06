import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for Rank 2 in Yono list
yono_list = content[content.find('id="yono-apps-list"'):]
rank2_pos = yono_list.find('class="game-rank">2</div>')
if rank2_pos != -1:
    # Check if 'hot-card' is in the div BEFORE this rank
    context = yono_list[rank2_pos-100:rank2_pos]
    if 'hot-card' in context:
        print("ALERT: Rank 2 has glow!")
    else:
        print("SUCCESS: Rank 2 has NO glow.")
else:
    print("Rank 2 not found.")
