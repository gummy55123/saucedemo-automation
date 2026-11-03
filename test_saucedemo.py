from playwright.sync_api import sync_playwright, expect
import pytest
import os

BASE_URL = "https://www.saucedemo.com/"

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





def login(page,username,password): #填入帳號密碼，按登入按鈕
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()



products = {
    "Backpack": "#add-to-cart-sauce-labs-backpack",
    "Bike Light": "#add-to-cart-sauce-labs-bike-light",
    "Bolt T-Shirt": "#add-to-cart-sauce-labs-bolt-t-shirt",
    "Fleece Jacket": "#add-to-cart-sauce-labs-fleece-jacket"
}
@pytest.mark.parametrize("goods_name,cart_count",[
    ("Backpack","1"),
    ("Bike Light","1"),
    ("Bolt T-Shirt","1"),
    ("Fleece Jacket","1")
])
def test_parametrize_cart(page,goods_name,cart_count):
    login(page,"standard_user","secret_sauce")
    page.locator(products[goods_name]).click()
    expect(page.locator(".shopping_cart_badge")).to_have_text(cart_count)
    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(page.locator(".inventory_item_name:has-text('"+ goods_name + "')")).to_have_text("Sauce Labs" +" " + goods_name)

# def test_cart (page): #測試購物車功能
#     login(page,"standard_user","secret_sauce")
#     page.locator("#add-to-cart-sauce-labs-backpack").click()
#     expect(page.locator(".shopping_cart_badge")).to_have_text("1",timeout=3000)
#     page.locator("#add-to-cart-sauce-labs-bike-light").click()
#     expect(page.locator(".shopping_cart_badge")).to_have_text("2",timeout=3000)
#     page.locator("#remove-sauce-labs-backpack").click()
#     expect(page.locator(".shopping_cart_badge")).to_have_text("1",timeout=5000)
#     page.locator(".shopping_cart_link").click()
#     expect(page).to_have_url("https://www.saucedemo.com/cart.html")
#     expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Bike Light")
#     expect(page.locator(".inventory_item_name:has-text('Sauce Labs Backpack')")).to_have_count(0)




# @pytest.mark.parametrize("username,password,expect_result,expect_message",[
#     ("standard_user","secret_sauce","success",""),
#     ("wrong_user","wrong_password","failure","Epic sadface: Username and password do not match any user in this service"),
#     ("standard_user","wrong_password","failure","Epic sadface: Username and password do not match any user in this service"),
#     ("","secret_sauce","failure","Epic sadface: Username is required"),
#     ("standard_user","","failure","Epic sadface: Password is required"),
#     ("locked_out_user","secret_sauce","failure","Epic sadface: Sorry, this user has been locked out.")
# ])
# def test_login_case(page,username,password,expect_result,expect_message): #從上面取得參數測試不同帳號密碼組合的結果
#     login(page,username,password)
#     if expect_result == "success":
#         expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
#         expect(page.locator(".title")).to_have_text("Products",timeout=8000)
#         expect(page.locator(".shopping_cart_link")).to_be_visible(timeout=5000)
#     else:
#         expect(page.locator("[data-test='error']")).to_have_text(expect_message)
#         expect(page).to_have_url("https://www.saucedemo.com/")
#         expect(page.locator(".title")).not_to_be_visible()



# def test_login(page):
#     login(page,"standard_user","secret_sauce")
#     expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
#     expect(page.locator(".title")).to_have_text("Products")

    
# def test_wrong_user(page):
#     login(page,"wrong_user","wrong_password")
#     expect(page.locator("[data-test='error']")).to_have_text("Epic sadface: Username and password do not match any user in this service")


    