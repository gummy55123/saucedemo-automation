from playwright.sync_api import sync_playwright, expect
import pytest

BASE_URL = "https://www.saucedemo.com/"

#
def login(page,username,password): 
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()

        
# 使用 pytest.mark.xfail 標記預期會失敗的測試
# reason：說明預期失敗的原因
# strict=True：如果測試意外通過（XPASS），pytest 會將它判定為失敗
# @pytest.mark.xfail(    
#     reason="登入後無法穩定進入商品頁面",
#     strict=True
#     )
# def test_xfail_login_demo(page):
#     page.fill("#user-name", "standard_user")
#     page.fill("#password", "secret_sauce")
#     page.click("#login-button")

#     assert page.url == "https://www.saucedemo.com/inventory.html"





# 使用 pytest.mark.parametrize 將多組帳號密碼資料帶入同一個測試函式
# 根據不同測試資料，驗證登入成功或失敗的結果
@pytest.mark.parametrize("username,password,expect_result,expect_message",[
    ("standard_user","secret_sauce","success",""),
    ("wrong_user","wrong_password","failure","Epic sadface: Username and password do not match any user in this service"),
    ("standard_user","wrong_password","failure","Epic sadface: Username and password do not match any user in this service"),
    ("","secret_sauce","failure","Epic sadface: Username is required"),
    ("standard_user","","failure","Epic sadface: Password is required"),
    ("locked_out_user","secret_sauce","failure","Epic sadface: Sorry, this user has been locked out.")    
])
def test_login_case(page,username,password,expect_result,expect_message): 
    login(page,username,password)
    if expect_result == "success":
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(page.locator(".title")).to_have_text("Products",timeout=8000)
        expect(page.locator(".shopping_cart_link")).to_be_visible(timeout=5000)
    else:
        expect(page.locator("[data-test='error']")).to_have_text(expect_message)
        expect(page).to_have_url("https://www.saucedemo.com/")
        expect(page.locator(".title")).not_to_be_visible()




def test_cart (page): #測試購物車功能
    login(page,"standard_user","secret_sauce")
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1",timeout=3000)
    page.locator("#add-to-cart-sauce-labs-bike-light").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("2",timeout=3000)
    page.locator("#remove-sauce-labs-backpack").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1",timeout=5000)
    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Bike Light")
    expect(page.locator(".inventory_item_name:has-text('Sauce Labs Backpack')")).to_have_count(0)





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





# 使用 pytest.raises() 驗證函式是否拋出預期的 ValueError
def validate_login(username, password):
    if username == "" or password == "":
        raise ValueError("帳號密碼不能為空")
    elif len(password) < 6:
        raise ValueError("密碼長度少於6字元")

    return True

def test_empty_username():
    with pytest.raises(ValueError):
        validate_login("","secret_sauce")

def test_empty_password():
    with pytest.raises(ValueError):
        validate_login("standard_user","")

def test_password_too_short():
    with pytest.raises(ValueError):
        validate_login("standard_user","passw")  