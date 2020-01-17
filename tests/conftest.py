"""
This module contains shared fixtures for web UI tests.
"""

import json
import pytest
from selenium import webdriver


config_path = 'config.json'
default_wait_time = 10
supported_browsers = ['chrome', 'firefox']


@pytest.fixture(scope='session')
def config():
    """" Read the JSON config file and returns it as a parsed dict """
    with open(config_path) as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture(scope='session')
def config_browser(config):
    """ Validate and return the browser choice from the config data """
    if 'browser' not in config:
        raise Exception('The config file does not contain "browser"')
    elif config['browser'] not in supported_browsers:
        raise Exception('"{config["browser"]}" is not a supported browser')
    return config['browser']


@pytest.fixture(scope='session')
def config_url(config):
    """ Validate and return the base url from config data"""
    if 'url' not in config:
        raise Exception('The config file does not contain "url"')
    return config['url']


@pytest.fixture(scope='session')
def config_wait_time(config):
    """ Validate and return the wait time from the config data """
    return config['wait_time'] if 'wait_time' in config else default_wait_time


@pytest.fixture
def browser(config, config_url, config_browser, config_wait_time):
    """This Fixture method will start the Browser based on the configuration provided
    in json file"""
    try:
        kwargs = {}
        if 'binary' in config:
            binary = config['binary']
        if config['selenium_grid']:
            caps = {'browserName': config_browser}
            command_executor_url = "http://{}:4444/wd/hub".format(config['hub_host'])
            driver = webdriver.Remote(
                command_executor=command_executor_url,
                desired_capabilities=caps
            )
        else:
            if config_browser == 'chrome':
                if binary:
                    kwargs.update({'executable_path': binary})
                options = webdriver.ChromeOptions()
                options.add_argument('disable-web-security')
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                kwargs.update({'options': options})
                driver = webdriver.Chrome(**kwargs)
            elif config_browser == 'firefox':
                driver = webdriver.Firefox(**kwargs)
            else:
                raise Exception('"{config_browser}" is not a supported browser')

        # Wait implicitly for elements to be ready before attempting interactions
        driver.implicitly_wait(config_wait_time)
        driver.get(config_url)
        driver.maximize_window()

        # Return the driver object at the end of setup
        yield driver
    finally:
        # For cleanup, quit the driver
        driver.quit()
