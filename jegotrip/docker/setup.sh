#!/bin/bash
# ==============================================================================
# 无忧行 (JegoTrip) 云端短信接收容器化部署脚本 (适用于 Ubuntu / Debian)
# ==============================================================================

set -e

echo "[1/5] 检查并加载 Linux 内核 Binder 模块..."
sudo apt-get update && sudo apt-get install -y linux-modules-extra-$(uname -r) adb curl
sudo modprobe binder_linux devices="binder,hwbinder,vndbinder" || true
sudo modprobe ashmem_linux || true

echo "[2/5] 启动 Docker 容器群 (Redroid + SMS Receiver)..."
docker compose down || true
docker compose up -d

echo "[3/5] 等待 Android 容器完全启动..."
sleep 15
adb connect 127.0.0.1:5555 || true
adb wait-for-device

echo "[4/5] 自动安装无忧行 APK 到 Redroid 容器..."
if [ -f "../jegotrip_v8.9.6.0.apk" ]; then
    echo "正在安装 无忧行 App..."
    adb -s 127.0.0.1:5555 install -r "../jegotrip_v8.9.6.0.apk"
else
    echo "未检测到 ../jegotrip_v8.9.6.0.apk，请手动安装！"
fi

echo "[5/5] 部署完成！"
echo "------------------------------------------------------------------------"
echo "1. 请在电脑端使用 scrcpy 远程控制该 Android 容器完成手机号登录与托管开启："
echo "   scrcpy -s <服务器IP>:5555"
echo "2. 安装 SmsForwarder 短信转发器并设置 Webhook 推送地址为："
echo "   http://sms-receiver:8080/sms 或 http://<服务器内网IP>:8080/sms"
echo "3. 外部业务系统获取最新验证码接口："
echo "   curl http://<服务器IP>:8080/latest"
echo "------------------------------------------------------------------------"

