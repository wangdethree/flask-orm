#!/bin/bash
set -e

# 等待数据库就绪
echo "Waiting for MySQL..."
while ! nc -z ${DB_HOST:-mysql} ${DB_PORT:-3306}; do
    sleep 2
done

echo "Waiting for Redis..."
while ! nc -z ${REDIS_HOST:-redis} ${REDIS_PORT:-6379}; do
    sleep 2
done

# 执行数据库迁移
echo "Running database migrations..."
flask db upgrade

# 启动应用
echo "Starting application..."
exec "$@"
