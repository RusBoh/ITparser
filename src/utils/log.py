import logging, sys


def set_logger(level = logging.INFO, log_file: str = None, form: str = None):
    root = logging.getLogger()

    root.setLevel(level)

    for handler in root.handlers[:]:
        root.removeHandler(handler)

    formatter = logging.Formatter()
    if form:
        formatter = logging.Formatter(fmt=form)
    
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

