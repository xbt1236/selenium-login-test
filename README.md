# 🔐 登录功能自动化测试项目

一个完整的软件测试进阶项目，涵盖**手工测试用例设计**、**Selenium 自动化测试**、**Page Object 工程化架构**三大核心技能，适合作为软件测试岗位实习的简历项目。

---

## 📋 项目简介

本项目以一个标准登录页面为测试对象，完整实践了软件测试的标准流程：

1. **需求分析** → 理解登录功能的需求规格
2. **手工用例设计** → 用等价类划分、边界值分析、错误推测法等方法设计 12 条手工用例
3. **自动化脚本编写** → 将核心流程转化为 5 条 Selenium + pytest 自动化用例
4. **Page Object 重构** → 引入页面对象模式，分离元素定位与业务逻辑，提升可维护性
5. **测试执行与报告** → 运行测试并生成 HTML 可视化报告

测试目标为本地模拟登录页（`test_pages/login.html`），界面参考了经典的 [the-internet](https://the-internet.herokuapp.com/login) 测试网站。

---

## 📁 项目结构

```
selenium-login-test/
├── pages/                        # Page Object 页面层（元素定位 + 操作封装）
│   ├── __init__.py
│   ├── base_page.py             # 基类：通用查找、等待、点击、输入
│   ├── login_page.py            # 登录页对象（用户名、密码、登录按钮、提示消息）
│   └── secure_page.py           # 安全区域页对象（登出、成功消息）
├── test_cases/                   # 测试用例层（只写业务逻辑）
│   ├── conftest.py              # pytest fixture：driver 创建与销毁
│   └── test_login.py            # 登录功能自动化测试（5 条用例）
├── test_pages/                   # 被测页面
│   └── login.html               # 本地模拟登录页
├── docs/                         # 测试文档
│   └── test_case_login.xlsx     # 手工测试用例 Excel（12 条，6 类测试方法）
├── reports/                      # 测试报告输出
│   └── report.html              # pytest-html 生成的测试报告
├── build_xlsx.mjs               # 生成手工用例 Excel 的脚本
├── requirements.txt             # Python 依赖
├── .gitignore                   # Git 忽略规则
└── README.md                    # 项目说明
```

---

## 🏗 架构设计：Page Object 模式

```
┌─────────────────────────────────────┐
│   test_cases/test_login.py          │  ← 只写业务逻辑，不碰 DOM
│   "点击登录 → 断言提示消息"          │
└──────────────┬──────────────────────┘
               │ 调用
┌──────────────▼──────────────────────┐
│   pages/login_page.py               │  ← 封装页面元素和操作
│   pages/secure_page.py              │    元素定位集中管理
│   pages/base_page.py                │    页面结构变了只改这里
└──────────────┬──────────────────────┘
               │ 驱动
┌──────────────▼──────────────────────┐
│   test_cases/conftest.py            │  ← driver 生命周期管理
│   Selenium WebDriver (Edge)         │
└─────────────────────────────────────┘
```

**这样做的好处**：
- 🔧 **页面结构变化时**，只需改 `pages/` 下的定位器，测试用例不用动
- 📖 **测试用例可读性强**，一眼能看懂在测什么
- ♻️ **页面操作可复用**，多个测试用例共享同一个页面方法

---

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.13+** | 自动化脚本语言 |
| **Selenium WebDriver** | 浏览器自动化操作 |
| **pytest** | 测试框架（用例管理、断言、fixture） |
| **pytest-html** | 生成可视化 HTML 测试报告 |
| **webdriver-manager** | 自动管理浏览器驱动（Edge / Chrome） |
| **Microsoft Edge (headless)** | 无头浏览器执行环境 |
| **Page Object Pattern** | 页面对象设计模式，工程化架构 |

---

## 🧪 手工测试用例概览（12 条）

用例文件：`docs/test_case_login.xlsx`

用例覆盖 6 类测试方法：

| 测试方法 | 用例编号 | 覆盖场景 |
|----------|----------|----------|
| **功能测试** | TC_FUNC_001 ~ 003 | 正常登录、错误密码、空用户名 |
| **UI 测试** | TC_UI_001 ~ 002 | 控件存在性、页面跳转 |
| **安全测试** | TC_SEC_001 ~ 002 | SQL 注入、XSS 注入 |
| **兼容性测试** | TC_COMPAT_001 ~ 002 | Chrome / Edge 浏览器 |
| **异常测试** | TC_EXCEP_001 ~ 002 | 网络中断、多次错误锁定 |
| **性能测试** | TC_PERF_001 | 页面加载时间 |

**执行结果**：✅ 11 PASS / ❌ 1 FAIL（性能测试——本地环境无法精确测量网络延迟）

---

## 🤖 自动化测试用例（5 条）

用例文件：`test_cases/test_login.py`

| 编号 | 用例名称 | 测试场景 | 预期结果 |
|------|----------|----------|----------|
| TC_LOGIN_001 | `test_login_success` | 正确用户名 + 正确密码 | 跳转到成功页，显示成功消息 |
| TC_LOGIN_002 | `test_login_wrong_password` | 正确用户名 + 错误密码 | 停留在登录页，显示密码错误提示 |
| TC_LOGIN_003 | `test_login_empty_username` | 用户名为空 | 提示用户名为必填 |
| TC_LOGIN_004 | `test_login_wrong_username` | 不存在的用户名 | 提示用户名不存在 |
| TC_LOGIN_005 | `test_logout` | 登录成功后点击登出 | 回到登录页，显示登出成功消息 |

**执行结果**：✅ 5/5 全部 PASSED

---

## 🚀 快速开始

### 环境要求

- **Python 3.10+**（推荐 3.13）
- **Microsoft Edge 浏览器**（或其他 Chromium 内核浏览器）
- **Git**（可选，用于版本管理）

### 1. 克隆项目

```bash
git clone https://github.com/XBT1236/selenium-login-test.git
cd selenium-login-test
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行测试

```bash
# 运行全部自动化测试（简洁输出）
pytest test_cases/test_login.py -v

# 运行测试并生成 HTML 报告
pytest test_cases/test_login.py --html=reports/report.html --self-contained-html

# 运行指定用例
pytest test_cases/test_login.py::TestLogin::test_login_success -v
```

### 5. 查看报告

用浏览器打开 `reports/report.html` 即可看到可视化测试报告。

---

## ⚙️ 配置说明

### 切换浏览器

默认使用 **Edge 浏览器 + headless 模式**。如需使用 Chrome，修改 `test_cases/conftest.py` 中的 driver fixture：

```python
# 替换 Edge 为 Chrome：
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
```

### 关闭 headless 模式

如需看到浏览器实际操作过程，在 `conftest.py` 中注释掉：

```python
# options.add_argument("--headless=new")
```

---

## 🐛 常见问题

| 问题 | 解决方法 |
|------|----------|
| `ModuleNotFoundError: No module named 'selenium'` | 确认已在虚拟环境中执行 `pip install -r requirements.txt` |
| `WebDriverException: 'msedgedriver' executable needs to be in PATH` | Edge 未安装或版本过旧，更新 Edge 或切换为 Chrome |
| `ConnectionRefusedError` | 检查 `test_pages/login.html` 文件是否存在 |
| 中文乱码 | 确保文件编码为 UTF-8 |

---

## 🎯 项目亮点（面试／简历用）

- ✅ 独立完成 **手工用例设计 + 自动化实现** 全流程
- ✅ 掌握 **等价类划分、边界值分析、错误推测法** 等经典测试方法
- ✅ 熟练使用 **Selenium WebDriver + pytest** 企业级测试框架
- ✅ 采用 **Page Object 设计模式**，页面操作与测试逻辑分离，代码可维护性高
- ✅ 使用 **pytest fixture** 管理驱动生命周期，工程化程度高
- ✅ 输出规范的 **HTML 测试报告** 和 **Excel 手工用例**

---

## 📚 学习路线建议

完成本项目后，建议按以下方向进阶：

1. **数据驱动测试** → 用 `@pytest.mark.parametrize` + JSON/CSV 驱动用例，减少重复代码
2. **CI/CD 集成** → 接入 GitHub Actions，实现代码推送自动运行测试
3. **接口测试** → 学习 `requests` + `pytest` 做 API 测试
4. **性能测试** → 学习 `Locust` 或 `JMeter` 做压力测试
5. **App 端测试** → 学习 Appium 做移动端自动化测试

参考文档：[实习准备/学习路线与项目方向.md](../实习准备/学习路线与项目方向.md)

---

## 🧪 测试账号

被测页面内置测试账号：

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 普通用户 | `tomsmith` | `SuperSecretPassword!` |

---

## 📄 License

本项目仅用于学习与面试展示，可自由使用和修改。

---

> 💡 **提示**：如果你正在找软件测试实习，这个项目可以作为你的入门实战作品。建议将项目上传到 GitHub 并写在简历的「项目经验」板块。
