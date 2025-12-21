import logging
import requests
from utils.edge_key import EdgeKey
from utils.get_databases_config import DatabaseConfig
from importlib.metadata import version

logger = logging.getLogger('agent_logger')


def formatted_database(database: DatabaseConfig):
    return {
        "name": database.name,
        "dbms": database.type,
        "generatedId": database.generatedId,
    }


def status_request(data: EdgeKey, databases):
    try:
        url = f"{data.serverUrl}/api/agent/{data.agentId}/status"
        logger.info(f'Status request | {url}')
        databases_items = []
        for database in databases:
            databases_items.append(formatted_database(database))
        body = {
            "version": version('portabase-agent'),
            "databases": databases_items,
        }
        response = requests.post(url=url, json=body)
        response.raise_for_status()
        return response.json(), True

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return f"Request error: {e}", False

    except ValueError as e:
        logger.error(f"JSON decoding error: {e}")
        return "Failed to parse JSON response", False

    except KeyError as e:
        logger.error(f"Missing key in input data: {e}")
        return f"Invalid input data: missing key {e}", False

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}", False
