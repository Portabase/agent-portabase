from tasks.restore import restore

class RestoreService:
    def __init__(self, ctx):
        self.ctx = ctx

    @staticmethod
    def dispatch(payload):
        restore.delay(payload)
