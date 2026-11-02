# Local RE Lab (本地逆向与安全实验室)

`local-re-lab` 是一个专注于**本地逆向工程、网络流量捕获与应用安全分析**的学习与实战工作台。

项目结合了现代 AI Agent 技能体系，支持针对多端目标（Android APK、Windows EXE、macOS DMG、React Native / Electron）进行静态反编译、动态分析与网络协议剖析。

---

## 核心特性

- **网络流量分析与协议捕获 (Traffic Capture)**：
  - 基于 `mitmproxy`、`Wireshark` 与 `tshark` 的自动化数据流拦截、过滤与持久化；
  - 覆盖 TLS 解密、SSL Pinning 绕过及私有通信协议重构。
- **跨平台逆向工程规范 (Reverse Engineering)**：
  - 集成官方 **REA (Reverse Engineer Anything)** 逆向技能体系；
  - 覆盖 Android (APK / DEX / SO)、原生二进制 (PE / ELF / Mach-O) 及 JavaScript 混合架构的证据链驱动分析。
- **客户端与传输安全审计 (Security Audit)**：
  - 移动端 IPC、本地数据存储、签名验证机制及 API 鉴权漏洞排查。

---

## 目录结构概览

```text
local-re-lab/
├── skills/                                    # AI Agent 逆向与安全专属技能矩阵
│   ├── reverse-engineer-anything/             # 官方 REA 全能逆向核心及各系统实战手册
│   ├── protocol-reverse-engineering/          # 协议与网络抓包实战指南
│   └── security-audit/                        # 客户端与网络安全审计规范
├── jegotrip/                                  # 目标应用实战样本与分析案例
├── mitmproxy-12.3.0-windows-x86_64-installer.exe # 本地抓包工具安装程序
├── AGENT.md                                   # AI Agent 项目全局操作与推理规范
└── .gitignore                                 # 自动过滤超大二进制与运行时日志
```

---

## 快速上手

### 1. 结合 AI Agent 展开逆向分析
项目内置了完整的 `skills/` 规范，当你使用支持 Agent 技能的环境（如 Antigravity、Claude Code、Cursor）打开本项目时，Agent 会自动激活逆向与抓包分析专家能力：
- 询问特定应用逻辑（如加密算法、网络接口、组件调用）；
- Agent 将遵循“证据链规范（Evidence-based）”展开代码与调用图定位。

### 2. 启动网络流量抓包
使用项目自带的 mitmproxy 或本地环境：
```bash
# 启动 mitmproxy 并加载目标过滤脚本
mitmweb -s <target_app>/mitm_capture.py -p 8080
```

---

## 免责声明

本项目及相关文档仅供**安全研究、合规逆向与协议互操作性学习**使用，严禁用于任何非法攻击或未授权测试。
