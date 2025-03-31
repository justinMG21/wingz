import time
from behave import *


@when('the user navigates to the my profile page')
def navigates_my_profile(context):
    context.web.profile.click_my_profile()

@then('the user should be redirected to the my_profile page')
def verify_url(context):
    actual_url = context.web.profile.in_profile_page()
    expected_url = context.test_data["profile_url"]
    assert actual_url == context.test_data["profile_url"], f"Expected URL {expected_url} but got {actual_url}"

@when('the user provide "{fname}" "{lname}" "{city}" "{bio}"')
def update_profile(context, fname, lname, city, bio):
    context.first_name = fname
    context.last_name = lname
    context.city = city
    context.bio = bio
    context.web.profile.input_field(context.first_name,context.last_name,context.city, context.bio)

@when('the user clicks save button')
def click_save(context):
    context.web.profile.click_save()

@then ('the user should be able to see the changes saved')
def verify_changes(context):
    is_saved = context.web.profile.is_saved()
    assert is_saved, "It is not saved"
    
    