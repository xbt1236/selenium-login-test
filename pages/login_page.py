# -*- coding: utf-8 -*-
"""
登录页面对象
封装登录页的所有元素定位和操作方法
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面"""

    # ── 元素定位器（集中管理，改页面结构时只改这里）──
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGIN_FORM = (By.ID, "login-form")

    # ── 页面操作方法 ──

    def enter_username(self, username):
        """输入用户名"""
        self.type(*self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """输入密码"""
        self.type(*self.PASSWORD_INPUT, password)

    def click_login(self):
        """点击登录按钮"""
        self.click(*self.LOGIN_BUTTON)

    def login(self, username, password):
        """执行完整登录流程：输入用户名 + 密码 + 点击登录"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_flash_message(self):
        """获取提示消息文本"""
        self.wait_visible(*self.FLASH_MESSAGE)
        return self.get_text(*self.FLASH_MESSAGE)

    def is_login_form_visible(self):
        """判断登录表单是否可见"""
        return self.is_displayed(*self.LOGIN_FORM)
