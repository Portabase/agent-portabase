from utils.status_request import status_request

class StatusService:
    def __init__(self, ctx):
        self.ctx = ctx

    def ping(self, databases):
        result, ok = status_request(self.ctx.edge_key, databases)
        if not ok:
            raise RuntimeError("Status request failed")
        return result
