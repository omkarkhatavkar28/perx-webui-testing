"""
This module contains web test cases for reward functionality
"""
from pages.login import LoginPage
from pages.rewards.reward import RewardPage
from pages.forbidden import ForbiddenPage
from fauxfactory import gen_string

invalid_user = ('omkar@mailinator.com', 'wireless28')
valid_user = ('reward_admin@dashboard.com', 'reward_admin')
input_data = {
    'Name': gen_string(str_type='alphanumeric'),
    'Subtitle': 'Testing Reward Creation',
    'Description': 'This is Public Reward',
    'Brands': 'Nike',
    'Tags': 'MY DIGI HOME HIGHLIGHTS',
    'Catalogues': 'Harmon Catalogue'
}


def test_permissions_for_rewards_valid_user(browser):
    """"This test will verify permissions for reward create, update, read permissions.
    This will be for tested for an valid user has reward role.
    """
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    permissions = reward_page.get_permissions()
    assert len(permissions) == 3
    for permission in permissions:
        assert permissions[permission]


def test_permissions_for_rewards_non_authorized_user_ui_navigation(browser):
    """"This test will verify non-authorized user do not have permissions for reward create,
    update, read permissions. This verification is done from UI navigation.
    """
    email, password = invalid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    permissions = reward_page.get_permissions()
    assert len(permissions) == 0


def test_permissions_for_rewards_non_authorized_user_from_url(browser):
    """"This test will verify non-authorized user do not have permissions for reward create,
    update, read permissions. This verification is done from API end_points.
    """
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    reward_id = reward_page.get_valid_reward_id()
    reward_page.log_out()
    email, password = invalid_user
    login_page.login(email, password)
    reward_page.is_logged_in(email)
    permissions = reward_page.get_permissions_using_url(reward_id)
    assert len(permissions) == 3
    for permission in permissions:
        assert not permissions[permission]
    forebidden_page = ForbiddenPage(browser)
    assert '403 Forbidden' in forebidden_page.get_page_header()


def test_access_api_endpoints_using_rewards_admin_valid_user(browser):
    """"This test will verify invalid user do not have permissions for reward create,
    update, read permissions. This verification is done from UI navigation.
    """
    end_points = ('/loyalties/list', '/campaigns/list', '/merchants/list', '/settings/users',
                  '/bulkaction')
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    status_dict = reward_page.get_api_end_point_status_with_url()
    assert len(status_dict) > 5
    for end_point in end_points:
        if end_point in status_dict:
            assert status_dict[end_point] == 'No Access'


def test_access_api_endpoints_using_ui_rewards_admin_authorized_user(browser):
    """"This test will verify invalid user do not have permissions for reward create,
    update, read permissions. This verification is done from UI navigation.
    """
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    status_dict = reward_page.get_left_panel_links()
    assert len(status_dict) > 5
    for key in status_dict:
        if 'rewards' in key:
            assert status_dict[key] == 'Access', "Failed For {}".format(key)
        else:
            assert status_dict[key] == 'No Access', "Failed For {}".format(key)


def test_create_public_reward(browser):
    """verifies creation of public reward with all mandatory information"""
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    input_data['Type'] = 'Public'
    input_data['Name'] = 'Public_Reward-{}'.format(input_data['Name'])
    reward_info = reward_page.create_reward(input_data)
    assert input_data['Name'] in reward_info
    assert 'Active' in reward_info
    assert input_data['Brands'] in reward_info


def test_check_mandatory_information_create_reward(browser):
    """verifies error message to create of public reward without filling all mandatory
    information"""
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    input_data['Type'] = 'Public'
    assertions = reward_page.check_mandatory_information(input_data)
    for assertion in assertions:
        assert assertion, "No Error Message displayed for mandatory information"


def test_successful_create_public_reward_with_search(browser):
    """Create Public Reward and Search that reward in Rewards List"""
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    input_data['Type'] = 'Public'
    input_data['Name'] = 'Public_Reward-{}'.format(input_data['Name'])
    reward_page.create_reward(input_data)
    reward_page.search_reward(input_data['Name'])
    table = reward_page.read_table()
    assert input_data['Name'] in table[0]["Name"]
    assert table[0]["Status"] == 'ACTIVE'


def test_access_level_for_fields_with_private_reward(browser):
    """This test will verify that all fields related to catalogues, labels, brands,
    tags and categories should disappear for private reward"""
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    del input_data['Catalogues']
    input_data['Type'] = 'Private'
    input_data['Name'] = 'Private_Reward-{}'.format(input_data['Name'])
    fields_visibility_status = reward_page.get_field_status(input_data)
    assert len(fields_visibility_status) > 3
    for field in ['Brands', 'Tags', 'Catalogues', 'Labels', 'Categories']:
        if field in fields_visibility_status:
            assert not fields_visibility_status[field], "Failed For {}".format(field)


def test_disable_section_on_ui(browser):
    """This is test will verify that disabling of sections in form reward payload"""
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    reward_page = RewardPage(browser)
    reward_page.is_logged_in(email)
    disable_status = reward_page.check_sections_after_disable_on_ui()
    assert disable_status, "Failed to disable the UI Section"
