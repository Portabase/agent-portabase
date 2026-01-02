from utils.get_databases_config import get_databases_config


class ConfigService:
    def __init__(self, ctx):
        self.ctx = ctx

    @staticmethod
    def load():
        data, ok = get_databases_config()
        if not ok:
            raise RuntimeError("Failed loading DB config")
        return data.databases
