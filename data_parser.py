import csv
import json
import re

"""CSV/json parser 
        CSV -> list (for input)"""

# NOTE: JSON format is given in the example.json file please do not make any changes to the format
#       (the code will tell you if the format is wrong when it parses - "INCORRECT FORMAT - <type of file>")

# input_list in the main function refers to this format -
#       name, url, login_id, password

final_list = []
filename = ""


def json_parse(jsonfile):
    with open(jsonfile, "r") as jsonfile:
        file = json.load(jsonfile)
        for row in file['universities']:
            fuzzy_var = row['name']
            username = row['login_id']
            password = row['password']
            url = row['url']  # not added to the example
            # regex_url = r'\.'.join(url[8:].split('.'))
            regex_url = "vtuconsortia\\.knimbus\\.com/"
            if username != '' and username != 'Skip for now':
                final_list.append([username, password, url, fuzzy_var, regex_url])
    return final_list


def csv_parse(csvfile):
    """checks for some common errors in the inputs and skips over them to then convert the input into python format
    NOTE: this parses the format of the existing file
    """
    # TODO: add function to change the index and then store those to further read the file correctly
    with open(csvfile, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            username = row[2]
            password = row[3]
            url = row[1]
            fuzzy_var = row[0]
            # regex_url = r'\.'.join(url[8:].split('.'))
            regex_url = "vtuconsortia\\.knimbus\\.com/"
            if username != '' and username != 'Skip for now':
                final_list.append([username, password, url, fuzzy_var, regex_url])
    return final_list


def check_filetype_run(file: str):
    if file.endswith(".json"):
        json_parse(file)
    elif file.endswith(".csv"):
        csv_parse(file)
    else:
        print("NOT A VALID FILE")
    return final_list
