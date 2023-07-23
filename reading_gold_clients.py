import csv
import json

# we are parsing the gold clients list file here to remove data that is not valid
# While making changes or creating a new file to parse :
#       1. Use "Skip for now" in the USERNAME cell to skip the whole row
#       2. Adding username, as some require assist and some do not - not consistent.
#           (this has been handled in the main function - works about 50% of the time)

final_dict = {}  # to write json files into
with open("/configs/Gold Clients (with Passwords) (1).csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        username = row[15]
        password = 'k2win21'
        url = row[14]
        fuzzy_var = row[0]
        if row[14].startswith('https://'):
            regex_url = r'\.'.join(row[14][8:].split('.'))
        else:
            regex_url = r'\.'.join(row[14].split('.'))
        list_append = [fuzzy_var, username, password, url, fuzzy_var, regex_url]
        if username != '' and username != 'Skip for now':
            final_dict[fuzzy_var] = list_append

print(final_dict)
