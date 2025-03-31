import time
import os
from selenium import webdriver
from web.web_application import WebApplication
from web.config_loader import load_all_configs


def before_scenario(context, scenario):
    configs = load_all_configs()
    try:
        browser = os.environ.get("BROWSER", "Chrome")
    except KeyError:
        print('KeyError Happened. The test seemed to be executed on local environment.')
        browser = 'Chrome'

    running_in_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'

    if browser == 'Chrome':
        options = webdriver.ChromeOptions()
        if running_in_github_actions:
            options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        context.driver = webdriver.Chrome(options=options)
    elif browser == 'Edge':
        options = webdriver.EdgeOptions()
        if running_in_github_actions:
            options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        context.driver = webdriver.Edge(options=options)
    context.driver.set_window_size(1920, 1080)
    context.driver.maximize_window()
    context.test_data = configs["test_data"]
    context.config_e2e = configs["config_e2e"]
    context.web = WebApplication(context.driver, context)
    context.driver.implicitly_wait(5)  # seconds

def after_scenario(context, scenario):
    try:
        # Save a screenshot if the driver is still active
        screenshot_path = os.path.join(
            "e2e_test_automation",
            f"screenshot_{time.strftime('%y-%m-%d_%H%M%S')}.png"
        )
        if context.driver and context.driver.session_id:
            context.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        # Log the exception if screenshot saving fails
        print(f"Failed to take screenshot: {e}")
    finally:
        try:
            if context.driver:
                context.driver.quit()
        except Exception as e:
            print(f"Failed to close the driver: {e}")
        time.sleep(1)  # Optional delay for stability


