"""
This module contains RewardReviewPage,
the page object for the RewardReviewPage.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.helper_methods import custom_click, read_widget_data


class RewardReviewPage(BasePage):

    breadcrumb = (By.XPATH, "//div[@class='ant-breadcrumb']")
    reward_review_title = (By.XPATH, "//strong[text()='Review']")
    reward_info_header = (By.XPATH, "//h3[text()='Reward Info']")
    reward_mechanics_header = (By.XPATH, "//h3[text()='Reward Mechanics']")
    reward_info_data = (By.XPATH, "//h3[text()='Reward Info']/parent::div//section")
    reward_mechanics_data = (By.XPATH, "//h3[text()='Reward Mechanics']/parent::div//section")

    launch_button = (By.XPATH, "//button/span[text()='Launch']")
    save_as_draft_button = (By.XPATH, "//button/span[text()='Save as Draft']")

    def read_widget(self, widget_name):
        """return the information data for the widget"""
        if widget_name == 'reward_info':
            return read_widget_data(self.browser, self.reward_info_data)
        elif widget_name == 'reward_mechanics':
            return read_widget_data(self.browser, self.reward_mechanics_data)
        else:
            raise Exception("Not a valid widget name!")

    def launch_reward(self):
        """click on launch reward button"""
        launch_button = self.browser.find_element(*self.launch_button)
        custom_click(self.browser, launch_button)
