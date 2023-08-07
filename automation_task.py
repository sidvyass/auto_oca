import os
import time
import re
import json
import csv

from thefuzz import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# TODO: CHANGE THIS TO YOUR SPECIFIC DRIVER
os.environ['PATH'] += r"users/sidvyas/selenium_drivers"

time_of_running = time.ctime()  # add this to final output
data_frame = []  # final output
list_x_paths = []  # list of all connectors
names_all = []  # names of all connectors
ebsco_codes_list = ['SA1424', 'SA1186', 'SA1016']


class AutoOca2:

    def __init__(self, username, password, url, fuzzy_var, regex_url):  # TODO: take these from a list
        self.driver = webdriver.Chrome()
        self.username = username
        self.password = password
        self.url = url
        self.fuzzy_var = fuzzy_var
        self.regex_url = regex_url
        self.university_name = fuzzy_var

    def initialise_page(self):
        """get initial page - logs in and goes to off campus page, functions called below"""
        self.driver.get(self.url)
        self.driver.maximize_window()
        try:
            self.driver.find_element(By.XPATH, "//*[@id='userLogin']").click()
            self.driver.implicitly_wait(5)
        except NoSuchElementException:
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.XPATH, "//*[@id='userLogin']").click()

        self.go_to_off_campus_page()

    def login(self):
        """finds the login window and logs in -- this only works 60% of the time for some reason"""
        try:
            self.driver.implicitly_wait(10)
            user_id = self.driver.find_element(By.NAME, "emailId")
            user_id.send_keys(self.username)
            password_element = self.driver.find_element(By.NAME, "password")
            password_element.send_keys(self.password)
            password_element.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.XPATH, '//*[@id="userLoginBlock"]/div/div/div/div[5]/a').click()
            user_id = self.driver.find_element(By.NAME, "emailId")
            user_id.send_keys(self.username)
            password_element = self.driver.find_element(By.NAME, "password")
            password_element.send_keys(self.password)
            password_element.send_keys(Keys.ENTER)

    def go_to_off_campus_page(self):
        """Opens the publisher's page - finds all connectors called below"""

        self.login()

        try:  # TODO: add logging
            self.driver.find_element(By.XPATH, "//*[@id='navMenuBlock']/li[7]/a").click()
            time.sleep(5)
        except ElementNotInteractableException:
            self.driver.implicitly_wait(5)
            element = self.driver.find_element(By.XPATH, "//*[@id='navMenuBlock']/li[7]/a")
            if element:
                element.click()
            else:
                return None

        self.find_all_connectors()

    def find_all_connectors(self):
        """Stores all publisher's xpaths in "link_x_paths" list"""
        total = self.driver.find_elements(By.CLASS_NAME, 'raWidgetCard')
        for idx, element in enumerate(total):
            try:
                connector = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
                name = self.driver.find_element(By.XPATH, f'//*[@id="mainContainer"]/div/div/div[2]/div/div[1]/div['
                                                          f'2]/div[2]/div/div/div/div/div/div[{idx + 1}]/div/a/span['
                                                          f'3]').text
                if len(connector) == 75:
                    code = connector[-9:-4]
                    list_x_paths.append((code, f"//*[@id='mainContainer']/div/div/div[2]/div/div[1]/div[2]/div["
                                               f"2]/div/div/div/div/div/div[{idx + 1}]/div/a"))
                else:
                    code = connector[-10:-4]
                    list_x_paths.append((code, f"//*[@id='mainContainer']/div/div/div[2]/div/div[1]/div[2]/div["
                                               f"2]/div/div/div/div/div/div[{idx + 1}]/div/a"))
                names_all.append(name)
            except NoSuchElementException:
                continue

    def click_link(self, y):
        """click the link with the xpath provided to it"""
        try:
            link = self.driver.find_element(By.XPATH, list_x_paths[y][1])  # pulling xpath - stored in find_all_connectors
            link.click()
            self.driver.implicitly_wait(5)
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            pass

    def running_checks(self, y):
        """Checks for multiple windows first. Then window switches and the checks run, after which driver returns to the original window"""
        # multiple window checks
        windows = self.driver.window_handles
        if (len(windows) > 2) and (y <= 4):  # pop up check
            time.sleep(30)
        self.driver.switch_to.window(windows[1])

        start_time = time.time()
        data = self.get_url_text()  # (RETURNS (text, url))?
        if list_x_paths[y][0] in ebsco_codes_list:  # ebsco only check
            self.ebsco_check(self.driver.current_url)
        else:
            self.check_url_text(*data, start_time, y=y)  # main check - y = index number we have to pull data from. (PRODUCES FINAL RESULT)

        self.driver.close()
        self.driver.switch_to.window(windows[0])

    def get_url_text(self):
        """returns (text,url) of the link opened"""
        try:
            text = self.driver.find_element(By.TAG_NAME, 'body').text
        except StaleElementReferenceException:
            text = self.driver.find_element(By.TAG_NAME, 'body').text
        url = self.driver.current_url
        pair = (text, url)
        return pair

    def check_url_text(self, text, url, start_time, y):
        """
        :param text: Text that was returned in get_url_text()
        :param url: URL returned in get_url_text()
        :param start_time: started when the loop began
        :param y: the index that we need to pull the result from - also opens the link of the perspective xpaths
        :return: name of the publisher, connector code, load time, *check result has 2 -> URL check - passed or incomplete, Fuzzy text matching result
         - passed, failed, user not logged in, error - no text,
        """
        check_result = []

        end_time = time.time()
        url_search = re.search(re.compile(self.regex_url), url)
        if url_search:
            check_result.append("Passed")
            if self.fuzzy_check(text) == "passed":
                check_result.append("passed")
                self.screenshot(y)
            elif re.search(re.compile(r"error", re.IGNORECASE), text):
                check_result.append('Error - site has no text')
            elif "User not logged in" in text.casefold():
                check_result.append('User not logged in')
            else:
                check_result.append("Failed")
        else:
            check_result.append("URL check failed")
        load_time = round(end_time-start_time)
        list_final_output = [names_all[y], list_x_paths[y][0], load_time, *check_result]  # connector name
        print(list_final_output)
        data_frame.append(list_final_output)

    def fuzzy_check(self, text):
        list1 = text.split("\n")
        for element in list1:
            ratio = fuzz.token_set_ratio(self.fuzzy_var, element)
            if ratio > 75:
                return "passed"

        return "failed"

    @staticmethod
    def ebsco_check(url):
        pattern = r"search\.ebscohost\.com"
        match = re.search(pattern, url)
        if match:
            "passed"
        else:
            "failed"

    def screenshot(self, num):
        directory = f"/Users/sidvyas/PycharmProjects/OCA_automation_v2/{self.university_name}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = f"{directory}/{list_x_paths[num][0]}.png"
        self.driver.save_screenshot(file_name)

    @staticmethod
    def data_return_csv(list_rows, name_csv):
        fields = ['connector_name', "connector_code", 'load_time', 'url_check', 'text_check']
        with open(f'{name_csv}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            writer.writerows(list_rows)
