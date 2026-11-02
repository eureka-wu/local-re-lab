"""
Mitmproxy Traffic Capture Addon Script
Run with:
    mitmdump -s mitm_capture.py -p 8080
    or
    mitmweb -s mitm_capture.py -p 8080
"""

import json
import os
import time
from mitmproxy import http
from mitmproxy import ctx

# Target domains to capture (leave empty to capture all traffic)
TARGET_DOMAINS = [
    "jegotrip.com",
    "jegotrip.com.cn",
    "jegotrip.cn",
    "cmi.chinamobile.com",
    "chinamobile.com",
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "captures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class TrafficCaptureAddon:
    def __init__(self):
        self.log_file = os.path.join(OUTPUT_DIR, f"capture_{int(time.time())}.jsonl")
        ctx.log.info(f"[TrafficCapture] Log output: {self.log_file}")

    def request(self, flow: http.HTTPFlow):
        host = flow.request.pretty_host
        if TARGET_DOMAINS and not any(d in host for d in TARGET_DOMAINS):
            return

        ctx.log.info(f"[REQ] {flow.request.method} {flow.request.pretty_url}")

    def response(self, flow: http.HTTPFlow):
        host = flow.request.pretty_host
        if TARGET_DOMAINS and not any(d in host for d in TARGET_DOMAINS):
            return

        status = flow.response.status_code if flow.response else 0
        ctx.log.info(f"[RESP] {status} {flow.request.pretty_url}")

        record = {
            "timestamp": time.time(),
            "url": flow.request.pretty_url,
            "method": flow.request.method,
            "request_headers": dict(flow.request.headers),
            "request_body": flow.request.get_text(strict=False),
            "status_code": status,
            "response_headers": dict(flow.response.headers) if flow.response else {},
            "response_body": flow.response.get_text(strict=False) if flow.response else "",
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


addons = [TrafficCaptureAddon()]

