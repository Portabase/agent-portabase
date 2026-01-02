import logging
import requests

from domain.factory import get_file_extension
from settings import config

logger = logging.getLogger('agent_logger')


def upload_restoration_file(url: str, generated_id: str, db_type: str):
    try:
        file_ext = get_file_extension(db_type)
        response = requests.get(url)
        response.raise_for_status()
        filename = f'{config.DATA_PATH}/files/restorations/{generated_id}{file_ext}'

        with open(filename, "wb") as file:
            file.write(response.content)

        return f"File {filename} downloaded successfully.", True

    except Exception as e:
        # Catch any other exceptions
        logger.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}", False
