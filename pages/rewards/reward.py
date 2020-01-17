"""
This module contains RewardPage,
the page object for the RewardPage.
"""
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.rewards.rewards_details import RewardDetailsPage
from pages.rewards.rewards_info import RewardInfoPage
from pages.rewards.rewards_mechanics import RewardMechanicsPage
from pages.rewards.rewards_review import RewardReviewPage
from utils.helper_methods import (
    custom_click,
    ensure_no_error_message,
    ensure_page_safe,
    find_element,
    get_config,
    move_to_element,
    read_table,
    wait_for,
    wait_for_element_displayed
)


class RewardPage(BasePage):

    breadcrumb = (By.XPATH, "//div[@class='ant-breadcrumb']")
    reward_title = (By.XPATH, '//strong[contains(text, Rewards)]')
    create_new = (By.XPATH, '//button[contains(text, create)]')
    edit_button = (By.XPATH, '//button[contains(text, Edit)]')
    reward_search = (By.XPATH, "//input[contains(@placeholder, 'Find a reward')]")
    list_table = (By.XPATH, "//table")
    name_column = (By.XPATH, "//div[@class='ant-table-column-sorters']/span[text()='Name']")
    switcher_button = (By.XPATH, "//button[@role='switch']")
    upload_file_button = (By.XPATH, "//button/span[text()='Upload a File']")
    create_merchant = (By.XPATH, "//span[@class='ant-radio-button']")
    add_selling_price = (By.XPATH, "//button[text()='Add Selling Price']")

    def on_reward_page(self):
        """check if are already on rewards page"""
        return find_element(self.browser, self.rewards)

    def read_table(self, autorefresh=False):
        """return the list of dict which contains key => column_name and value => row_value"""
        if autorefresh:
            self.browser.refresh()
        self.browser.find_element(*self.rewards).click() if not self.on_reward_page() else None
        read_table(self.browser, self.list_table, row_number=1)
        return read_table(self.browser, self.list_table)

    def get_first_row_from_table(self, autorefresh=False):
        """return the first row from the table"""
        if autorefresh:
            self.browser.refresh()
        self.browser.find_element(*self.rewards).click() if not self.on_reward_page() else None
        return read_table(self.browser, self.list_table, row_number=1)

    def _navigate_to_edit_page(self, element):
        """navigate to edit page"""
        name_element = element[0]['Name']
        name_element.find_element(By.TAG_NAME, 'a').click()
        wait_for_element_displayed(self.browser.find_element(*self.edit_button))

    def navigate_to_reward_create_page(self):
        """navigate to reward create page"""
        self.browser.find_element(*self.rewards).click() if not self.on_reward_page() else None
        wait_for(lambda: len(self.read_table()) > 0, delay=1, num_sec=5)
        self.browser.find_element(*self.create_new).click()

    def create_reward(self, input_data):
        """create reward and return the result"""
        self.navigate_to_reward_create_page()
        rewards_info_page = RewardInfoPage(self.browser)
        rewards_info_page.fill(input_data)
        rewards_mechanics_page = RewardMechanicsPage(self.browser)
        rewards_mechanics_page.fill(input_data)
        rewards_review_page = RewardReviewPage(self.browser)
        rewards_review_page.launch_reward()
        ensure_no_error_message(self.browser, self.error_message)
        rewards_detail_page = RewardDetailsPage(self.browser)
        return rewards_detail_page.read_widget(widget_name='reward_info')

    def check_mandatory_information(self, input_data):
        """check mandatory information messages and return their status"""
        assertions = []
        self.navigate_to_reward_create_page()
        rewards_info_page = RewardInfoPage(self.browser)
        assertion = rewards_info_page.check_error_message(input_data)
        assertions.append(assertion)
        rewards_mechanics_page = RewardMechanicsPage(self.browser)
        assertion = rewards_mechanics_page.check_error_message()
        assertions.append(assertion)
        return assertions

    def get_field_status(self, input_data):
        """return the filed status for private reward"""
        self.navigate_to_reward_create_page()
        rewards_info_page = RewardInfoPage(self.browser)
        return rewards_info_page.get_field_access_status(input_data)

    def search_reward(self, data):
        """search the reward in search box"""
        self.browser.find_element(*self.rewards).click()
        wait_for(lambda: len(self.read_table()) > 0, delay=1, num_sec=5)
        self.browser.find_element(*self.reward_search).send_keys(data)
        ensure_no_error_message(self.browser, self.error_message)

    def check_sections_after_disable_on_ui(self):
        """check that sections are disable correctly and return the result"""
        self.navigate_to_reward_create_page()
        elements = self.browser.find_elements(*self.switcher_button)
        for element in elements:
            move_to_element(self.browser, element)
            custom_click(self.browser, element)
        for locator in (self.upload_file_button, self.create_merchant, self.add_selling_price):
            if find_element(self.browser, locator):
                return False
            else:
                return True

    def get_permissions(self):
        """return the permissions for the create, read and update reward"""
        permission_list = {}
        try:
            rewards_panel = self.browser.find_element(*self.rewards)
            rewards_panel.click()
            wait_for_element_displayed(self.browser.find_element(*self.list_table))
            wait_for(lambda: len(self.read_table()) > 0, delay=1, num_sec=5)
            table = self.read_table()
            if len(table) > 0:
                permission_list['read'] = True
            else:
                permission_list['read'] = False
            permission_list['create'] = True if find_element(self.browser, self.create_new) else False
            element = self.get_first_row_from_table()
            self._navigate_to_edit_page(element)
            permission_list['update'] = True if find_element(self.browser, self.edit_button) else False
            return permission_list
        except NoSuchElementException:
            return permission_list

    def get_valid_reward_id(self):
        wait_for_element_displayed(self.browser.find_element(*self.list_table))
        wait_for(lambda: len(self.read_table()) > 0, delay=1, num_sec=5)
        first_row = self.get_first_row_from_table()
        pattern = re.compile('ID: (.*.+?)')
        ids = pattern.findall(first_row[0]['Name'].text)
        return ids[0]

    def get_permissions_using_url(self, reward_id):
        """return the access level status for by calling the urls end point for reward"""
        permission_list = {}
        try:
            config = get_config()
            reward_list_url = config['url'] + '/p/rewards/list'
            self.browser.get(reward_list_url)
            ensure_page_safe(self.browser)
            permission_list['read'] = False
            if find_element(self.browser, self.list_table):
                table = self.read_table()
                if len(table) > 0:
                    permission_list['read'] = True

            permission_list['create'] = True if find_element(self.browser, self.create_new) else False
            reward_create_url = config['url'] + '/p/rewards/create'
            self.browser.get(reward_create_url)
            ensure_page_safe(self.browser)
            permission_list['create'] = True if find_element(self.browser, self.create_new) else False

            reward_resource_url = config['url'] + '/p/rewards/show/{}'.format(reward_id)
            self.browser.get(reward_resource_url)
            ensure_page_safe(self.browser)
            permission_list['update'] = True if find_element(self.browser, self.edit_button) else False
            return permission_list
        except NoSuchElementException:
            return permission_list
