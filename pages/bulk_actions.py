"""
This module contains BulkActionPage,
the page object for the BulkActionPage.
"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.helper_methods import (
    custom_click,
    ensure_no_error_message,
    find_element,
    get_file_name,
    read_table,
    select_value_from_drop_down,
    wait_for_element
)


class BulkActionsPage(BasePage):

    breadcrumb = (By.XPATH, '//span[contains(@class, "ant-breadcrumb-link")]')
    upload_button = (By.XPATH, '//i[@aria-label="icon: upload"]/following-sibling::span')
    upload_input = (By.XPATH, '//span/input')
    upload_button_in_modal = (By.XPATH, "//div[@class='ant-modal-footer']//span[text()='Upload']")
    list_table = (By.XPATH, "//table")
    action_drop_down = (By.XPATH, "//div[@role='combobox']")
    campaign_drop_down = (By.XPATH, "//div[text()='Please select a campaign']")

    @classmethod
    def upload_results(cls, file_name):
        xpath = "//span[@title='{}']".format(file_name)
        return By.XPATH, xpath

    @classmethod
    def select_value(cls, value):
        xpath = "//ui[@role='listbox'/li[text()='{}']]".format(value)
        return By.XPATH, xpath

    def on_bulk_action_page(self):
        """check on the bulk action page """
        return find_element(self.browser, self.bulk_actions)

    def open_upload_model(self):
        """open the upload widget"""
        wait_for_element(self.browser, self.upload_button)
        upload_button = self.browser.find_element(*self.upload_button)
        custom_click(self.browser, upload_button)

    def _select_action(self, action_dict):
        """select the action from upload widget"""
        self.browser.find_element(*self.action_drop_down).click()
        select_value_from_drop_down(self.browser, self.action_drop_down, action_dict['action'])
        if 'campaign' in action_dict:
            self.browser.find_element(*self.campaign_drop_down).click()
            select_value_from_drop_down(self.browser, action_dict['campaign'])

    def upload_file(self, file_path, action_dict=None):
        """upload file in upload widget"""
        bulk_action_panel = self.browser.find_element(*self.bulk_actions)
        bulk_action_panel.click()
        self.open_upload_model()
        if action_dict is not None:
            self._select_action(action_dict)
        upload_input = self.browser.find_element(*self.upload_input)
        self.browser.execute_script("arguments[0].style.display = 'block';", upload_input)
        upload_input.send_keys(file_path)
        file_name = get_file_name(file_path)
        upload_results = self.browser.find_element(*self.upload_results(file_name))
        upload_button_in_modal = self.browser.find_element(*self.upload_button_in_modal)
        if upload_results.text == file_name:
            print("File Present In Model")
        custom_click(self.browser, upload_button_in_modal)
        ensure_no_error_message(self.browser, self.error_message)

    def read_table(self, autorefresh=False):
        """read the whole table from list"""
        if autorefresh:
            self.browser.refresh()
            self.browser.find_element(*self.rewards).click() if not self.on_bulk_action_page() else None
        wait_for_element(self.browser, self.breadcrumb, 'Bulkaction')
        return read_table(self.browser, self.list_table)

    def get_permissions(self):
        """get permissions for bulk action functionality"""
        permission_list = {}
        try:
            bulk_action_panel = self.browser.find_element(*self.bulk_actions)
            bulk_action_panel.click()
            permission_list['create'] = True if find_element(self.browser, self.upload_button) else False
            permission_list['read'] = self.read_table()
            return permission_list
        except NoSuchElementException:
            return permission_list
