from tasks.backup import backup

class BackupService:
    def __init__(self, ctx):
        self.ctx = ctx

    @staticmethod
    def dispatch(payload):
        backup.delay(payload)
