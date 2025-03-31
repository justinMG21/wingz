from behave import *
import time

@given('the user login to wingz using "{username}"')
def login(context, username):
    context.web.login.access_url(context.test_data["wingz_url"])
    context.web.login.wingz_login(username,context.test_data["password"])

@when('the user navigates to the account page')
def navigates_account(context):
    context.web.profile.click_account()