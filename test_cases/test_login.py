# -*- coding: utf-8 -*-
"""
登录功能自动化测试（Page Object 重构版）

将页面元素和操作封装到 pages/ 目录下的页面类中，
测试用例只关注业务逻辑，不直接操作 DOM。

运行方式：
    pytest test_cases/test_login.py -v
    pytest test_cases/test_login.py --html=reports/report.html --self-contained-html
"""

import time
from pages.login_page import LoginPage
from pages.secure_page import SecurePage


class TestLogin:
    """登录功能自动化测试"""

    def test_login_success(self, driver, login_page_url):
        """正确用户名 + 正确密码 → 提示登录成功"""
        driver.get(login_page_url)
        login_page = LoginPage(driver)

        login_page.login("tomsmith", "SuperSecretPassword!")
        time.sleep(0.5)

        secure_page = SecurePage(driver)
        assert "You logged into a secure area!" in secure_page.get_success_message()

    def test_login_wrong_password(self, driver, login_page_url):
        """正确用户名 + 错误密码 → 提示密码无效"""
        driver.get(login_page_url)
        login_page = LoginPage(driver)

        login_page.login("tomsmith", "wrongpassword")
        time.sleep(0.5)

        assert "Your password is invalid!" in login_page.get_flash_message()

    def test_login_empty_username(self, driver, login_page_url):
        """不输入用户名 → 提示用户名无效"""
        driver.get(login_page_url)
        login_page = LoginPage(driver)

        login_page.enter_password("SuperSecretPassword!")
        login_page.click_login()
        time.sleep(0.5)

        assert "Your username is invalid!" in login_page.get_flash_message()

    def test_login_wrong_username(self, driver, login_page_url):
        """不存在的用户名 → 提示用户名无效"""
        driver.get(login_page_url)
        login_page = LoginPage(driver)

        login_page.login("nobody", "SuperSecretPassword!")
        time.sleep(0.5)

        assert "Your username is invalid!" in login_page.get_flash_message()

    def test_logout(self, driver, login_page_url):
        """先登录成功，再点击登出 → 提示已登出"""
        driver.get(login_page_url)
        login_page = LoginPage(driver)
        login_page.login("tomsmith", "SuperSecretPassword!")
        time.sleep(0.5)

        secure_page = SecurePage(driver)
        secure_page.click_logout()
        time.sleep(0.5)

        assert "You logged out of the secure area!" in secure_page.get_logout_message()
