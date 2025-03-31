import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from web.steps.base_step import BasePage

class LoginPage(BasePage):
    def __init__(self, driver, context):
        super().__init__(driver, context)
        self.learn_develop_url = None
        self.driver = driver
        self.context = context

        self.username_input_locator = (By.XPATH, '//*[@id="username"]')
        self.password_input_locator = (By.XPATH, '//*[@id="password"]')
        self.login_button_locator = (By.XPATH, '//button[contains(text(),"Sign In")]')

    def access_url(self, url):
        self.get_url(url)
        assert (self.element_display(self.username_input_locator)), (
            'User name field is not found. \n'
            'Expected is: success to login'
        )

    def wingz_login(self, username, password):
        self.element_display(self.username_input_locator)
        self.input(self.username_input_locator, username)
        self.element_display(self.password_input_locator)
        self.input(self.password_input_locator, password)
        self.click(self.login_button_locator)
