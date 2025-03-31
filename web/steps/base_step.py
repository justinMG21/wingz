import inspect
import os
import random
import time
import logging
import datetime
import string
from logging import getLogger
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains, Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

class BaseLog:
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)

    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.level = logging.DEBUG

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


class BasePage(BaseLog):

    def __init__(self, driver, context):
        super().__init__()
        self.now = None
        self.platform_endpoint = None
        self.timestamp = None
        self.modified_email = None
        self.cookie_auth = None
        self.driver = driver
        self.threshold = 20
        self.quick_threshold = 5
        self.element_should_be_shown_threshold = 5
        self.element_should_not_be_shown_threshold = 5

    def get_url(self, url):
        self.driver.get(url)

    def find_locator(self, loc):
        return self.driver.find_element(*loc)

    def find_locators(self, loc):
        return self.driver.find_elements(*loc)

    def input(self, loc, value):
        # debug print(inspect.stack())
        # self.debug('str(inspect.stack()): ' + str(inspect.stack()))
        self.debug("The function which called this safe_input is: " + inspect.stack()[2].function)
        self.debug("The file which has the function above is: " + inspect.stack()[2].filename)
        self.debug("Trying to check if " + str(loc) + " is clickable and put the text, " + str(value) + " on it...")
        ret = self.element_clickable(loc)
        assert ret is True, (
            "Assertion failed: The target element, " + str(loc) + " was not clickable in the time threshold \n",
            "Expected is: self.element_clickable(loc) should be True. \n",
            "But the actual is: " + str(ret)
        )
        self.debug("Trying to put text in: " + str(loc))
        self.find_locator(loc).send_keys(value)

    def click(self, loc):
        function_name = inspect.stack()[1].function
        file_path = inspect.stack()[1].filename
        self.debug(f"The function name is {function_name} and the file path is {file_path}")
        self.debug(f"Trying to check if {loc} is clickable and click on it...")
        self.driver.find_element(*loc).click()

    def gets_cookie(self, cookie_name):
        self.driver.get_cookie(cookie_name)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def user_login(self, username_field, username, password_field, password, login_btn):
        self.input(username_field, Keys.BACKSPACE * 30)
        self.input(username_field, username)
        self.input(password_field, Keys.BACKSPACE * 20)
        self.input(password_field, password)
        self.click(login_btn)

    def new_tab(self):
        self.driver.switch_to.new_window('tab')

    def tab_close(self, original_window):
        self.driver.close()
        self.driver.switch_to.window(original_window)

    def clear_textbox(self, loc, keys_control, keys_delete):
        self.input(loc, keys_control)
        self.input(loc, keys_delete)

    def upload_file(self, loc, file_path):
        self.driver.find_element(*loc).send_keys(file_path)

    def add_timestamp(self, email):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.modified_email = f"{email.split('@')[0]}_{self.timestamp}@{email.split('@')[1]}"
        return self.modified_email

    def element_display(self, loc):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                EC.visibility_of_element_located(loc)
            )
        except TimeoutException:
            self.debug("Fell into timeout in element_display()")
            return False
        return True

    def quick_element_display(self, loc):
        try:
            WebDriverWait(self.driver, self.quick_threshold).until(
                EC.visibility_of_element_located(loc)
            )
        except TimeoutException:
            self.debug("Fell into timeout in quick_element_display()")
            return False
        return True

    def wait_element_in_dom(self, loc):
        # wait until element is visible in dom without returning boolean
        return WebDriverWait(self.driver, self.threshold).until(
            EC.presence_of_element_located(loc)
        )

    def all_elements_display(self, locator):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                EC.visibility_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.debug("Fell into timeout in all_elements_display()")
            return False
        return True

    def element_invisibility(self, loc):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                EC.invisibility_of_element_located(loc)
            )
        except TimeoutException:
            self.debug("Fell into timeout in element_invisibility()")
            # sys.exit(1)

    def element_clickable(self, loc):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                EC.element_to_be_clickable(loc)
            )
            return True
        except TimeoutException:
            self.debug("Fell into timeout in element_clickable()")
            return False

    def url_fluent_wait(self, target_element):
        self.debug(target_element)
        for i in range(self.threshold):
            time.sleep(1)
            self.debug("str(self.driver.current_url): " + str(self.driver.current_url))
            self.debug('Fluent Loop Count: ' + str(i))
            if target_element in self.driver.current_url:
                return True
            elif i >= self.threshold - 1:
                self.debug("Fell into timeout in url_fluent_wait()")
                return False

    def alert_display(self):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                expected_conditions.alert_is_present()
            )
            return True
        except TimeoutException:
            self.debug("Fell into timeout in alert_display()")
            return False

    def page_load_waiter(self):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                EC.presence_of_element_located
            )
            return True
        except TimeoutException:
            self.debug("Fell into timeout in wait_page_read()")
            return False

    @staticmethod
    def get_endpoint(endpoint, url):
        try:
            platform_endpoint = os.environ[endpoint]
        except KeyError:
            platform_endpoint = url

        return platform_endpoint

    # open new blank tab
    def open_blank_tab(self):
        self.driver.execute_script("window.open('about:blank', '_blank');")

    # switch to another tab
    def switch_to(self, frame):
        self.driver.switch_to.frame(frame)

    # wait and switch to another tab
    def fluent_switch_window(self, original_window):
        self.page_load_waiter()
        try:
            WebDriverWait(self.driver, self.element_should_not_be_shown_threshold).until(
                EC.number_of_windows_to_be(2)
            )
        except TimeoutException:
            self.debug("New tab was not open in the time threshold.")
            return False
        # Loop through until a new window handle is found
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.debug("A new window(tab) was found and got the handler.")
                self.driver.switch_to.window(window_handle)
                return True
        self.debug("Unknown tab was found.")
        return False

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    def get_time(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def mouse_hover(self, loc):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(*loc)).perform()

    def fluent_assertion(self, loc, expected_value):
        self.debug('expected_value: ' + expected_value)
        self.debug("str(expected_value.encode('utf-8')): " + str(expected_value.encode('utf-8')))
        for i in range(self.threshold):
            time.sleep(1)
            self.debug('Fluent loop count: ' + str(i))
            if expected_value in self.driver.find_element(*loc).text:
                return True
            elif i == self.threshold-1:
                self.debug("str(self.driver.find_element(*loc).text.encode('utf-8') is: " +
                           str(self.driver.find_element(*loc).text.encode('utf-8')))
                assert self.driver.find_element(*loc).text == expected_value, (
                    "Assertion failed: \n"
                    "Expected value is: " + expected_value + '\n'
                    "But the actual is: " + self.driver.find_element(*loc).text
                )
                # sys.exit(1)
            else:
                self.debug("self.driver.find_element(*loc).text is: " + self.driver.find_element(*loc).text)
                self.debug("str(self.driver.find_element(*loc).text.encode('utf-8') is: " +
                           str(self.driver.find_element(*loc).text.encode('utf-8')))

    def assert_element_not_exists(self, loc):
        try:
            WebDriverWait(self.driver, self.element_should_not_be_shown_threshold).until(
                EC.visibility_of_element_located(loc)
            )
        except TimeoutException:
            self.debug("Target element hasn't been shown as expected.")
            return True
        self.debug("Target element is still existing.")
        return False

    def assert_element_exists(self, loc):
        try:
            WebDriverWait(self.driver, self.element_should_be_shown_threshold).until(
                EC.visibility_of_element_located(loc)
            )
        except NoSuchElementException:
            self.debug("Target element isn't existing.")
            return False
        self.debug("Target element has been shown as expected.")
        return True

    def scroll_down(self, target):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)

    def select_random_value(self, locator):
        self.all_elements_display(locator)
        values = self.driver.find_elements(*locator)
        random.choice(values).click()

    def force_click(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)

    def mouse_down(self, locator):
        element = self.driver.find_element(*locator)
        actions = ActionChains(self.driver)
        actions.click_and_hold(element).perform()

    def generate_random_value(self, length=8):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def generate_random_letters_and_digit(self, length=8):
        characters = string.ascii_lowercase + string.digits
        result_str = ''.join(random.choice(characters) for _ in range(length))
        return result_str

    def generate_email(self):
        email = self.generate_random_value().lower() + "@mailnator.com"
        return email

    def generate_random_number(self):
        characters_string = '01234567789'
        result = ''.join((random.choice(characters_string)) for x in range(9))
        return result

    def get_all_list(self, locator):
        list_name = []
        list_name.clear()
        elements = self.find_locators(locator)
        for individual_elements in elements:
            list_name.append(str(individual_elements.text))
        return list_name

    def scroll_to(self, location):
        match location:
            case 'top':
                self.driver.execute_script("window.scrollTo(0, 0);")
            case 'bottom':
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            case _:
                self.debug("Location unspecified")

    @staticmethod
    def generate_datetime():
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        return f"{date_str} {time_str}"

    def scroll_into_view(self, loc):
        element = self.driver.find_element(*loc)
        element_position = element.location['y']
        viewport_height = self.driver.execute_script("return window.innerHeight")
        scroll_distance = element_position - (viewport_height / 2)

        self.driver.execute_script(f"""
               window.scrollBy(0, {scroll_distance});
               arguments[0].scrollIntoView({{
                   behavior: 'smooth',
                   block: 'center'
               }});
           """, element)
        time.sleep(1) # I need this for it not to fail
        WebDriverWait(self.driver, 4).until(EC.visibility_of(element))

    def staleness_of(self, loc):
        try:
            WebDriverWait(self.driver, self.threshold).until(
                EC.staleness_of(self.find_locator(loc))
            )
        except TimeoutException:
            self.debug("Fell into timeout in staleness_of()")
            return False
        return True

    def select_random_membership_number(self, membership_numbers):
        numbers = membership_numbers["membership_numbers"]
        random_membership_num = numbers[random.randint(0,len(numbers))]
        print(f"The random number is: {random_membership_num}")
        return random_membership_num


