import os
import re
import json
import time
import requests
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI(title="JegoTrip SMS Webhook Receiver", version="1.0.0")

LOG_FILE = "/app/logs/sms_history.jsonl"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 内存保留最近 50 条短信，便于外部接口快速轮询
sms_cache: List[dict] = []

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
WECHAT_WEBHOOK_URL = os.getenv("WECHAT_WEBHOOK_URL")


class SmsPayload(BaseModel):
    content: Optional[str] = ""
    title: Optional[str] = ""
    sender: Optional[str] = ""
    time: Optional[str] = None


def extract_verification_code(text: str) -> Optional[str]:
    """通过正则提取 4-6 位验证码"""
    patterns = [
        r'(?:验证码|动态码|校验码|code is)[：:\s]*([0-9]{4,6})',
        r'([0-9]{4,6})[^\d]*(?:为您的验证码|是您的验证码|为本次验证)',
        r'【.+】.*?([0-9]{4,6})',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def forward_to_external_channels(msg: dict):
    """转发至 Telegram 或企业微信"""
    text = (
        f"📩 【无忧行新短信】\n"
        f"• 发件人: {msg.get('sender')}\n"
        f"• 验证码: {msg.get('code') or '未识别'}\n"
        f"• 内容: {msg.get('content')}\n"
        f"• 时间: {msg.get('time')}"
    )

    # 1. Telegram
    if TG_BOT_TOKEN and TG_CHAT_ID:
        try:
            tg_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
            requests.post(tg_url, json={"chat_id": TG_CHAT_ID, "text": text}, timeout=5)
        except Exception as e:
            print(f"[TG Error] {e}")

    # 2. 企业微信 Webhook
    if WECHAT_WEBHOOK_URL:
        try:
            requests.post(
                WECHAT_WEBHOOK_URL,
                json={"msgtype": "text", "text": {"content": text}},
                timeout=5
            )
        except Exception as e:
            print(f"[WeChat Error] {e}")


@app.get("/")
def index():
    return {
        "service": "JegoTrip SMS Receiver",
        "status": "running",
        "cached_count": len(sms_cache),
        "latest": sms_cache[0] if sms_cache else None
    }


@app.post("/sms")
async def receive_sms(request: Request):
    """SmsForwarder 推送通知接收端点"""
    try:
        data = await request.json()
    except Exception:
        body = await request.body()
        data = {"content": body.decode("utf-8", errors="ignore")}

    content = data.get("content") or data.get("msg") or str(data)
    sender = data.get("sender") or data.get("title") or "Unknown"
    receive_time = data.get("time") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    code = extract_verification_code(content)

    record = {
        "timestamp": time.time(),
        "time": receive_time,
        "sender": sender,
        "content": content,
        "code": code,
        "raw": data
    }

    # 写入内存缓存
    sms_cache.insert(0, record)
    if len(sms_cache) > 50:
        sms_cache.pop()

    # 持久化到日志
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\n[新短信入库] 来自: {sender} | 验证码: {code}\n内容: {content}")

    # 异步或同步转发
    forward_to_external_channels(record)

    return {"status": "ok", "code": code}


@app.get("/latest")
def get_latest():
    """自动化脚本调用的快速查码接口"""
    if not sms_cache:
        return {"code": None, "msg": "No SMS received yet"}
    return {
        "latest_code": sms_cache[0].get("code"),
        "latest_sms": sms_cache[0]
    }

