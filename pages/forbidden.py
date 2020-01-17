"""
This module contains ForbiddenPage,
the page object for the ForbiddenPage.
"""

from selenium.webdriver.common.by import By


class ForbiddenPage:

    header = (By.XPATH, '//h1')

    def __init__(self, browser):
        self.browser = browser

    def get_page_header(self):
        return self.browser.find_element(*self.header).text
