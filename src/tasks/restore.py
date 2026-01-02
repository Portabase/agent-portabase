import logging
from tasks.result import send_result_restoration
from celery import shared_task
from services.executor import RestoreExecutor
from core.context import AgentContext

logger = logging.getLogger("agent_logger")


@shared_task(name="tasks.restore")
def restore(payload):
    logger.info("Restore task started")

    try:
        logger.debug("Initializing AgentContext")
        ctx = AgentContext()

        logger.debug("Instantiating RestoreExecutor")
        executor = RestoreExecutor(ctx)

        logger.info("Executing restore process")
        executor.execute(payload)

        logger.info("restore task completed successfully")
        return {"message": True}


    except Exception as exc:
        logger.exception(f"Restore task failed, error: {str(exc)}")
        try:
            send_result_restoration.apply_async(args=("", payload.get("generatedId"), "failed", "manual",),
                                                ignore_result=True)
        except Exception as inner_e:
            logger.exception(f"Failed to send failure result: {inner_e}")
        return {"message": False}
