from utils.cron import check_and_update_cron


class CronService:
    def __init__(self, ctx):
        self.ctx = ctx

    @staticmethod
    def sync(database):
        check_and_update_cron(database)
