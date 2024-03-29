import json
import logging
import sys, os
import datetime
from logging.handlers import RotatingFileHandler
from logging import Handler, LogRecord, StreamHandler
import requests
import socket
from config.config import get_config

c = get_config()

# HOST_UP = True if os.system("ping -c 1 " + c.get('logger_url')) is 0 else False
HOST_UP = False


# Logger.exception() dumps a stack trace along with it. Call this method only from an exception handler.
class MyLogger:
    def __init__(self, logger_name=__name__, level=logging.DEBUG, file_size=2, backup=0):
        self.script_path = os.path.abspath(__file__)
        self.script_dir = os.path.split(self.script_path)[0]
        self.logger_name = logger_name
        self.level = level
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.level)
        self.formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')
        # self.fh = RotatingFileHandler(os.path.join(self.script_dir, '{:%Y-%m-%d}'.format(datetime.datetime.now()) + '.log'), maxBytes=file_size * 1000, backupCount=backup)
        # self.fh = logging.FileHandler(sys.path[1] + '\\' + '{:%Y-%m-%d}'.format(datetime.datetime.now()) + '.log')
        # self.fh.setLevel(self.level)

        # self.sh = logging.StreamHandler()
        self.sh = MyCustomHandler(logger_url=c.get('logger_url'), logger_port=c.get('logger_port'))
        self.sh.setLevel(self.level)

        # self.fh.setFormatter(self.formatter)
        self.sh.setFormatter(self.formatter)
        # self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh) if HOST_UP else None

    def set_level(self, level):
        self.logger.setLevel(level)
        # self.fh.setLevel(level)
        self.sh.setLevel(level)

    def get_logger(self):
        return self.logger


class MyCustomHandler(StreamHandler):
    def __init__(self, logger_url: str, logger_port: str):
        StreamHandler.__init__(self)
        self.logger_url = logger_url
        self.logger_port = logger_port

    def emit(self, record: LogRecord) -> None:
        # print('record-------', record)
        try:
            url = f"{c.get('logger_protocol')}://{c.get('logger_url')}:{c.get('logger_port')}/logs"

            payload = json.dumps({"app_name": c.get('app_name'),
                                  "namespace": "",
                                  "host": socket.gethostname(),
                                  "service": record.name,
                                  "level": record.levelname,
                                  "service_module": record.module,
                                  "func_name": record.funcName,
                                  "message": record.msg
                                  })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request('POST', url, headers=headers, data=payload)
            print(response.text)
            # a = json.loads(json.dumps(record.__dict__))
            # print(a)
        except Exception as e:
            print(e.__str__())
