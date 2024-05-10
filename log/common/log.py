import logging
import os

from colorlog import ColoredFormatter


class CommonLogger:
    def __init__(self):
        module_name = 'logs'

        folder_path = f'../{module_name}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - 进程[%(processName)s] - 线程[%(threadName)s] - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)

        info_file_handler = logging.FileHandler(f'{folder_path}/info_log.txt', encoding='utf-8')
        info_file_handler.setFormatter(formatter)
        info_file_handler.setLevel(logging.INFO)

        warning_file_handler = logging.FileHandler(f'{folder_path}/warning_log.txt', encoding='utf-8')
        warning_file_handler.setFormatter(formatter)
        warning_file_handler.setLevel(logging.WARNING)

        error_file_handler = logging.FileHandler(f'{folder_path}/error_log.txt', encoding='utf-8')
        error_file_handler.setFormatter(formatter)
        error_file_handler.setLevel(logging.ERROR)

        self.logger = logging.getLogger('common_logger')
        self.logger.addHandler(error_file_handler)
        self.logger.addHandler(warning_file_handler)
        self.logger.addHandler(info_file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)

        werkzeug_log = logging.getLogger('werkzeug')
        werkzeug_log.setLevel(logging.ERROR)


# 在使用时，创建CustomLogger的实例
common_logger = CommonLogger()
logger = common_logger.logger
