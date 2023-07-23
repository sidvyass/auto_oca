from automation_task import *
import json
import time
import multiprocessing

# FIRST-make a main loop function which will iterate over each publisher DONE
#      - retry function that is hit when the code breaks on the login/find_connectors
# THIRD-data entry - sql or something robust that will save files even if the code breaks in the middle - SOLVE
# LAST - functionality to run periodically DONE


data_list_input = []
filepath = "configs/data_set2.json"  # only takes json input - put entire path here


def main_loop(input_list):
    """iterates over each university and gives a csv file as the output after the checks are done"""
    university_name = input_list[3]
    print(input_list, university_name, sep='\n')
    website = AutoOca2(*input_list)
    website.initialise_page()
    try:
        for counter in range(len(list_x_paths)):  # this counter = driver clicking on the publisher
            website.click_link(counter)
            website.running_checks(counter)

        website.data_return_csv(data_frame, f'{university_name}_oca')
        website.driver.close()
    except IndexError:
        website.data_return_csv(data_frame, f'{university_name}_oca')
        website.driver.close()


def load_json():
    """we will load a json file here and then parse it into a variable that python can use. Also checks if the data is correctly formatted"""
    with open(filepath, 'r') as file:
        data = json.load(file)

        for university_name in data:
            password = 'k2win21'

            if data[university_name][1].startswith("assist."):
                username = data[university_name][1]
            else:
                username = "assist." + data[university_name][1]
            if data[university_name][3].startswith("https://"):
                url = data[university_name][3]
            else:
                url = "https://" + data[university_name][3]

            fuzzy_var = data[university_name][4]
            regex_url = data[university_name][5]
            data_list_input.append([username, password, url, fuzzy_var, regex_url])
    return data_list_input


def multiprocessing_func(function, no_of_processes: int, data_list):
    """
    :param function: Main function in this case, param 3 is the input
    :param no_of_processes: int depending on how heavy - current limit unknown
    :param data_list: the list that gives the input to the function
    :return: None "completed" is printed after all of them are over
    """
    stop_index = len(data_list_input)-1
    x = 0
    try:
        while x < stop_index:  # to iterate over all the inputs in the dataset
            processes_list = []
            for i in range(no_of_processes):  # looping over 5 processes at once and waiting for them to finish
                p = multiprocessing.Process(name=f"process{i+x}", target=function, args=(data_list[i+x],))  # i+x is the correct index for data
                p.start()
                print(p.name + " started")
                processes_list.append(p)

            for process in processes_list:
                process.join()
            x += 5  # increment to be able to run only 5 processes at a given time
    except IndexError:  # will always give due to the increment being an odd number - but covers all the inputs even in the len is odd or even
        return None
    print("completed")


if __name__ == "__main__":
    load_json()  # appends the data to data_list_input
    multiprocessing_func(main_loop, 5, data_list_input)






