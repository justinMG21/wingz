from web.steps.base_step import BasePage
from web.pages.wingz_login_page import LoginPage
from web.pages.wingz_profile_page import ProfilePage

class WebApplication:

    def __init__(self, driver, context):
        self.base_page = BasePage(driver, context)
        self.login = LoginPage(driver, context)
        self.profile = ProfilePage(driver, context)
        
        