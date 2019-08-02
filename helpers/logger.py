import logging
import os

class Logger:
    def __init__(self, write_logs=False, log_path=None):
        self.write_logs = write_logs
        if self.write_logs:
            log_dir = log_path.rsplit('/', 1)[0]
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            logging.basicConfig(level=logging.DEBUG, filename=log_path, filemode='a+',
                                format="%(asctime)-15s %(levelname)-8s %(message)s")
    
    def info(self, message):
        if self.write_logs:
            logging.info(message)
        print('[INFO] {}'.format(message))
    
    def error(self, message):
        if self.write_logs:
            logging.info(message)
        print('[ERROR] {}'.format(message))
