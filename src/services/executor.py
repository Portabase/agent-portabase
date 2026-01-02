import logging

from utils.clear_file_directory import delete_old_file
from utils.get_databases_config import get_databases_config
from domain.factory import DatabaseFactory
from tasks.result import send_result_backup, send_result_restoration
from utils.upload_restoration_file import upload_restoration_file

logger = logging.getLogger("agent_logger")


class BackupExecutor:
    def __init__(self, ctx):
        self.ctx = ctx

    @staticmethod
    def execute(payload, method):
        databases, _ = get_databases_config()
        cfg = next(db for db in databases.databases if db.generatedId == payload["generatedId"])

        result = delete_old_file(cfg.generatedId, f"backups/{method}", cfg.type)
        if result:
            db = DatabaseFactory.create(cfg, method)
            ok_ping, _ = db.ping()
            if ok_ping:
                ok, _, file = db.backup()
                if ok:
                    send_result_backup.apply_async(args=(file, cfg.generatedId, "success", method,), ignore_result=True)
                    return
        send_result_backup.apply_async(args=("", cfg.generatedId, "failed", method,), ignore_result=True)


class RestoreExecutor:
    def __init__(self, ctx):
        self.ctx = ctx

    @staticmethod
    def execute(payload):
        databases, _ = get_databases_config()
        cfg = next(db for db in databases.databases if db.generatedId == payload["generatedId"])
        url = payload['data']['restore']['file']

        result = delete_old_file(cfg.generatedId, "restorations", cfg.type)
        if result:
            result_upload, status = upload_restoration_file(url, cfg.generatedId, cfg.type)
            if status:
                db = DatabaseFactory.create(cfg, "")
                ok, _ = db.restore()
                if ok:
                    send_result_restoration.apply_async(args=(cfg.generatedId, "success" if ok else "failed"),
                                                        ignore_result=True)
                    return
        send_result_restoration.apply_async(args=(cfg.generatedId, "failed"), ignore_result=True)
