"""
This module contains LoginPage,
the page object for the LoginPage.
"""

from selenium.webdriver.common.by import By


class LoginPage:

    email = (By.NAME, 'email')
    password = (By.NAME, 'password')
    login_button = (By.XPATH, "//button[@type='submit']")

    def __init__(self, browser):
        self.browser = browser

    def set_email(self, email):
        email_element = self.browser.find_element(*self.email)
        email_element.clear()
        email_element.send_keys(email)

    def set_password(self, password):
        password_element = self.browser.find_element(*self.password)
        password_element.clear()
        password_element.send_keys(password)

    def click_login_btn(self):
        login_button = self.browser.find_element(*self.login_button)
        login_button.click()

    def login(self, email, password):
        self.set_email(email)
        self.set_password(password)
        self.click_login_btn()
