import time
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from web.steps.base_step import BasePage

class ProfilePage(BasePage):
    def __init__(self, driver, context):
        super().__init__(driver, context)
        self.learn_develop_url = None
        self.driver = driver
        self.context = context

        self.account_menu = (By.XPATH, '//a[@href="/account"]')
        self.my_profile= (By.XPATH, '//a[@href="/account/profile"]')
        self.first_name = (By.XPATH, '//input[@name="firstName"]')
        self.last_name = (By.XPATH, '//input[@name="lastName"]')
        self.home_city = (By.XPATH, '//input[@placeholder="Home city"]')
        self.bio = (By.XPATH, '//textarea[@name="bio"]')
        self.save = (By.XPATH, '//button[@type="submit"]')
        self.saved = (By.XPATH, '//button[text()="Saved !"]')

    def click_account(self):
        self.element_display(self.account_menu)
        self.click(self.account_menu)

    def click_my_profile(self):
        self.element_display(self.my_profile)
        self.click(self.my_profile)

    def in_profile_page(self):
        page_url = self.driver.current_url
        return page_url

    def input_field(self, fname, lname, city, bio):
        self.input(self.first_name, Keys.BACKSPACE * 20)
        self.input(self.first_name, fname)
        self.input(self.last_name, Keys.BACKSPACE * 20)
        self.input(self.last_name, lname)
        self.input(self.home_city, Keys.BACKSPACE * 20)
        self.input(self.home_city, city)
        self.input(self.bio, Keys.BACKSPACE * 20)
        self.input(self.bio, bio)

    def click_save(self):
        self.element_display(self.save)
        self.click(self.save)

    def is_saved(self):
        if self.element_display(self.saved):
            return True
        else:
            raise Exception("Not Saved")


