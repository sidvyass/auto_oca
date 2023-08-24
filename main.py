from automation_task import *
import data_parser
import multiprocessing
import json

with open("config.json", "r") as configs:
    data = json.load(configs)
    filepath = data["configs"]["input file path"]

data_list_input = data_parser.check_filetype_run(filepath)


def main_loop(input_list):  # this needs to be able to open 5-6 windows and check after which it closes all of them
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
        print("completed")
    print("completed")


if __name__ == "__main__":
    print("[username, password, url, name, regex]")
    for data in data_list_input:
        print(data, "\n")
    user_input = input(f"Please check the following data and the format\nType: (y/yes/no)\n")
    if user_input == "Y" or "yes".casefold():
        if len(data_list_input) == 1:  # 1 case cannot run any loops
            main_loop(data_list_input[0])
        else:
            multiprocessing_func(main_loop, 5, data_list_input)
    elif user_input == "n" or "no".casefold():
        print("terminated")
