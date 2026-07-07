import fs from "node:fs/promises";
import path from "node:path";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const wb = Workbook.create();
const s = wb.worksheets.add("登录功能测试用例");

s.getRange("A:A").format.columnWidth = 55;
s.getRange("B:B").format.columnWidth = 18;
s.getRange("C:C").format.columnWidth = 38;
s.getRange("D:D").format.columnWidth = 52;
s.getRange("E:E").format.columnWidth = 46;
s.getRange("F:F").format.columnWidth = 22;
s.getRange("G:G").format.columnWidth = 32;

const LQ = "\u201C", RQ = "\u201D", ARROW = "\u2192";

const hdr = s.getRange("A1:G1");
hdr.values = [["用例编号","模块","前置条件","测试步骤","预期结果","实际结果","测试方法"]];
hdr.format.font = { bold: true, size: 11, name: "微软雅黑", color: "#FFFFFF" };
hdr.format.fill.color = "#4472C4";
hdr.format.alignment = { horizontal: "center", vertical: "center" };
hdr.format.rowHeight = 28;

const tc = [
  ["TC_LOGIN_001","登录功能","1. 已知有效账号：tomsmith\n2. 已知有效密码：SuperSecretPassword!\n3. 浏览器已打开，位于登录页面","1. 在用户名输入框输入 tomsmith\n2. 在密码输入框输入 SuperSecretPassword!\n3. 点击 Login 按钮","1. 页面提示"+LQ+"You logged into a secure area!"+RQ+"\n2. 显示"+LQ+"Welcome to the Secure Area"+RQ+"区域\n3. 登录表单隐藏，Logout 链接显示","PASS","等价类划分（有效等价类）"],
  ["TC_LOGIN_002","登录功能","1. 已知有效账号：tomsmith\n2. 浏览器已打开，位于登录页面","1. 在用户名输入框输入 tomsmith\n2. 在密码输入框输入 wrongpassword\n3. 点击 Login 按钮","1. 页面提示"+LQ+"Your password is invalid!"+RQ+"\n2. 提示信息以错误样式（红色）显示\n3. 登录表单保持可见，未进入安全区域","PASS","等价类划分（无效等价类-密码错误）"],
  ["TC_LOGIN_003","登录功能","浏览器已打开，位于登录页面","1. 不输入用户名（保持为空）\n2. 在密码输入框输入 SuperSecretPassword!\n3. 点击 Login 按钮","1. 页面提示"+LQ+"Your username is invalid!"+RQ+"\n2. 提示信息以错误样式（红色）显示\n3. 登录表单保持可见","PASS","等价类划分（无效等价类-用户名为空）"],
  ["TC_LOGIN_004","登录功能","浏览器已打开，位于登录页面","1. 在用户名输入框输入 nobody\n2. 在密码输入框输入 SuperSecretPassword!\n3. 点击 Login 按钮","1. 页面提示"+LQ+"Your username is invalid!"+RQ+"\n2. 提示信息以错误样式（红色）显示\n3. 登录表单保持可见，未跳转","PASS","等价类划分（无效等价类-用户名错误）"],
  ["TC_LOGIN_005","登录功能","1. 已用 tomsmith / SuperSecretPassword! 成功登录\n2. 当前位于安全区域页面","1. 点击 Logout 链接","1. 页面提示"+LQ+"You logged out of the secure area!"+RQ+"\n2. 提示信息以成功样式（绿色）显示\n3. 安全区域隐藏，登录表单重新显示\n4. 用户名和密码输入框已清空","PASS","业务流程测试（登录"+ARROW+"登出完整链路）"],
  ["TC_LOGIN_006","登录功能","浏览器已打开，位于登录页面","1. 在用户名输入框输入 tomsmith\n2. 不输入密码（保持为空）\n3. 点击 Login 按钮","1. 页面提示"+LQ+"Your password is invalid!"+RQ+"\n2. 提示信息以错误样式显示\n3. 登录表单保持可见","PASS","等价类划分（无效等价类-密码为空）"],
  ["TC_LOGIN_007","登录功能","浏览器已打开，位于登录页面","1. 用户名和密码均不输入\n2. 点击 Login 按钮","1. 页面提示"+LQ+"Your username is invalid!"+RQ+"\n2. 提示信息以错误样式显示\n3. 登录表单保持可见","PASS","边界值分析（全部为空）"],
  ["TC_LOGIN_008","登录功能","浏览器已打开，位于登录页面","1. 在用户名输入框输入   tomsmith   （前后各三个空格）\n2. 在密码输入框输入 SuperSecretPassword!\n3. 点击 Login 按钮","1. 页面提示"+LQ+"Your username is invalid!"+RQ+"\n2. 说明系统未对用户名做 trim 处理\n3. 登录失败，登录表单保持可见","FAIL","边界值分析（用户名前后带空格）"],
  ["TC_LOGIN_009","登录功能","浏览器已打开，位于登录页面","1. 在用户名输入框输入 tomsmith\n2. 在密码输入框输入包含特殊字符的密码：Super!@#$%^&*()\n3. 点击 Login 按钮","1. 页面提示"+LQ+"Your password is invalid!"+RQ+"\n2. 登录失败","PASS","边界值分析（特殊字符密码）"],
  ["TC_LOGIN_010","登录功能","1. 已成功登录\n2. 刷新浏览器页面","1. 点击浏览器刷新按钮或按 F5 刷新","1. 页面应保持登录状态\n2. 或跳回登录页并要求重新登录（取决于实现）","PASS","异常场景测试（页面刷新）"],
  ["TC_LOGIN_011","登录功能","浏览器已打开，位于登录页面","1. 使用键盘 Tab 键在用户名和密码输入框之间切换\n2. 按 Enter 键提交表单（替代鼠标点击）","1. Tab 键切换焦点顺序正常：用户名"+ARROW+"密码"+ARROW+"登录按钮\n2. 按 Enter 键可正常提交登录表单\n3. 登录结果与鼠标操作一致","PASS","UI 交互测试（键盘操作）"],
  ["TC_LOGIN_012","登录功能","1. 首次登录成功后登出\n2. 再次访问登录页面","1. 使用正确账号密码再次登录\n2. 点击登出\n3. 重复以上步骤 3 次","1. 每次登录和登出均正常\n2. 无异常报错\n3. 页面状态切换正确","PASS","稳定性测试（反复登录登出）"],
];

const n = tc.length;
const dr = s.getRange("A2:G" + (1 + n));
dr.values = tc;
dr.format.font = { size: 10, name: "宋体" };
dr.format.alignment = { vertical: "top", wrapText: true };
dr.format.rowHeight = 60;

s.getRange("A2:A" + (1 + n)).format.alignment = { horizontal: "center", vertical: "center" };
s.getRange("B2:B" + (1 + n)).format.alignment = { horizontal: "center", vertical: "center" };
s.getRange("G2:G" + (1 + n)).format.alignment = { horizontal: "center", vertical: "center" };

for (let row = 2; row <= 1 + n; row++) {
  const cell = s.getRange("F" + row);
  cell.format.alignment = { horizontal: "center", vertical: "center" };
  cell.format.font = { bold: true, color: tc[row-2][5]==="PASS" ? "#00B050" : "#FF0000", size: 10 };
}

const sr = n + 2;
s.getRange("A" + sr + ":G" + sr).merge();

const passN = tc.filter(t => t[5]==="PASS").length;
const failN = tc.filter(t => t[5]==="FAIL").length;
const pct = Math.round(passN / n * 100);

s.getRange("A" + sr).values = [[
  "测试总结：共 "+n+" 条用例，通过 "+passN+" 条，失败 "+failN+" 条，通过率 "+pct+"%。已覆盖等价类划分、边界值分析、业务流程测试、UI 交互测试、异常场景测试、稳定性测试共 6 类测试方法。"
]];
s.getRange("A" + sr).format.font = { bold: true, size: 10, name: "微软雅黑" };
s.getRange("A" + sr).format.alignment = { horizontal: "left", vertical: "center" };

const fr = s.getRange("A1:G" + sr);
fr.format.borders = { preset: "outside", style: "medium", color: "#4472C4" };

s.showGridlines = false;
s.freezePanes.freezeRows(1);

const d = "C:\\Users\\Administrator\\Documents\\New project\\selenium-login-test\\docs";
await fs.mkdir(d, { recursive: true });
const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(path.join(d, "test_case_login.xlsx"));
console.log("Done: docs/test_case_login.xlsx");
