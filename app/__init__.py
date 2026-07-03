from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

from app.config import config_map

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config_map.get(config_name, config_map["development"]))

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    # 注册蓝图
    from app.api.user import user_bp
    from app.api.auth import auth_bp

    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # 注册 CLI 命令
    from app.commands import register_commands
    register_commands(app)

    # 健康检查端点
    @app.route("/health")
    def health_check():
        return {"status": "ok"}

    return app
