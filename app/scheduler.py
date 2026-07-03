from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()


def init_scheduler(app):
    """初始化定时任务调度器"""
    scheduler.add_job(
        func=_run_sync,
        trigger="interval",
        minutes=30,
        id="sync_users_job",
        name="sync users from remote DB",
        replace_existing=True,
    )

    scheduler.start()

    # 应用退出时关闭调度器
    import atexit
    atexit.register(lambda: scheduler.shutdown())


def _run_sync():
    """通过 CLI runner 执行 sync-users 命令"""
    from flask import current_app
    from app import create_app

    app = create_app()
    with app.app_context():
        runner = app.test_cli_runner()
        result = runner.invoke(args=["sync-users"])
        print(result.output)
