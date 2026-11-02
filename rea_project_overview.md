# REA (Reverse Engineer Anything) 项目详细解析

> 项目仓库：[https://github.com/morluto/rea](https://github.com/morluto/rea)  
> 官方网站：[https://rea.tools](https://rea.tools)  
> npm 包名：`rea-agents`

---

## 1. 项目定位与核心价值

**REA（Reverse Engineer Anything）** 是一个专为 **AI Agent（如 Cursor、Claude Code、Codex、Gemini CLI 等）** 设计的**逆向工程与程序分析工具套件**，支持从宏观应用行为一直分析到底层原生二进制文件。

### 核心痛点与理念
在传统软件开发中，开发者看到竞品或第三方应用的某个优秀功能（如搜索算法、富文本剪贴板桥接、网络交互逻辑）时，由于没有源码，很难准确还原其实现细节。
**REA 的核心目标**：
让开发者能够对 AI 助手说：
> *"分析一下这个应用里的搜索功能是怎么实现的，展示相关代码和调用证据，并在我的项目中复现类似的功能。"*

AI Agent 通过 REA 提供的工具能力，自动化进行逆向、反编译、静态与动态分析，提供严密的**证据链（Evidence）**，并根据分析结果为用户编写出功能一致的实现代码。

---

## 2. 核心架构与运行机制

REA 基于 **Model Context Protocol (MCP)** 构建，将复杂的逆向工具链封装成标准化工具供 Agent 调度：

```text
[ 用户指令 ]
     │
     ▼
[ AI Agent (Cursor / Claude / Codex / Gemini) ]
     │  (MCP 协议调用工具)
     ▼
[ REA 本地服务端 (rea-agents) ]
     │
     ├─► JavaScript / Electron 分析器 (@babel/parser, @electron/asar, source-maps)
     ├─► 原生反编译桥接层 (Hopper Disassembler / Ghidra / IDA Pro)
     ├─► 移动与固件分析器 (JADX 反编译 APK, Binwalk / Unblob 解包固件)
     ├─► 浏览器与网络分析器 (Playwright, HAR 抓包解析)
     ├─► 运行时监控 (PTY 伪终端, Linux 崩溃转储分析)
     └─► 智能合约解析器 (EVM Bytecode 反编译 / evmole 选择器提取)
```

### 隐私与安全
- **100% 本地化分析**：所有的反编译、静态解包与动态分析均在开发者本地计算机上执行，**不会**将目标程序或二进制文件上传到第三方服务器。
- Agent 仅接收分析后的关键伪代码、AST 片段、符号及调用证据。

---

## 3. 支持分析的目标与能力矩阵

| 分析目标类型 | REA 能够提取与分析的内容 | 底层依赖与工具 |
| :--- | :--- | :--- |
| **原生二进制 (Native Binaries)** | 汇编代码、反编译伪代码 (C/C++)、字符串、导入/导出符号、交叉引用与调用图 | Hopper, Ghidra 或 IDA Pro（实验性支持 16 位 DOS） |
| **JavaScript / Electron 应用** | ASAR 解包、模块依赖图、Source Map 还原源码、IPC 通信端点、Native C++ 插件边界 | `@electron/asar`, `@babel/parser`, `@jridgewell/trace-mapping` |
| **网页与前端站点 (Websites)** | 页面 DOM 结构、脚本执行流、网络 API 调用、界面截图 | Chromium / Playwright |
| **网络流量抓包 (Captures)** | 结构化请求/响应分析、未公开 Payload 解析、前端触发代码定位 | HAR 文件、mitmproxy |
| **.NET 程序集 (.NET)** | 元数据、CIL 中间语言指令、原生依赖声明、不同构建版本差异 | 内置静态 Managed-code 检查器 |
| **Android APK** | AndroidManifest 配置、Java/Kotlin 反编译类与方法、资源引用 | 无头 JADX + JDK |
| **嵌入式固件 (Firmware)** | 固件分区识别、文件系统解包、原生可执行文件转交分析 | Binwalk, Unblob |
| **EVM 智能合约** | 函数分发选择器 (Selectors)、字节偏移、参数推断与只读/修改状态分析 | `evmole`, EVM Bytecode 静态分析 |
| **进程动态行为** | 终端输出流捕获、交互式命令行响应、文件系统修改监控 | `@lydell/node-pty`, `@xterm/headless` |

---

## 4. 经典实战案例 (Showcases)

1. **DX-Ball 音效声道平移计算还原**：
   - 从旧版 x86 游戏的音频调用一路追踪至声音位置与左右平移辅助函数，通过汇编与反编译伪代码重构出纯 C 语言函数。
   - 重构出的代码通过了全部 3,205 组原始 x86 用例测试，生成的 63 字节机器码与原版完全一致。
2. **Notion 桌面端剪贴板 IPC 通信链路追踪**：
   - 分析 Notion Electron 客户端的渲染进程剪贴板 API，穿透 Preload 脚本并捕获 IPC 发送给主进程的流程，成功复现了其富文本剪贴板格式规范。
3. **东方 Project (TH04) 16 位 DOS 弹幕计算算法恢复**：
   - 使用 Ghidra 逆向 PC-98 平台 16 位 DOS 汇编指令，恢复了自机狙与固定角度弹幕算法，并还原出与历史编译器完全一致的 C++ 算法代码。

---

## 5. 快速上手与集成方式

### 方式 1：一键为 AI Agent 配置 MCP 环境（推荐）
```bash
npx rea-agents setup
```
支持自动检测并注册至 Cursor、Claude Code、Codex、Gemini CLI 等主流客户端，同时注入对应的工作流技能（Skill）。

### 方式 2：作为独立命令行工具（CLI）使用
```bash
# 全局安装
npm install --global rea-agents

# 示例：快速分析一个 Electron 应用或导出的 JavaScript 包
npx -y rea-agents@latest analyze-javascript-application "D:/path/to/app" --json
```

---

## 6. 总结评价

REA 是当前 AI Agent 生态中**极其罕见的将系统级逆向工程深度融合进 Agent 工作流**的前沿项目：
- 极大地降低了没有资深逆向工程背景的普通开发者**探索第三方应用黑盒机制、挖掘未公开 API、逆向复现特定底层算法**的技术门槛。
- 不仅仅提供“反编译文本”，而是以**结构化证据链（Evidence）**的方式与 Agent 协同，让 Agent 能够基于证据闭环完成“分析 ➔ 假设 ➔ 验证 ➔ 编码 ➔ 测试”。
