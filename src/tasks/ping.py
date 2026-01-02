import logging

from celery import shared_task
from core.context import AgentContext
from core.agent import Agent

logger = logging.getLogger("agent_logger")


@shared_task(name="periodic.ping_server")
def ping_server():
    logger.info("ping_server task started")

    try:
        logger.debug("Initializing AgentContext")
        ctx = AgentContext()

        logger.debug("Instantiating Agent")
        agent = Agent(ctx)

        logger.info("Running Agent")
        agent.run()

        logger.info("ping_server task completed successfully")
        return {"message": True}

    except Exception as exc:
        logger.exception("ping_server task failed")
        raise
