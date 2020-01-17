"""
This module contains RewardDetailsPage,
the page object for the RewardDetailsPage.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.helper_methods import read_widget_data


class RewardDetailsPage(BasePage):

    breadcrumb = (By.XPATH, "//div[@class='ant-breadcrumb']")
    reward_info_data = (By.XPATH, "//h3[text()='Reward Info']/parent::div//section")
    reward_mechanics_data = (By.XPATH, "//h3[text()='Reward Mechanics']/parent::div//section")
    edit_button = (By.XPATH, "//button/span[text()='Edit']")

    def read_widget(self, widget_name):
        """return the information data for the widget"""
        if widget_name == 'reward_info':
            return read_widget_data(self.browser, self.reward_info_data)
        elif widget_name == 'reward_mechanics':
            return read_widget_data(self.browser, self.reward_mechanics_data)
        else:
            raise Exception("Not a valid widget name!")
