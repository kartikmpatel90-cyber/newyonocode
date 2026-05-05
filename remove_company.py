import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'Company' or 'COMPANY' specifically when it follows 'EP code' or is in those common phrases
content = re.sub(r'EP code Company', 'EP code', content, flags=re.I)
content = re.sub(r'EP code COMPANY', 'EP code', content) # Case sensitive for the uppercase one just in case

# Global replacement for any other occurrences that look like "Company Apps"
content = re.sub(r'\bCompany\b', '', content, flags=re.I)

# Clean up double spaces that might have been created
content = re.sub(r'  +', ' ', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed 'Company' from the site.")
