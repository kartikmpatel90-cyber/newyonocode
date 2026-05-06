import os
import json
import re

with open('audit_results.json', 'r') as f:
    data = json.load(f)

def slugify(text):
    return re.sub(r'[^a-z0-9]', '', text.lower().strip())

valid_slugs = set()
for entry in data['yono'] + data['colour']:
    valid_slugs.add(slugify(entry['title']))

# Add protected folders
valid_slugs.add('assets')
valid_slugs.add('.gemini')
valid_slugs.add('.git')
valid_slugs.add('.vercel')

deleted_count = 0
for d in os.listdir('.'):
    if os.path.isdir(d) and d not in valid_slugs:
        # Check if it has an index.html (personal page)
        if os.path.exists(os.path.join(d, 'index.html')):
            print(f"Deleting dead folder: {d}")
            # Use shell command to remove directory on Windows
            os.system(f'rmdir /s /q "{d}"')
            deleted_count += 1

print(f"Cleanup complete. Deleted {deleted_count} dead folders.")
