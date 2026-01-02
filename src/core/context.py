import logging
from settings import config
from utils.edge_key import decode_edge_key

logger = logging.getLogger("agent_logger")


class AgentContext:
    def __init__(self):
        self.config = config

        if not config.EDGE_KEY:
            raise RuntimeError("EDGE_KEY missing")

        self.edge_key, ok = decode_edge_key(config.EDGE_KEY)
        if not ok:
            raise RuntimeError("Invalid EDGE_KEY")
        else:
            logger.debug("EDGE_KEY decoded")
