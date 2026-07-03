import json
from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, current_app, request, jsonify
from werkzeug.security import check_password_hash

from app.models.user import User
from app.utils.aes_crypto import aes_decrypt

auth_bp = Blueprint("auth", __name__)

# 登陆功能
@auth_bp.route("/login", methods=["POST"])
def login():
    # 拿到前端传过来的数据
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # 是否开启加密模式
    enable_encryption = current_app.config.get("ENABLE_ENCRYPTION", False)

    if enable_encryption:
        try:
            aes_key = current_app.config["AES_KEY"]
            decrypted = aes_decrypt(username, aes_key)
            payload = json.loads(decrypted)
            username = payload.get("username", "")
            password = payload.get("password", "")
        except Exception:
            return jsonify({"error": "decryption failed"}), 400

    # 查询用户是否存在
    user = User.query.filter_by(username=username).first()
    # 用户不存在或密码错误
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    # 登陆成功，拿到对应的jwt信息
    token = _generate_jwt(user)

    return jsonify({"token": token, "user": user.to_dict()}), 200


# 生成jwt认证信息
def _generate_jwt(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "uuid": user.uuid,
        "exp": datetime.now(timezone.utc) + timedelta(
            hours=current_app.config["JWT_EXPIRATION_HOURS"]
        ),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
