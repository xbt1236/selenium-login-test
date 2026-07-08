# -*- coding: utf-8 -*-
"""
pytest 公共配置
将 WebDriver 的创建和销毁提取为 fixture，供所有测试用例共享
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 项目根目录 & 登录页 URL
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_PAGE = "file:///" + os.path.join(PROJECT_DIR, "test_pages", "login.html").replace("\\", "/")


@pytest.fixture
def driver():
    """创建 Edge headless 浏览器实例，测试结束后自动关闭"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options,
    )
    yield driver
    driver.quit()


@pytest.fixture
def login_page_url():
    """登录页 URL"""
    return LOGIN_PAGE
