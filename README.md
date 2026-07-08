# 🔐 登录功能自动化测试项目

一个完整的软件测试进阶项目，涵盖**手工测试用例设计**、**Selenium 自动化测试**、**Page Object 工程化架构**、**JSON 数据驱动**四大核心技能，适合作为软件测试岗位实习的简历项目。

---

## 📋 项目简介

本项目以一个标准登录页面为测试对象，完整实践了软件测试的标准流程：

1. **需求分析** → 理解登录功能的需求规格
2. **手工用例设计** → 用等价类划分、边界值分析、错误推测法等方法设计 12 条手工用例
3. **自动化脚本编写** → 将核心流程转化为 5 条 Selenium + pytest 自动化用例
4. **Page Object 重构** → 引入页面对象模式，分离元素定位与业务逻辑
5. **数据驱动改造** → 测试数据外置到 JSON 文件，用 `@pytest.mark.parametrize` 驱动
6. **测试执行与报告** → 运行测试并生成 HTML 可视化报告

---

## 📁 项目结构

```
selenium-login-test/
├── pages/                        # Page Object 页面层
│   ├── base_page.py             # 基类：通用查找、等待、点击、输入
│   ├── login_page.py            # 登录页对象
│   └── secure_page.py           # 安全区域页对象
├── data/                         # 数据驱动层
│   └── login_data.json          # 登录场景测试数据（JSON）
├── test_cases/                   # 测试用例层
│   ├── conftest.py              # fixture + 数据加载函数
│   └── test_login.py            # 参数化测试（4 场景 + 1 登出）
├── test_pages/                   # 被测页面
│   └── login.html               # 本地模拟登录页
├── docs/                         # 测试文档
│   └── test_case_login.xlsx     # 手工测试用例 Excel（12 条）
├── reports/                      # 测试报告输出
├── requirements.txt             # Python 依赖
├── .gitignore                   # Git 忽略规则
└── README.md
```

---

## 🏗 架构设计

```
┌─────────────────────────────────────┐
│   data/login_data.json              │  ← JSON 数据层（新增场景只加一条记录）
└──────────────┬──────────────────────┘
               │ 驱动
┌──────────────▼──────────────────────┐
│   test_cases/test_login.py          │  ← 参数化测试（1 条方法覆盖 4 个场景）
│   @pytest.mark.parametrize(...)     │
└──────────────┬──────────────────────┘
               │ 调用
┌──────────────▼──────────────────────┐
│   pages/login_page.py               │  ← Page Object 层（封装元素和操作）
│   pages/secure_page.py              │
│   pages/base_page.py                │
└──────────────┬──────────────────────┘
               │ 驱动
┌──────────────▼──────────────────────┐
│   test_cases/conftest.py            │  ← driver fixture 生命周期管理
│   Selenium WebDriver (Edge)         │
└─────────────────────────────────────┘
```

**三层分离的好处**：
- 📝 **改数据**：只改 `data/login_data.json`，测试代码不动
- 🔧 **改页面**：只改 `pages/`，测试代码不动
- 🧪 **改逻辑**：只改 `test_cases/`，数据和页面不动

---

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.13+** | 自动化脚本语言 |
| **Selenium WebDriver** | 浏览器自动化操作 |
| **pytest** | 测试框架（fixture、参数化、断言） |
| **pytest-html** | 生成可视化 HTML 测试报告 |
| **webdriver-manager** | 自动管理浏览器驱动 |
| **Microsoft Edge (headless)** | 无头浏览器执行环境 |
| **Page Object Pattern** | 页面对象设计模式 |
| **JSON 数据驱动** | `@pytest.mark.parametrize` + JSON |

---

## 🧪 手工测试用例概览（12 条）

用例文件：`docs/test_case_login.xlsx`

| 测试方法 | 用例编号 | 覆盖场景 |
|----------|----------|----------|
| **功能测试** | TC_FUNC_001 ~ 003 | 正常登录、错误密码、空用户名 |
| **UI 测试** | TC_UI_001 ~ 002 | 控件存在性、页面跳转 |
| **安全测试** | TC_SEC_001 ~ 002 | SQL 注入、XSS 注入 |
| **兼容性测试** | TC_COMPAT_001 ~ 002 | Chrome / Edge 浏览器 |
| **异常测试** | TC_EXCEP_001 ~ 002 | 网络中断、多次错误锁定 |
| **性能测试** | TC_PERF_001 | 页面加载时间 |

**执行结果**：✅ 11 PASS / ❌ 1 FAIL

---

## 🤖 自动化测试用例（5 条）

### 参数化登录场景（4 条，数据驱动）

数据文件：`data/login_data.json`

| 编号 | 场景 | 用户名 | 密码 | 预期结果 |
|------|------|--------|------|----------|
| TC_LOGIN_001 | 正确登录 | `tomsmith` | `SuperSecretPassword!` | 登录成功 |
| TC_LOGIN_002 | 密码错误 | `tomsmith` | `wrongpassword` | 密码无效 |
| TC_LOGIN_003 | 用户名为空 | *(空)* | `SuperSecretPassword!` | 用户名无效 |
| TC_LOGIN_004 | 用户名错误 | `nobody` | `SuperSecretPassword!` | 用户名无效 |

### 独立用例

| 编号 | 用例名称 | 测试场景 |
|------|----------|----------|
| TC_LOGIN_005 | `test_logout` | 登录成功后点击登出 → 回到登录页 |

**执行结果**：✅ 5/5 全部 PASSED

> 💡 **新增场景只需在 JSON 中加一条记录**，无需修改测试代码。

---

## 🚀 快速开始

### 环境要求

- **Python 3.10+**（推荐 3.13）
- **Microsoft Edge 浏览器**（或其他 Chromium 内核浏览器）

### 1. 克隆项目

```bash
git clone https://github.com/XBT1236/selenium-login-test.git
cd selenium-login-test
```

### 2. 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. 运行测试

```bash
# 全部测试
pytest test_cases/test_login.py -v

# 生成 HTML 报告
pytest test_cases/test_login.py --html=reports/report.html --self-contained-html
```

---

## 🎯 项目亮点（面试／简历用）

- ✅ 独立完成 **手工用例设计 + 自动化实现** 全流程
- ✅ 掌握 **等价类划分、边界值分析、错误推测法** 等测试方法
- ✅ 熟练使用 **Selenium WebDriver + pytest** 企业级测试框架
- ✅ 采用 **Page Object 设计模式**，页面操作与测试逻辑分离
- ✅ 实现 **JSON 数据驱动测试**，使用 `@pytest.mark.parametrize` 参数化
- ✅ 使用 **pytest fixture** 管理驱动生命周期，工程化程度高
- ✅ 输出规范的 **HTML 测试报告** 和 **Excel 手工用例**

---

## 📚 学习路线建议

| 状态 | 方向 | 说明 |
|------|------|------|
| ✅ 已完成 | 手工用例设计 | 12 条用例，6 类测试方法 |
| ✅ 已完成 | Selenium 自动化 | 5 条自动化用例 |
| ✅ 已完成 | Page Object 重构 | 页面对象模式，三层架构 |
| ✅ 已完成 | 数据驱动测试 | JSON + parametrize |
| ⬜ 下一步 | **CI/CD 集成** | GitHub Actions 自动运行测试 |
| ⬜ | **接口测试项目** | requests + pytest 测 REST API |
| ⬜ | **性能测试** | Locust / JMeter |

---

## 📄 License

本项目仅用于学习与面试展示，可自由使用和修改。
