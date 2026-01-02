import logging
import os

from domain.factory import get_file_extension
from settings import config

logger = logging.getLogger('agent_logger')


def delete_old_file(file_name, kind, db_type):
    file_ext = get_file_extension(db_type)
    folder = f'{config.DATA_PATH}/files/{kind}/'
    file_path = os.path.join(folder, f'{file_name}{file_ext}')
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
        return True
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
