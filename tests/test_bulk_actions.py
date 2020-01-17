"""
This module contains web test cases for bulk upload functionality
"""
import pytest
from utils.helper_methods import get_file_name, get_file_paths
from utils.exceptions import ErrorMessageException
from pages.login import LoginPage
from pages.bulk_actions import BulkActionsPage

valid_user = ('admin@dashboard.com', 'admin1234')
invalid_user = ('reward_admin@dashboard.com', 'reward_admin')
valid_files = get_file_paths(file_type='valid')
invalid_files = get_file_paths(file_type='invalid')
action_selector = [{'action': 'Issue Vouchers'},
                   {'action': 'Upload Transactions'},
                   {'action': 'Upload Users'},
                   {'action': 'Upload Tries', 'campaign': 'Stamp Campaign'}]


@pytest.fixture(params=valid_files)
def valid_file(request):
    return str(request.param)


@pytest.fixture(params=invalid_files)
def invalid_file(request):
    return str(request.param)


@pytest.fixture(params=action_selector)
def action(request):
    return request.param


def test_permissions_bulk_file_upload(browser):
    """"This test will verify permissions for bulk file upload and read details.
    We will be testing this for User has only BulkAction Permission
    """
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    bulk_actions_page = BulkActionsPage(browser)
    bulk_actions_page.is_logged_in(email)
    permissions = bulk_actions_page.get_permissions()
    assert permissions['create']
    assert len(permissions['read']) > 0


def test_permissions_bulk_file_upload_for_invalid_user(browser):
    """"This test will verify there will no permissions for bulk file upload and read details
    for an invalid user.
    """
    email, password = invalid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    bulk_actions_page = BulkActionsPage(browser)
    bulk_actions_page.is_logged_in(email)
    permissions = bulk_actions_page.get_permissions()
    assert len(permissions) == 0


def test_bulk_upload_valid_input_files(browser, valid_file, action):
    """"This test will verify that the bulk file upload is possible for all valid file
    formats and all Actions e.g. .txt, .csv, .xlsx and Status is Processed"""
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    bulk_actions_page = BulkActionsPage(browser)
    bulk_actions_page.is_logged_in(email)
    bulk_actions_page.upload_file(valid_file, action)
    table = bulk_actions_page.read_table()
    assert (action['action']).lower() in (table[0]['Action Name']).lower()
    assert table[0]['File Name'] == get_file_name(valid_file)
    assert table[0]['User'] == email
    assert table[0]['Status'] in ['PROCESSING', 'INITIAL']
    # TODO : Below code was to verify the uploaded document get processed.
    # table = bulk_actions_page.read_table(autorefresh=True)
    # assert table[0]['File Name'] == get_file_name(valid_file)
    # assert table[0]['Status'] == 'PROCESSED'


def test_bulk_upload_invalid_input_files(browser, invalid_file):
    """"This test will verify that the bulk file upload is not possible for invalid file
    formats e.g. .pdf, .gif, .zip ...
    """
    email, password = valid_user
    login_page = LoginPage(browser)
    login_page.login(email, password)
    bulk_actions_page = BulkActionsPage(browser)
    bulk_actions_page.is_logged_in(email)
    with pytest.raises(ErrorMessageException) as error_info:
        bulk_actions_page.upload_file(invalid_file)
    assert 'Error uploading file.' in str(error_info.value)

