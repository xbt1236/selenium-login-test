# -*- coding: utf-8 -*-
"""
Page Object 基类
封装 Selenium 通用操作：查找元素、等待、获取文本等
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """所有页面类的基类，提供通用方法"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, by, value):
        """查找单个元素"""
        return self.driver.find_element(by, value)

    def find_all(self, by, value):
        """查找多个元素"""
        return self.driver.find_elements(by, value)

    def wait_visible(self, by, value):
        """等待元素可见"""
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def wait_clickable(self, by, value):
        """等待元素可点击"""
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def get_text(self, by, value):
        """获取元素文本"""
        return self.find(by, value).text

    def is_displayed(self, by, value):
        """判断元素是否可见"""
        return self.find(by, value).is_displayed()

    def click(self, by, value):
        """点击元素"""
        self.wait_clickable(by, value).click()

    def type(self, by, value, text):
        """输入文本（先清空再输入）"""
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)
