from playwright.sync_api import sync_playwright, expect
import pytest
import os

BASE_URL = "https://www.saucedemo.com/"

#fixture scope是function讓每一個測試執行前都預先建立環境，減少重複的code
@pytest.fixture
def page():
    with sync_playwright() as p:
        headless  = os.getenv("CI") == "true"
        browser = p.chromium.launch(headless = headless)
        page = browser.new_page()
        page.goto(BASE_URL)

        try:
            yield page
        finally:
            browser.close()