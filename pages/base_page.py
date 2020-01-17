"""
This module contains BasePage,
the page object for the BasePage.
"""
from selenium.webdriver.common.by import By

from pages.forbidden import ForbiddenPage
from utils.helper_methods import (
    custom_click,
    ensure_page_safe,
    find_element,
    get_config,
    read_table,
    wait_for_element,
    wait_for
)


class BasePage:

    perx_logo = (By.XPATH, "//img[@alt='Perx Logo']")
    expand_left_panel = (By.XPATH, "//div[@class='ant-layout-sider-trigger']/i")
    logged_user = (By.XPATH, "//div[@class='ant-layout-sider-children']//strong")
    reports = (By.XPATH, "//li[@data-key='reports']")
    rewards = (By.XPATH, "//li[@data-key='rewards']")
    catalogs = (By.XPATH, "//li[@data-key='catalogs']")
    campaigns = (By.XPATH, "//li[@data-key='campaigns']")
    loyalties = (By.XPATH, "//li[@data-key='loyalties']")
    merchants = (By.XPATH, "//li[@data-key='merchants']")
    customer_management = (By.XPATH, "//li[@data-key='customer_management']")
    bulk_actions = (By.XPATH, "//li[@data-key='bulk_actions']")
    settings = (By.XPATH, "//li[@data-key='settings']")
    business_intelligence = (By.XPATH, "//li[@data-key='business_intelligence']")
    logout = (By.XPATH, "//span[text()='Logout']")
    error_message = (By.XPATH, "//i[@class='anticon anticon-close-circle']/following-sibling::span")
    success_message = (By.XPATH, "//i[@class='anticon anticon-check-circle']/following-sibling::span")
    list_table = (By.XPATH, "//table")
    urls_enpoints = ('/reports/downloads', '/reports/scheduled', '/rewards/list',
                     '/catalogues/list', '/campaigns/list', '/loyalties/list', '/rules/list',
                     '/merchants/list', '/customers/list', '/bulkaction', '/settings/users',
                     '/business_intelligence/overview')

    def __init__(self, browser):
        self.browser = browser

    def is_logged_in(self, email):
        """check if user is already logged in"""
        wait_for_element(self.browser, self.expand_left_panel)
        expand_panel = self.browser.find_element(*self.expand_left_panel)
        custom_click(self.browser, expand_panel)
        wait_for(lambda: len(self.browser.find_element(*self.logged_user).text) > 0, delay=1, num_sec=5)
        user_logged_in = self.browser.find_element(*self.logged_user).text
        if user_logged_in == email:
            return True
        else:
            raise Exception('Failed to login by user => {}'.format(email))

    def log_out(self):
        """logout from system"""
        self.logout = (By.XPATH, "//span[text()='Logout']")
        logout_link = self.browser.find_element(*self.logout)
        custom_click(self.browser, logout_link)

    def get_api_end_point_status_with_url(self):
        """return the status list by hitting the multiple web-points on the browser"""
        status_list = {}
        config = get_config()
        base_url = config['url']
        for end_point in self.urls_enpoints:
            self.browser.get(base_url + '/p' + end_point)
            ensure_page_safe(self.browser)
            forbidden_page = ForbiddenPage(self.browser)
            if find_element(self.browser, forbidden_page.header):
                status_list[end_point] = 'No Access'
            else:
                if find_element(self.browser, self.list_table):
                    if len(read_table(self.browser, self.list_table)) == 0:
                        status_list[end_point] = 'No Access'
                    else:
                        status_list[end_point] = 'Access'
                else:
                    status_list[end_point] = 'Access'
        return status_list

    def get_left_panel_links(self):
        """return the list containing 'Access' or 'No Access' for the links from left panel"""
        status_list = {}
        link_list = (self.reports, self.rewards, self.catalogs, self.campaigns, self.loyalties,
                     self.merchants, self.customer_management, self.bulk_actions, self.settings,
                     self.business_intelligence)
        for link in link_list:
            if find_element(self.browser, link):
                status_list[link[1]] = 'Access'
            else:
                status_list[link[1]] = 'No Access'
        return status_list
