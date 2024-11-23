import json
from datetime import datetime

class Logger:
    def __init__(self, logfile):
        self.logfile = logfile
        self.logs = []

    def log(self, command, result):
        entry = {
            "command": command,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.logs.append(entry)

    def save(self):
        with open(self.logfile, "w") as log_file:
            json.dump(self.logs, log_file, indent=4)
