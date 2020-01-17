import ntpath
import time
import os
import json
from wait_for import wait_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from utils.exceptions import ErrorMessageException
from pathlib import Path
from fauxfactory import gen_string

ENSURE_PAGE_SAFE = '''\
        return {
            jquery: (typeof jQuery === "undefined") ? true : jQuery.active < 1,
            prototype: (typeof Ajax === "undefined") ? true : Ajax.activeRequestCount < 1,
            document: document.readyState == "complete"
        }
        '''

config_path = 'config.json'


def custom_click(browser, element):
    """Customized click method for elements which need the mouse movement"""
    time.sleep(1)
    webdriver.ActionChains(browser).move_to_element(element).click(element).perform()


def move_to_element(browser, element):
    """Customized method for elements which need the scroll down"""
    browser.execute_script("arguments[0].scrollIntoView();", element)


def get_file_name(path):
    """get the file name from file path"""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def ensure_no_error_message(browser, error_locator):
    """checks if error message has encounter and it will raise in case if
    error message arrived"""
    try:
        # Adding below logic to avoid Stale Element Exception
        browser.find_element(*error_locator).text
        error_text = browser.find_element(*error_locator).text
        if error_text is not None:
            raise ErrorMessageException("{}".format(error_text))
    except NoSuchElementException:
        pass


def ensure_page_safe(browser, timeout='10s'):
    """It internally uses the javascript check to see if the page is loaded correctly,
    if not it will wait"""
    # THIS ONE SHOULD ALWAYS USE JAVASCRIPT ONLY, NO OTHER SELENIUM INTERACTION

    def _check():
        result = browser.execute_script(ENSURE_PAGE_SAFE)
        # TODO: Logging
        try:
            return all(result.values())
        except AttributeError:
            return True
    wait_for(_check, timeout=timeout, delay=2, very_quiet=True)


def wait_for_element_displayed(element, timeout=3):
    """custom wait for element should get displayed"""
    wait_for(lambda: element.is_displayed(), delay=1, num_sec=timeout)


def wait_for_element(browser, locator, text=None):
    """Wait for presence or visibility of elements specified by a locator."""
    ensure_page_safe(browser)
    # added sleep for synchronisation
    time.sleep(2)
    if text is not None:
        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(locator)
    )


def read_table(browser, table_locator, row_number=None):
    """helper function to read the data from web table"""
    table_id = browser.find_element(*table_locator)
    rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
    headers = rows[0].find_elements(By.TAG_NAME, "th")
    keys = [header.text for header in headers]
    data = []
    if row_number is not None:
        for row in rows[row_number:(row_number+1)]:
            row_data = {}
            cols = row.find_elements(By.TAG_NAME, "td")
            for key, value in zip(keys, cols):
                row_data[key] = value
            data.append(row_data)
            return data
    for row in rows[1:]:
        # Get the columns (all the data from column 2)
        row_data = {}
        cols = row.find_elements(By.TAG_NAME, "td")
        for key, value in zip(keys, cols):
            row_data[key] = value.text
        data.append(row_data)
        del row_data
    return data


def read_widget_data(browser, locator):
    """this will help to get the widget information data"""
    return browser.find_element(*locator).text
    # Todo Need to Find Some Better Solution


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent


def get_config():
    """" Read the JSON config file and returns it as a parsed dict """
    with open(config_path) as config_file:
        data = json.load(config_file)
    return data


def get_file_paths(file_type):
    """return the valid and invalid file paths from a folder"""
    root = get_project_root()
    if file_type == 'valid':
        base_path = Path("{}/valid_files".format(root))
        for filename in os.listdir(base_path):
            if filename.startswith("file_"):
                name, extension = filename.split('.')
                file_rename = "file_{}.{}".format(gen_string('alpha'), extension)
                os.rename("{}/{}".format(base_path, filename),
                          "{}/{}".format(base_path, file_rename))
        return [entry for entry in base_path.iterdir() if entry.is_file()]
    elif file_type == 'invalid':
        base_path = Path("{}/invalid_files".format(root))
        return [entry for entry in base_path.iterdir() if entry.is_file()]
    else:
        raise Exception("Missing/Invalid file type parameter")


def select_value_from_drop_down(browser, locator, value):
    """custom helper method to select the value from drop down"""
    # added sleep for synchronisation
    time.sleep(2)
    element = browser.find_element(*locator)
    li_locator = (By.XPATH, "//li")
    elements = element.find_elements(*li_locator)
    for element in elements:
        if element.text == value:
            element.click()


def find_element(browser, locator):
    """custom helper method if find element without raising the exception"""
    try:
        if browser.find_element(*locator).is_displayed():
            return True
    except NoSuchElementException:
        return False
