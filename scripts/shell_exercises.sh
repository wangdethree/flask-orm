# ============================================================
# Shell 命令练习：find / grep / sed / xargs
# ============================================================

# ========== 1. find - 查找文件 ==========

# 查找所有 .py 文件
find . -name "*.py"

# 查找最近1天内修改的 .py 文件
find . -name "*.py" -mtime -1

# 查找大于 1KB 的 .py 文件
find . -name "*.py" -size +1k

# 查找目录（不查文件）
find . -type d -name "app*"

# 排除特定目录的查找
find . -name "*.py" -not -path "./venv/*" -not -path "./migrations/*"

# 查找并执行操作（-exec）
find . -name "*.pyc" -exec rm {} \;
find . -name "__pycache__" -type d -exec rm -rf {} +


# ========== 2. grep - 搜索内容 ==========

# 递归搜索 "User" 关键字
grep -r "User" app/

# 仅列出匹配的文件名
grep -rl "import jwt" app/

# 显示行号
grep -rn "db.session" app/

# 正则搜索（搜索函数定义）
grep -rn "def .*user" app/

# 排除目录
grep -rn "TODO" app/ --exclude-dir=__pycache__ --exclude-dir=venv

# 统计匹配次数
grep -rc "jsonify" app/

# 反向匹配（不包含某关键词的行）
grep -rn -v "import" app/models/user.py


# ========== 3. sed - 流编辑器 ==========

# 替换（仅打印，不修改文件）
sed 's/flask-orm/my-service/g' docker-compose.yml

# 原地替换
sed -i '' 's/5050/5000/g' manage.py

# 删除包含某关键词的行
sed '/import os/d' manage.py

# 在第 5 行后插入新行
sed '5a\# new comment' manage.py

# 仅替换第 N 行
sed '3s/development/production/' manage.py

# 批量替换多个文件中的内容（macOS）
find . -name "*.py" -not -path "./venv/*" -exec sed -i '' 's/old_string/new_string/g' {} \;


# ========== 4. xargs - 参数传递 ==========

# 查找所有 .py 文件并用 wc 统计行数
find app/ -name "*.py" | xargs wc -l

# 查找并删除 .pyc 文件
find . -name "*.pyc" | xargs rm -f

# 查找包含某关键词的文件后批量 sed 替换
grep -rl "SECRET_KEY" app/ | xargs sed -i '' 's/SECRET_KEY/APP_SECRET_KEY/g'

# 限制每次传递的参数数量（-n）
find . -name "*.py" | xargs -n 3 echo "Files:"

# 使用占位符 -I（支持任意位置插入）
find . -name "*.log" | xargs -I {} cp {} /tmp/backup/{}

# 并行执行（-P）
find . -name "*.py" | xargs -P 4 -I {} wc -l {}


# ========== 5. 组合实战 ==========

# 场景：查找所有 API 文件中包含 "db.session" 的行
find app/api/ -name "*.py" | xargs grep -n "db.session"

# 场景：统计整个项目代码行数（排除目录）
find . \( -name "*.py" -o -name "*.yml" -o -name "*.sh" \) \
  -not -path "./venv/*" -not -path "./migrations/versions/*" \
  | xargs wc -l | tail -1

# 场景：批量将 tab 缩进替换为 4 空格
find app/ -name "*.py" | xargs sed -i '' 's/\t/    /g'
