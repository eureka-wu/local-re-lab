# 无忧行 (JegoTrip) 云端无头接码 Docker 部署套件

本项目提供了将**无忧行（免插卡接收中国移动短信）**跑在云端 Linux 服务器上的完整容器化部署方案。无需在本地开发机运行，直接打包上传至云服务器即可一键启动。

---

## 1. 目录结构
```text
jegotrip/docker/
├── docker-compose.yml   # 容器编排 (Redroid Android 11 + 短信接收网关)
├── server.py            # 短信 Webhook 接收、提取验证码、转发服务 (FastAPI)
├── Dockerfile           # 短信接收网关镜像构建文件
├── setup.sh             # Linux 服务器一键初始化脚本
└── README.md            # 本使用说明
```

---

## 2. 部署步骤（云服务器）

### 准备环境
- **操作系统**：Ubuntu 20.04 / 22.04 / Debian 11+
- **系统工具**：Docker、Docker Compose、ADB

### 一键部署
1. 将 `jegotrip` 目录打包上传至云服务器。
2. 进入 `docker` 目录并运行初始化脚本：
   ```bash
   cd jegotrip/docker
   chmod +x setup.sh
   bash setup.sh
   ```
3. 脚本会自动加载内核模块、启动 `redroid` 和 `sms-receiver`，并将同级目录下的 `jegotrip_v8.9.6.0.apk` 安装到容器中。

---

## 3. 初始登录与开启托管

由于首次登录需要手机短信验证码并点击开启“托管”，推荐通过 **Scrcpy** 远程投屏操作：

1. 在本地电脑终端运行（需放行服务器 5555 端口或通过 SSH 端口转发）：
   ```bash
   scrcpy -s <服务器IP>:5555
   ```
2. 在投屏界面中打开**无忧行 App**，输入国内手机号获取验证码登录。
3. 进入 **【我的】 -> 【免费接听与短信托管】**：
   - 勾选开启“免费接收短信”和“免费接听电话”。
4. 在容器中安装开源短信转发器 **SmsForwarder**（[下载地址](https://github.com/pppscn/SmsForwarder/releases)）：
   ```bash
   adb -s <服务器IP>:5555 install SmsForwarder.apk
   ```
5. 打开 SmsForwarder：
   - 授予“通知监听权限”。
   - 添加“应用列表过滤器”：仅勾选 **无忧行**。
   - 添加发送通道为 **Webhook**：
     - 请求地址填入：`http://sms-receiver:8080/sms`（Docker 内部网络）或 `http://127.0.0.1:8080/sms`。

---

## 4. API 接口与外部对接

短信接收服务启动在 `8080` 端口：

| 接口 | 方法 | 说明 | 示例返回值 |
| :--- | :---: | :--- | :--- |
| `/sms` | `POST` | SmsForwarder 推送端点（内置正则自动提取 4~6 位验证码） | `{"status": "ok", "code": "629104"}` |
| `/latest` | `GET` | 供外部脚本/自动化任务快速轮询最新验证码 | `{"latest_code": "629104", "latest_sms": {...}}` |
| `/` | `GET` | 服务健康检查及缓存短信列表 | `{"status": "running", "cached_count": 5}` |

---

## 5. 关键运维注意事项

1. **托管续期**：无忧行号码托管通常每 21~30 天需在 App 内点击一次续期。
2. **防休眠保活**：如发现容器休眠，可通过服务器 `crontab` 每 5 分钟执行一次屏幕唤醒：
   ```bash
   */5 * * * * adb -s 127.0.0.1:5555 shell input keyevent 224 >/dev/null 2>&1
   ```

