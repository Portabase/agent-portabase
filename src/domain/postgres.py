import os
from settings import config
from domain.database import Database


class PostgresDatabase(Database):
    def __init__(self, cfg, method):
        super().__init__(cfg, method)

        self.backup_file = f"{config.DATA_PATH}/files/backups/{method}/{cfg.generatedId}.dump"
        self.restore_file = f"{config.DATA_PATH}/files/restorations/{cfg.generatedId}.dump"

        self.password = cfg.password

        self.terminate_connections_cmd = [
            'psql',
            '-U', cfg.username,
            '-d', 'postgres',
            '-h', cfg.host,
            '-p', cfg.port,
            '-c',
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{cfg.database}' AND pid <> pg_backend_pid();"
        ]

        self.command_restore = ['pg_restore',
                                '--no-owner',
                                '--no-privileges',
                                '--clean',
                                '--if-exists',
                                '--create',
                                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(cfg.username, cfg.password, cfg.host,
                                                                              cfg.port, "postgres"),
                                '-v',
                                self.restore_file]

        self.command_backup = ['pg_dump',
                               '--dbname=postgresql://{}:{}@{}:{}/{}'.format(cfg.username, cfg.password, cfg.host, cfg.port,
                                                                             cfg.database),
                               '-Fc',
                               # '-Fd',
                               '-f', self.backup_file,
                               '-v',
                               # '--jobs=4'
                               '--compress=3'
                               ]

        self.command_ping = [
            'pg_isready',
            '--dbname=postgresql://{}:{}@{}:{}/{}'.format(cfg.username, cfg.password, cfg.host, cfg.port, cfg.database)
        ]

    def backup(self):
        status, result = self.execute(self.command_backup)
        return status, result, self.backup_file

    def restore(self):
        env = os.environ.copy()
        env["PGPASSWORD"] = self.password

        self.execute(self.terminate_connections_cmd, env=env)

        return self.execute(self.command_restore)

    def ping(self):
        return self.execute(self.command_ping)
