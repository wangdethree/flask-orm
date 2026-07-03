from flask import Blueprint, request, jsonify

from app import db, cache
from app.models.user import User

user_bp = Blueprint("user", __name__)

# 创建用户
@user_bp.route("", methods=["POST"])
def create_user():
    # 拿到前端传过来的数据
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "username, email, password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409

    from werkzeug.security import generate_password_hash

    # 创建用户
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created", "user": user.to_dict()}), 201

# 查询单个用户信息
@user_bp.route("/<int:user_id>", methods=["GET"])
@cache.cached(timeout=60, key_prefix="user_%s")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify({"user": user.to_dict()}), 200

# 查询所有用户
@user_bp.route("", methods=["GET"])
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "users": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
    }), 200

# 修改用户信息
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    data = request.get_json() or {}

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        from werkzeug.security import generate_password_hash
        user.password_hash = generate_password_hash(data["password"])
    if "is_active" in data:
        user.is_active = data["is_active"]

    db.session.commit()
    cache.delete(f"user_{user_id}")

    return jsonify({"message": "user updated", "user": user.to_dict()}), 200

# 删除用户
@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 拿到我们需要删除的对象
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    # 删除对象
    db.session.delete(user)
    db.session.commit()
    cache.delete(f"user_{user_id}")

    return jsonify({"message": "user deleted"}), 200
