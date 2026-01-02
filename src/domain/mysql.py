import os

from domain.database import Database
from settings import config


class MySQLDatabase(Database):
    def __init__(self, cfg, method):
        super().__init__(cfg, method)

        self.host = cfg.host
        self.database = cfg.database
        self.user = cfg.username
        self.password = cfg.password
        self.port = cfg.port

        self.backup_file = f"{config.DATA_PATH}/files/backups/{method}/{cfg.generatedId}.sql"
        self.restore_file = f"{config.DATA_PATH}/files/restorations/{cfg.generatedId}.sql"
        self.password = cfg.password

        self.command_backup = [
            'mysqldump',
            f'--host={cfg.host}',
            f'--port={cfg.port}',
            f'--user={cfg.username}',
            f'--password={cfg.password}',
            '--routines',
            '--events',
            '--triggers',
            '--single-transaction',
            '--quick',
            '--add-drop-database',
            '--verbose',
            '--databases', cfg.database,
            '-r', self.backup_file
        ]

        self.command_restore = [
            'mysql',
            f'--host={cfg.host}',
            f'--port={cfg.port}',
            f'--user={cfg.username}',
            f'--password={cfg.password}',
            # To confirm if interesting
            # '--verbose',
            cfg.database
        ]

        self.command_ping = [
            'mysqladmin',
            f'--host={cfg.host}',
            f'--port={cfg.port}',
            f'--user={cfg.username}',
            f'--password={cfg.password}',
            'ping'
        ]

    def backup(self):
        status, result = self.execute(self.command_backup)
        return status, result, self.backup_file

    def restore(self):
        env = os.environ.copy()
        env["MYSQL_PWD"] = self.password

        drop_create_cmd = [
            'mysql',
            f'--host={self.host}',
            f'--port={self.port}',
            f'--user={self.user}',
            f'--password={self.password}',
            '-e',
            f"DROP DATABASE IF EXISTS {self.database}; CREATE DATABASE {self.database};"
        ]
        self.execute(drop_create_cmd, env=env)

        with open(self.restore_file, 'r') as sql_file:
            restore_cmd = self.command_restore.copy()
            return self.execute(restore_cmd, env=env, input_content=sql_file.read())

    def ping(self):
        return self.execute(self.command_ping)
