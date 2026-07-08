# -*- coding: utf-8 -*-
"""
安全区域页面对象
封装登录成功后的 Secure Area 页面操作
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SecurePage(BasePage):
    """登录成功后的安全区域页面"""

    # ── 元素定位器 ──
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_LINK = (By.ID, "logout-link")
    SECURE_AREA = (By.ID, "secure-area")

    # ── 页面操作方法 ──

    def get_success_message(self):
        """获取登录成功提示消息"""
        self.wait_visible(*self.FLASH_MESSAGE)
        return self.get_text(*self.FLASH_MESSAGE)

    def click_logout(self):
        """点击登出链接"""
        self.click(*self.LOGOUT_LINK)

    def is_secure_area_visible(self):
        """判断安全区域是否可见"""
        return self.is_displayed(*self.SECURE_AREA)

    def get_logout_message(self):
        """获取登出提示消息"""
        self.wait_visible(*self.FLASH_MESSAGE)
        return self.get_text(*self.FLASH_MESSAGE)
