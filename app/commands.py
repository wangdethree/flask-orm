import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import create_engine, text


def register_commands(app):
    @app.cli.command("sync-users")
    @with_appcontext
    def sync_users():
        """从远程数据库 A 同步用户数据到本地数据库 B"""
        remote_uri = current_app.config["REMOTE_DB_URI"]
        local_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]

        click.echo(f"Syncing from remote: {remote_uri}")
        click.echo(f"Syncing to local:   {local_uri}")

        remote_engine = create_engine(remote_uri)
        local_engine = create_engine(local_uri)

        try:
            with remote_engine.connect() as conn:
                rows = conn.execute(text("SELECT * FROM users")).mappings().all()
                click.echo(f"Fetched {len(rows)} users from remote DB")

            with local_engine.connect() as conn:
                for row in rows:
                    r = dict(row)
                    # 使用 ON DUPLICATE KEY UPDATE 策略实现 upsert
                    upsert_sql = text("""
                        INSERT INTO users (id, uuid, username, email, password_hash, is_active, created_at, updated_at)
                        VALUES (:id, :uuid, :username, :email, :password_hash, :is_active, :created_at, :updated_at)
                        ON DUPLICATE KEY UPDATE
                            uuid = VALUES(uuid),
                            username = VALUES(username),
                            email = VALUES(email),
                            password_hash = VALUES(password_hash),
                            is_active = VALUES(is_active),
                            updated_at = VALUES(updated_at)
                    """)
                    conn.execute(upsert_sql, r)
                conn.commit()

            click.echo("Sync completed successfully.")
        except Exception as e:
            click.echo(f"Sync failed: {e}", err=True)
            raise
        finally:
            remote_engine.dispose()
            local_engine.dispose()
