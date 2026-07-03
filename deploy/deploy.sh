#!/bin/bash
# ============================================================
# 一键部署脚本 - 用于部署仓库
# 用法: ./deploy.sh
# ============================================================
set -e

REGISTRY="dockerhub.datagrand.com"
IMAGE="jinquzu/zuoye/flask-orm"
TAG="${TAG:-latest}"

echo "========================================="
echo "   Flask ORM 服务部署"
echo "   镜像: $REGISTRY/$IMAGE:$TAG"
echo "========================================="

# 1. 登录镜像仓库（如需要）
# docker login $REGISTRY -u "$REGISTRY_USERNAME" -p "$REGISTRY_PASSWORD"

# 2. 拉取最新镜像
echo "[1/4] 拉取镜像..."
docker pull $REGISTRY/$IMAGE:$TAG

# 3. 停止并删除旧容器（如果存在）
echo "[2/4] 停止旧服务..."
docker compose -f docker-compose.swarm.yml down 2>/dev/null || true

# 4. 启动服务
echo "[3/4] 启动服务..."
TAG=$TAG docker compose -f docker-compose.swarm.yml up -d

# 5. 等待服务就绪
echo "[4/4] 等待服务就绪..."
sleep 5

# 健康检查
echo ""
echo "========================================="
echo "   健康检查"
echo "========================================="

# 检查容器状态
docker compose -f docker-compose.swarm.yml ps

echo ""
if curl -sf http://localhost:80/health > /dev/null 2>&1; then
    echo "✅ 服务启动成功！"
else
    echo "⚠️  健康检查未通过，请查看日志:"
    echo "   docker compose -f docker-compose.swarm.yml logs"
fi
