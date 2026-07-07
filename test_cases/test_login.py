# -*- coding: utf-8 -*-
# 登录功能自动化测试
#
# 测试页面：test_pages/login.html（本地模拟登录页）
# 测试账号：tomsmith / SuperSecretPassword!
#
# 运行方式：
#   pytest test_cases/test_login.py -v
#   pytest test_cases/test_login.py --html=reports/report.html --self-contained-html

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time


# 项目根目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_PAGE = "file:///" + os.path.join(PROJECT_DIR, "test_pages", "login.html").replace("\\", "/")


class TestLogin:
    """登录功能自动化测试"""

    def setup_method(self):
        """每个测试方法执行前：打开浏览器、访问登录页"""
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=options,
        )
        self.driver.get(LOGIN_PAGE)

    def teardown_method(self):
        """每个测试方法执行后：关闭浏览器"""
        time.sleep(0.5)
        self.driver.quit()

    # ── 用例1：正常登录 ──
    def test_login_success(self):
        """正确用户名 + 正确密码 → 提示登录成功"""
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        flash_msg = self.driver.find_element(By.ID, "flash")
        assert "You logged into a secure area!" in flash_msg.text

    # ── 用例2：密码错误 ──
    def test_login_wrong_password(self):
        """正确用户名 + 错误密码 → 提示密码无效"""
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        flash_msg = self.driver.find_element(By.ID, "flash")
        assert "Your password is invalid!" in flash_msg.text

    # ── 用例3：用户名为空 ──
    def test_login_empty_username(self):
        """不输入用户名 → 提示用户名无效"""
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        flash_msg = self.driver.find_element(By.ID, "flash")
        assert "Your username is invalid!" in flash_msg.text

    # ── 用例4：用户名错误 ──
    def test_login_wrong_username(self):
        """不存在的用户名 → 提示用户名无效"""
        self.driver.find_element(By.ID, "username").send_keys("nobody")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        flash_msg = self.driver.find_element(By.ID, "flash")
        assert "Your username is invalid!" in flash_msg.text

    # ── 用例5：登录后登出 ──
    def test_logout(self):
        """先登录成功，再点击登出 → 提示已登出"""
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        logout_btn = self.driver.find_element(By.ID, "logout-link")
        logout_btn.click()
        time.sleep(0.5)

        flash_msg = self.driver.find_element(By.ID, "flash")
        assert "You logged out of the secure area!" in flash_msg.text
