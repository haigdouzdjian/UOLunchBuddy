import logging


def setup_log():
    logging.basicConfig(format='[%(asctime)s] <%(levelname)s> %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)


def log(message='', level=logging.INFO):
    logging.log(level, message)
