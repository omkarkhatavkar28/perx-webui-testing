"""
This module contains RewardInfoPage,
the page object for the RewardInfoPage.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.helper_methods import (
    custom_click,
    find_element,
    move_to_element,
    select_value_from_drop_down
)


class RewardInfoPage(BasePage):
    breadcrumb = (By.XPATH, "//div[@class='ant-breadcrumb']")
    reward_info_title = (By.XPATH, "//strong[text()='Reward Info']")
    name = (By.NAME, 'name_en')
    subtitle = (By.NAME, 'subtitle_en')
    description = (By.NAME, 'description_en')
    brands = (By.XPATH, "//div[text()='Please select your brands']")
    brand_label = (By.XPATH, "//label[@title='Brands']")
    tags = (By.XPATH, "//div[text()='Please select your tags']")
    categories = (By.XPATH, "//div[text()='Please select your categories']")
    labels = (By.XPATH, "//div[text()='Please select your labels']")
    catalogues = (By.XPATH, "//div[text()='Please select your catalogues']")
    next_button = (By.XPATH, "//button/span[text()='Next']")
    mandatory_error_message = (By.XPATH, "//div[text()='Rewards must have a name.']")

    @classmethod
    def select_reward_type(cls, reward_type):
        xpath = "//input[@value='{}']".format(reward_type.lower())
        return By.XPATH, xpath

    def _self_fill_inputs(self, attribute, input_data, field):
        if attribute in input_data:
            self.browser.find_element(*field).clear()
            self.browser.find_element(*field).send_keys(input_data[attribute])

    def _self_fill_tags(self, attribute, input_data, field):
        if attribute in input_data:
            element = self.browser.find_element(*field)
            move_to_element(self.browser, element)
            element.click()
            select_value_from_drop_down(self.browser, field, input_data[attribute])
            self.browser.find_element(*self.brand_label).click()

    def fill(self, input_data):
        """fill the form on the rewards info page"""
        if 'Type' in input_data:
            if input_data['Type'].lower() in ('public', 'private', 'system'):
                reward_type = self.select_reward_type(input_data['Type'])
                self.browser.find_element(*reward_type).click()
            else:
                raise Exception("Not a valid reward type ! ")
        for attribute, locator in [('Name', self.name), ('Subtitle', self.subtitle),
                                   ('Description', self.description)]:
            self._self_fill_inputs(attribute, input_data, locator)
        for attribute, locator in [('Brands', self.brands), ('Tags', self.tags),
                                   ('Catalogues', self.catalogues)]:
            self._self_fill_tags(attribute, input_data, locator)
        next_button = self.browser.find_element(*self.next_button)
        custom_click(self.browser, next_button)

    def check_error_message(self, input_data):
        """return the error message assertion status"""
        next_button = self.browser.find_element(*self.next_button)
        custom_click(self.browser, next_button)
        assertion = find_element(self.browser, self.mandatory_error_message)
        self.browser.find_element(*self.name).send_keys(input_data['Name'])
        custom_click(self.browser, next_button)
        return assertion

    def get_field_access_status(self, input_data):
        """return the field access assertion status"""
        field_status_dict = {}
        if 'Type' in input_data:
            if input_data['Type'].lower() in ('public', 'private', 'system'):
                reward_type = self.select_reward_type(input_data['Type'])
                self.browser.find_element(*reward_type).click()
            else:
                raise Exception("Not a valid reward type ! ")

        for attribute, locator in [('Brands', self.brands), ('Tags', self.tags),
                                   ('Catalogues', self.catalogues), ('Labels', self.labels),
                                   ('Categories', self.categories)]:
            if find_element(self.browser, locator):
                field_status_dict[attribute] = True
            else:
                field_status_dict[attribute] = False
        return field_status_dict
