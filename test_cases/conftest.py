# -*- coding: utf-8 -*-
"""
pytest 公共配置
- WebDriver fixture：创建/销毁 Edge 浏览器
- 数据驱动：从 JSON 文件加载测试数据
"""

import json
import os
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 项目根目录 & 登录页 URL
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_PAGE = "file:///" + os.path.join(PROJECT_DIR, "test_pages", "login.html").replace("\\", "/")
DATA_DIR = os.path.join(PROJECT_DIR, "data")


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


def load_login_scenarios():
    """从 JSON 文件加载登录场景测试数据，供 @pytest.mark.parametrize 使用"""
    filepath = os.path.join(DATA_DIR, "login_data.json")
    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    return data["login_scenarios"]
