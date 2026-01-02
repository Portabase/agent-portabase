import subprocess
import logging

logger = logging.getLogger("agent_logger")


class Database:
    def __init__(self, cfg, method):
        self.cfg = cfg
        self.method = method

    @staticmethod
    def execute(command, env=None, input_content: str = None):
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE if input_content else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                env=env
            )

            stdout_lines, stderr_lines = [], []

            if input_content and process.stdin:
                for line in input_content.splitlines():
                    process.stdin.write(line + "\n")
                process.stdin.close()

            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    logger.info(stdout_line.strip())
                    stdout_lines.append(stdout_line)
                if stderr_line:
                    logger.error(stderr_line.strip())
                    stderr_lines.append(stderr_line)

                if not stdout_line and not stderr_line and process.poll() is not None:
                    break

            if process.returncode != 0:
                return False, ''.join(stderr_lines)
            return True, ''.join(stdout_lines)

        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return False, f"Error: Exception during execution - {e}"
