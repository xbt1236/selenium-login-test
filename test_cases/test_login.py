# -*- coding: utf-8 -*-
"""
登录功能自动化测试（数据驱动版）

架构：Page Object 模式 + JSON 数据驱动
- 测试数据统一放在 data/login_data.json 中
- 新增场景只需加一条 JSON 记录，无需改测试代码

运行方式：
    pytest test_cases/test_login.py -v
    pytest test_cases/test_login.py --html=reports/report.html --self-contained-html
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.secure_page import SecurePage
from test_cases.conftest import load_login_scenarios


class TestLogin:
    """登录功能自动化测试"""

    @pytest.mark.parametrize("scenario", load_login_scenarios(), ids=lambda s: s["id"])
    def test_login_scenarios(self, driver, login_page_url, scenario):
        """数据驱动：根据 JSON 数据执行登录场景测试"""
        driver.get(login_page_url)
        login_page = LoginPage(driver)

        # 执行登录操作
        if scenario.get("skip_username"):
            login_page.enter_password(scenario["password"])
            login_page.click_login()
        else:
            login_page.login(scenario["username"], scenario["password"])
        time.sleep(0.5)

        # 验证结果
        if scenario["expect_success"]:
            secure_page = SecurePage(driver)
            assert scenario["expected_message"] in secure_page.get_success_message()
        else:
            assert scenario["expected_message"] in login_page.get_flash_message()

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
