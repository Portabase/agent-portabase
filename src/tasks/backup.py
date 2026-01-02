import logging

from celery import shared_task
from services.executor import BackupExecutor
from core.context import AgentContext
from tasks.result import send_result_backup, send_result_restoration

logger = logging.getLogger("agent_logger")


@shared_task()
def backup(payload):
    logger.info("Manual backup task started")
    try:
        logger.debug("Initializing AgentContext")
        ctx = AgentContext()

        logger.debug("Instantiating BackupExecutor")
        executor = BackupExecutor(ctx)

        logger.info("Executing manual backup")
        executor.execute(payload, "manual")

        logger.info("Manual backup task completed successfully")
        

    except Exception as exc:
        logger.exception(f"Manual backup task failed, error: {str(exc)}")
        try:
            send_result_backup.apply_async(args=("", payload.get("generatedId"), "failed", "manual",),
                                           ignore_result=True)
        except Exception as inner_e:
            logger.exception(f"Failed to send failure result: {inner_e}")
        return {"message": False}


@shared_task()
def periodic_backup(payload):
    logger.info("periodic backup task started")

    try:
        logger.debug("Initializing AgentContext")
        ctx = AgentContext()

        logger.debug("Instantiating BackupExecutor")
        executor = BackupExecutor(ctx)

        logger.info("Executing automatic (periodic) backup")
        executor.execute(payload, "automatic")

        logger.info("periodic backup task completed successfully")
        return {"message": True}

    except Exception as exc:
        logger.exception(f"periodic backup task failed, error: {str(exc)}")
        try:
            send_result_backup.apply_async(args=("", payload.get("generatedId"), "failed", "manual",),
                                           ignore_result=True)
        except Exception as inner_e:
            logger.exception(f"Failed to send failure result: {inner_e}")
        return {"message": False}
