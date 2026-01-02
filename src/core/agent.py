from services.config import ConfigService
from services.status import StatusService
from services.cron import CronService
from services.backup import BackupService
from services.restore import RestoreService

class Agent:
    def __init__(self, ctx):
        self.ctx = ctx
        self.config_service = ConfigService(ctx)
        self.status_service = StatusService(ctx)
        self.cron_service = CronService(ctx)
        self.backup_service = BackupService(ctx)
        self.restore_service = RestoreService(ctx)

    def run(self):
        databases = self.config_service.load()
        server_state = self.status_service.ping(databases)

        for db in server_state["databases"]:
            self.cron_service.sync(db)

            if db["data"]["backup"]["action"]:
                self.backup_service.dispatch(db)

            elif db["data"]["restore"]["action"]:
                self.restore_service.dispatch(db)
