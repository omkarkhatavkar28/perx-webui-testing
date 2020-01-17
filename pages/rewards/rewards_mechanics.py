"""
This module contains RewardMechanicsPage,
the page object for the RewardMechanicsPage.
"""

import datetime
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.helper_methods import custom_click, move_to_element, find_element


class RewardMechanicsPage(BasePage):

    breadcrumb = (By.XPATH, "//div[@class='ant-breadcrumb']")
    reward_mechanics_title = (By.XPATH, "//strong[text()='Reward Mechanics']")
    validity_period = (By.XPATH, "//h3[text()='Validity Period']")
    start_date_input = (By.XPATH, "//section[text()='Start Date']/following-sibling::section"
                                  "//input[@placeholder='Select date']")
    start_date_input_time = (By.XPATH, "//section[text()='Start Date']/following-sibling::section"
                                       "//input[@placeholder='Select time']")

    end_date_input = (By.XPATH, "//section[text()='End Date']/following-sibling::section"
                                "//input[@placeholder='Select date']")

    end_date_input_time = (By.XPATH, "//section[text()='End Date']/following-sibling::section"
                                     "//input[@placeholder='Select time']")

    today_date = (By.XPATH, "//td[contains(@class, 'ant-calendar-today')]")

    next_button = (By.XPATH, "//button/span[text()='Next']")
    mandatory_error_message = (By.XPATH, "//label[text()='Start date & end date required']")

    def fill_the_end_date(self, input_data):
        """fill the end date on rewards mechanics page """
        end_date = self.browser.find_element(*self.end_date_input)
        move_to_element(self.browser, end_date)
        end_date.click()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        next_date = "{} {}, {}".format(tomorrow.strftime("%B"), tomorrow.day, tomorrow.year)
        next_date_locator = (By.XPATH, "//td[@title='{}']".format(next_date))
        element = self.browser.find_element(*next_date_locator)
        custom_click(self.browser, element)

    def fill(self, input_data):
        """fill the form on the rewards mechanics page"""
        self.fill_the_end_date(input_data)
        next_button = self.browser.find_element(*self.next_button)
        custom_click(self.browser, next_button)

    def check_error_message(self):
        """return the error message assertion status"""
        next_button = self.browser.find_element(*self.next_button)
        custom_click(self.browser, next_button)
        end_date = self.browser.find_element(*self.end_date_input)
        move_to_element(self.browser, end_date)
        return find_element(self.browser, self.mandatory_error_message)
