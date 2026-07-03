import os

from app import create_app, db
from app.scheduler import init_scheduler

config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)

# 启动定时任务（仅非 debug 模式下启动，避免 Flask reload 导致重复任务）
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    init_scheduler(app)


@app.shell_context_processor
def make_shell_context():
    return {"db": db}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
