from domain.mysql import MySQLDatabase
from domain.postgres import PostgresDatabase


def get_file_extension(db_type: str) -> str | None:
    match db_type:
        case "postgresql":
            return ".dump"
        case "mysql":
            return ".sql"


class DatabaseFactory:
    @staticmethod
    def create(cfg, method):
        match cfg.type:
            case "postgresql":
                return PostgresDatabase(cfg, method)
            case "mysql":
                return MySQLDatabase(cfg, method)
            case _:
                raise ValueError("Unsupported DB type")
