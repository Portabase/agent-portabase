import logging
import json

import tomli
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from settings import config
from utils.format_validation import format_validation_error

logger = logging.getLogger('agent_logger')


class DatabaseConfig(BaseModel):
    name: str
    database: str
    type: str
    username: str
    password: str
    port: int
    host: str
    generatedId: str


class DatabasesConfig(BaseModel):
    databases: List[DatabaseConfig]


def get_databases_config(file_path: Optional[str] = None):
    """
    Get database config from file provided in DATABASES_CONFIG_FILE.
    Automatically supports JSON (.json) and TOML (.toml).
    If file_path is provided, it will override the default setting.
    """
    file_path = file_path or f"{config.DATA_PATH}/config/{config.DATABASES_CONFIG_FILE}"

    try:
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif file_path.endswith(".toml"):
            with open(file_path, "rb") as f:
                data = tomli.load(f)
        else:
            raise ValueError("Unsupported config file format. Use .json or .toml")

        obj = DatabasesConfig.model_validate(data)
        return obj, True

    except ValidationError as e:
        format_validation_error(e)
        return e, False
    except Exception as e:
        logger.exception("Error loading database config")
        return e, False
