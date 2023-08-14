import csv
import json

"""CSV/json parser 
        CSV -> list (for input)"""

# NOTE: JSON format is given in the example.json file please do not make any changes to the format
#       (the code will tell you if the format is wrong when it parses - "INCORRECT FORMAT - <type of file>")

final_dict = {"universities": []}  # to write json files into
filename = ""  # add later


def json_parse(jsonfile):
    with open(jsonfile, "r") as jsonfile:
        file = json.load(jsonfile)
        for row in file['universities']:
            if row[14].startswith('https://'):
                regex_url = r'\.'.join(row[14][8:].split('.'))
            else:
                regex_url = r'\.'.join(row[14].split('.'))
            fuzzy_var = row['name']
            username = row['login_id']
            password = row['password']
            url = row['url']  # not added to the example
            if username != '' and username != 'Skip for now':
                final_dict['universities'].append({
                    "name": fuzzy_var,
                    "login_id": username,
                    "password": password,
                    "url": url,
                    "regex_url": regex_url
                })
    print(final_dict)


def csv_parse(csvfile):
    """checks for some common errors in the inputs and skips over them to then convert the input into python format
    NOTE: this parses the format of the existing file
    """
    # TODO: add function to change the index and then store those to further read the file correctly
    with open(csvfile, "r") as file:
        reader = csv.reader(file)
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
            # list_append = [fuzzy_var, username, password, url, fuzzy_var, regex_url]
            if username != '' and username != 'Skip for now':
                final_dict['universities'].append({
                    "name": fuzzy_var,
                    "login_id": username,
                    "password": password,
                    "url": url,
                    "regex_url": regex_url
                })

    print(final_dict)


def check_filetype_run(file: str):
    if file.endswith(".json"):
        print("Working with a JSON file")
        json_parse(file)
    elif file.endswith(".csv"):
        print("Working with a CSV file")
        csv_parse(file)
    else:
        print("NOT A VALID FILE")
    pass


if __name__ == "__main__":
    check_filetype_run("/Users/sidvyas/PycharmProjects/auto_oca_final/configs/Gold Clients (with Passwords) (1).csv")
