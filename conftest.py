import os
import pytest
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

APPS_PATH = f"{os.path.expanduser('~')}/Downloads/apps"

# APPIUM settings
APPIUM_PORT = 4723
APPIUM_HOST = "127.0.0.1"


@pytest.fixture(autouse=True)
def appium_service():
    service = AppiumService()
    service.start(
        args=["--address", APPIUM_HOST, "-p", str(APPIUM_PORT)],
        timeout_ms=20000,
    )
    yield service
    service.stop()


@pytest.fixture(autouse=True)
def driver():
    driver = create_android_driver()
    yield driver
    driver.quit()


def create_android_driver():
    options = UiAutomator2Options()
    caps = {
        "platformName": "Android",
        "appium:options": {
            "automationName": "UIAutomator2",
            "app": f"{APPS_PATH}/ApiDemos-debug.apk",
        },
    }
    options.load_capabilities(caps)

    return webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}", options=options)


def create_ios_driver():
    options = XCUITestOptions()
    caps = {
        "platformName": "iOS",
        "appium:options": {
            "automationName": "XCUITest",
            "app": f"{APPS_PATH}/TestApp.app",
        },
    }
    options.load_capabilities(caps)

    return webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}", options=options)
