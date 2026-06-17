"""
Bộ test tự động Selenium cho website SauceDemo (https://www.saucedemo.com)
3 test case: Đăng nhập, Thêm sản phẩm vào giỏ hàng, Đăng xuất
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


class SauceDemoTests(unittest.TestCase):

    def setUp(self):
        # Dùng Chrome vì Firefox bản Snap trên Ubuntu không tương thích tốt với Selenium
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self):
        """Hàm dùng chung: thực hiện đăng nhập trước mỗi test cần đăng nhập"""
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "user-name").send_keys(USERNAME)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(EC.url_contains("inventory.html"))

    def test_01_login_success(self):
        """Test case 1: Đăng nhập thành công với tài khoản hợp lệ"""
        self.login()
        self.assertIn("inventory.html", self.driver.current_url)
        print("Test 1 PASS: Đăng nhập thành công, đã chuyển tới trang inventory")
        time.sleep(5)  # Giữ trình duyệt mở 5 giây để kịp chụp ảnh

    def test_02_add_to_cart(self):
        """Test case 2: Thêm một sản phẩm vào giỏ hàng và kiểm tra số lượng"""
        self.login()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        cart_badge = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        self.assertEqual(cart_badge.text, "1")
        print("Test 2 PASS: Đã thêm 1 sản phẩm, badge giỏ hàng hiển thị số 1")
        time.sleep(5)  # Giữ trình duyệt mở 5 giây để kịp chụp ảnh

    def test_03_logout(self):
        """Test case 3: Đăng xuất khỏi hệ thống, quay lại trang đăng nhập"""
        self.login()

        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        logout_link = self.wait.until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_link.click()

        self.wait.until(EC.url_to_be(BASE_URL))
        self.assertEqual(self.driver.current_url, BASE_URL)
        print("Test 3 PASS: Đăng xuất thành công, quay về trang login")
        time.sleep(5)  # Giữ trình duyệt mở 5 giây để kịp chụp ảnh


if __name__ == "__main__":
    unittest.main(verbosity=2)
