<!-- PROJECT Perx-webui-testing -->
 
<p align="center">  

 <h1 align="center">Perx-WebUI-Testing</h1>  
  
 <p align="center">  
 Perx-WebUI-Testing is a test suite which exercises the UI of Perx Loyalty System
    <br />  
 </a>  
 <br />
  ·  
    <a href="https://github.com/omkarkhatavkar/perx-webui-testing/tree/master/test_report.png">Test Reports</a>
           ·       
       <a href="https://github.com/omkarkhatavkar/perx-webui-testing/tree/master/tests">Tests</a>
  ·
    <a href="https://github.com/omkarkhatavkar/perx-webui-testing/issues">Request Feature</a>
 </p></p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Main Features](#main-features)
* [Requirements](#requirements)
  * [Prerequisites](#prerequisites)
* [Quick Start](#quick-start)
* [Running UI Tests On a Docker Browser](#running-ui-tests-on-a-docker-browser)
* [Testing With Pytest](#testing-with-pytest)



<!-- ABOUT THE PROJECT -->
## About The Project

Perx-WebUI-Testing is a test suite which exercises the UI for Perx Loyalty Management System. Currently, it contains the UI Automation tests, Test Reports for Perx Loyalty Management UI.

<!-- MAIN FEATUERES -->
#### Main Features

-   Tests are written in Python Language with pytest as underneath test framework.
-   Perx-WebUI-Testing uses the Page Object Model to make tests more compact.
-  Tests are run locally with firefox and chrome browser support.
-   It contains support for Selenium Grid and Tests can be run on the remote host. This needs configuration change.
-  It contains docker-compose file create same infra locally.

<!-- Requirements -->
## Requirements

You need Pip3 and Python 3.6  or later to run Perx-WebUI-Testing. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

### Prerequisites

In Ubuntu, Mint and Debian you can install Python 3 like this:
```
$ sudo apt-get install python3.6 python3-pip
```
For other Linux flavours, macOS and Windows, packages are available at

[http://www.python.org/getit/](http://www.python.org/getit/)

## Quick Start

 - Clone the git repo
```bash
git clone https://github.com/omkarkhatavkar/perx-webui-testing.git
cd perx-webui-testing
```
 - Create a Python Virtual Environment and Activate
```bash
virtualenv -p python3.6 env
source env/bin/activate
```
 - Install all dependencies
```bash
pip install --editable .
```
 - Download appropriate gecko driver from url  https://github.com/mozilla/geckodriver/releases moved it into '/usr/bin' path
 - Execute the Tests
```bash
pytest tests/ --html=report.html
```
##   Running UI Tests On a Docker Browser
It is possible to run UI tests within a docker container. To do this:

 -   Install docker. It is provided by the  `docker`  package on Fedora and Red Hat.
 -   Make sure that Docker is up and running and the user that will run perx-webui-testing has permission to run docker commands. For more information check the docker installation guide  [https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/)
 -   Set  `"selenium_grid": true` in the configuration file  `config.json`.

Once you’ve performed these steps, UI tests will no longer launch a web browser on your system. Instead, UI tests launch a web browser within a docker container and docker-compose file.

 - Clone the git repo
```bash
git clone https://github.com/omkarkhatavkar/perx-webui-testing.git
cd perx-webui-testing
```

 - Start the docker instances with Docker Compose File

```bash
[root@okhatavk # docker-compose up -d
Creating perx-webui-testing_hub_1 ... done
Creating perx-webui-testing_chrome_1  ... done
Creating perx-webui-testing_firefox_1 ... done
```

  - Execute the  tests
```bash
  pytest tests/ --html=report.html
  ```

  ## Testing With Pytest

  To run all tests:

    $ pytest

It is possible to run a specific subset of tests:

    $ pytest test_case.py
    $ pytest test_case.py::test_case_name

To get more verbose output, or run multiple tests:

    $ pytest tests/ -v
    $ pytest tests/test_web.py

To search in test case names, in this case, it will run just negative tests:

    $ pytest tests/test_web.py -k negative

For more information about Python’s  [pytest](https://docs.pytest.org/en/latest/contents.html)  module, read the documentation.


                                            PERX INTERVIEw ANSWER

  ## Testing authorization of user roles and groups

- Given a user acc with permissin to create a reward and ensure that the user is not able to visit the rest of the page sections (loyalties, campaigns, merchants, user lists, bulk actions) and all the other API endpoints shouldn't be accessible.

##### ANS ===> Verified with tests [test_access_api_endpoints_using_rewards_admin_valid_user, test_access_api_endpoints_using_ui_rewards_admin_authorized_user ]

## Creating a reward

- Ensure that a logged in user has sufficient permission to create a reward. 

##### ANS ==> Verified with test [test_permissions_for_rewards_valid_user]

- A non-authorized user should not have access to the reward detail/edit page if he tries to access directly from the URL.

##### ANS ==> Verified with test [test_permissions_for_rewards_non_authorized_user_ui_navigation, test_permissions_for_rewards_non_authorized_user_from_url]

- Clicking "+ Create New" button should lead to reward creation page

##### ANS ==> Verified with test [test_create_public_reward] 

- Reward form
  - A reward validity period should have both start and end dates.
  - A successful submission only happens when the payload contains all mandatory information.
  - It should not show up in the rewards listing.

##### ANS ==> Above is verified with tests [test_create_public_reward, test_check_mandatory_information_create_reward, test_successful_create_public_reward_with_search, ]

- Disabling a section should clear respective information from the form payload

##### ANS ==> Verified with test [test_disable_section_on_ui]

- If the reward is of private type,
  - All fields related to catalogues, labels, brands, tags and categories should disappaer.
  - It should not be tagged to any catalogues, labels, brands, tags nor categories.

##### ANS ==> Verified with test [test_access_level_for_fields_with_private_reward]

## Upload a file in bulk list

- Ensure that the logged in user has sufficient permission to visit the builk file upload page and has the ability to upload.

##### ANS ==> Verified with test [test_permissions_bulk_file_upload, test_permissions_bulk_file_upload_for_invalid_user]

- Form upload should only accept from the accepted file list (.txt, .xlsx, .csv).

##### ANS ==> Verified with test [test_bulk_upload_valid_input_files]
- Each file should be tied to one action.

##### ANS ==> Verified with test [test_bulk_upload_valid_input_files]

- After a successful upload, the file list should reflect the newly uploaded file

##### ANS ==> Verified with test [test_bulk_upload_invalid_input_files]
  
