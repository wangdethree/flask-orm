#!/bin/bash
# ============================================================
# 生成 AES 加密后的登录 payload
# 用法: python3 scripts/encrypt_login.py <username> <password>
# ============================================================
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.utils.aes_crypto import aes_encrypt

AES_KEY = os.environ.get("AES_KEY", "0123456789abcdef0123456789abcdef")

if len(sys.argv) != 3:
    print("Usage: python encrypt_login.py <username> <password>")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

payload = json.dumps({"username": username, "password": password})
encrypted = aes_encrypt(payload, AES_KEY)

print(f"Encrypted payload: {encrypted}")
print(f"")
print(f"curl 测试:")
print(f"  curl -X POST http://localhost:5050/api/auth/login \\")
print(f"    -H 'Content-Type: application/json' \\")
print(f"    -d '{{\"username\":\"{encrypted}\",\"password\":\"\"}}'")
