import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_EXPIRATION_HOURS = 24

    # 本地数据库 B（可读写）
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "mysql+pymysql://root:root@127.0.0.1:3306/dg_orm"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 远程数据库 A（只读，用于同步）
    REMOTE_DB_URI = os.environ.get(
        "REMOTE_DB_URI",
        "mysql+pymysql://root:root@172.26.22.190:10431/dg_oauth"
    )

    # AES 加密配置
    AES_KEY = os.environ.get("AES_KEY", "0123456789abcdef0123456789abcdef")
    ENABLE_ENCRYPTION = os.environ.get("ENABLE_ENCRYPTION", "false").lower() == "true"

    # Redis 缓存配置
    REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = REDIS_HOST
    CACHE_REDIS_PORT = REDIS_PORT
    CACHE_REDIS_DB = REDIS_DB
    CACHE_DEFAULT_TIMEOUT = 300


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
