import re

# created to add more ebsco specific functions - not pushed to git

url = 'https://search.ebscohost.com/login.aspx?direct=true&db=edsebk&AN=3318731&site=ehost-live'
pattern = r"search\.ebscohost\.com"
match = re.search(pattern, url)
print(match)
